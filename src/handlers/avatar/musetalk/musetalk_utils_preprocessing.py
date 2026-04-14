import logging
import os
import pickle

import cv2
import numpy as np
import torch
from tqdm import tqdm

from musetalk.utils.face_detection import FaceAlignment, LandmarksType

import onnxruntime as ort

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# DWPose ONNX model constants (match mmpose RTMPose-L wholebody-384x288)
# ---------------------------------------------------------------------------
_MODEL_INPUT_SIZE = (288, 384)  # (width, height)
_MEAN = np.array([123.675, 116.28, 103.53], dtype=np.float32)
_STD = np.array([58.395, 57.12, 57.375], dtype=np.float32)
_SIMCC_SPLIT_RATIO = 2.0


# ---------------------------------------------------------------------------
# Preprocessing helpers (replicate mmpose TopdownAffine + PoseDataPreprocessor)
# ---------------------------------------------------------------------------

def _bbox_xyxy2cs(bbox, padding=1.25):
    """Convert [x1,y1,x2,y2] bbox to (center, scale), matching mmpose
    GetBBoxCenterScale with padding=1.25."""
    x1, y1, x2, y2 = bbox
    center = np.array([(x1 + x2) * 0.5, (y1 + y2) * 0.5], dtype=np.float32)
    scale = np.array([(x2 - x1) * padding, (y2 - y1) * padding],
                     dtype=np.float32)
    return center, scale


def _rotate_point(pt, angle_rad):
    sn, cs = np.sin(angle_rad), np.cos(angle_rad)
    rot_mat = np.array([[cs, -sn], [sn, cs]])
    return rot_mat @ pt


def _get_3rd_point(a, b):
    direction = a - b
    return b + np.r_[-direction[1], direction[0]]


def _get_warp_matrix(center, scale, rot, output_size, inv=False):
    """Compute 2x3 affine warp matrix (identical to mmpose / rtmlib)."""
    shift = np.array([0., 0.])
    src_w = scale[0]
    dst_w, dst_h = output_size

    rot_rad = np.deg2rad(rot)
    src_dir = _rotate_point(np.array([0., src_w * -0.5]), rot_rad)
    dst_dir = np.array([0., dst_w * -0.5])

    src = np.zeros((3, 2), dtype=np.float32)
    src[0, :] = center + scale * shift
    src[1, :] = center + src_dir + scale * shift
    src[2, :] = _get_3rd_point(src[0, :], src[1, :])

    dst = np.zeros((3, 2), dtype=np.float32)
    dst[0, :] = [dst_w * 0.5, dst_h * 0.5]
    dst[1, :] = np.array([dst_w * 0.5, dst_h * 0.5]) + dst_dir
    dst[2, :] = _get_3rd_point(dst[0, :], dst[1, :])

    if inv:
        warp_mat = cv2.getAffineTransform(np.float32(dst), np.float32(src))
    else:
        warp_mat = cv2.getAffineTransform(np.float32(src), np.float32(dst))
    return warp_mat


def _top_down_affine(input_size, bbox_scale, bbox_center, img):
    """Affine-warp *img* so that the bbox region fills *input_size*."""
    w, h = input_size
    aspect_ratio = w / h
    bw, bh = bbox_scale[0], bbox_scale[1]
    if bw > bh * aspect_ratio:
        bbox_scale = np.array([bw, bw / aspect_ratio], dtype=np.float32)
    else:
        bbox_scale = np.array([bh * aspect_ratio, bh], dtype=np.float32)

    warp_mat = _get_warp_matrix(bbox_center, bbox_scale, 0, (w, h))
    img = cv2.warpAffine(img, warp_mat, (int(w), int(h)),
                         flags=cv2.INTER_LINEAR)
    return img, bbox_scale


# ---------------------------------------------------------------------------
# Post-processing helpers (replicate mmpose SimCC decoding)
# ---------------------------------------------------------------------------

def _get_simcc_maximum(simcc_x, simcc_y):
    """Decode SimCC representations to keypoint locations and scores."""
    N, K, Wx = simcc_x.shape
    simcc_x_flat = simcc_x.reshape(N * K, -1)
    simcc_y_flat = simcc_y.reshape(N * K, -1)

    x_locs = np.argmax(simcc_x_flat, axis=1)
    y_locs = np.argmax(simcc_y_flat, axis=1)
    locs = np.stack((x_locs, y_locs), axis=-1).astype(np.float32)

    max_val_x = np.amax(simcc_x_flat, axis=1)
    max_val_y = np.amax(simcc_y_flat, axis=1)
    vals = 0.5 * (max_val_x + max_val_y)
    locs[vals <= 0.] = -1

    return locs.reshape(N, K, 2), vals.reshape(N, K)


# ---------------------------------------------------------------------------
# Combined inference function
# ---------------------------------------------------------------------------

def _preprocess_image(img, input_size=_MODEL_INPUT_SIZE):
    """Full preprocessing: full-image bbox -> affine -> BGR2RGB -> normalize.

    Replicates mmpose ``inference_topdown`` behaviour when called without
    explicit bounding boxes (i.e. using the whole image as the person bbox).
    """
    h, w = img.shape[:2]
    bbox = [0, 0, w, h]
    center, scale = _bbox_xyxy2cs(bbox, padding=1.25)
    img_warped, scale = _top_down_affine(input_size, scale, center, img)
    img_rgb = cv2.cvtColor(img_warped, cv2.COLOR_BGR2RGB)
    img_norm = (img_rgb.astype(np.float32) - _MEAN) / _STD
    img_tensor = img_norm.transpose(2, 0, 1)[None].astype(np.float32)
    return img_tensor, center, scale


def _postprocess_simcc(simcc_x, simcc_y, center, scale,
                       input_size=_MODEL_INPUT_SIZE):
    """SimCC decode + rescale keypoints back to original image coordinates."""
    locs, scores = _get_simcc_maximum(simcc_x, simcc_y)
    keypoints = locs / _SIMCC_SPLIT_RATIO
    keypoints = keypoints / np.array(input_size, dtype=np.float32) * scale
    keypoints = keypoints + center - scale / 2
    return keypoints


def _inference_dwpose(session, img):
    """Run DWPose ONNX inference on a single BGR image.

    Returns keypoints array of shape (1, 133, 2), equivalent to
    ``mmpose.inference_topdown`` → ``merge_data_samples`` →
    ``.pred_instances.keypoints``.
    """
    input_tensor, center, scale = _preprocess_image(img)
    input_name = session.get_inputs()[0].name
    outputs = session.run(None, {input_name: input_tensor})
    simcc_x, simcc_y = outputs[0], outputs[1]
    return _postprocess_simcc(simcc_x, simcc_y, center, scale)


# ---------------------------------------------------------------------------
# Module-level initialization
# ---------------------------------------------------------------------------

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.getcwd()

# DWPose ONNX session: lazy-loaded on first use (only needed by prepare_material)
_dwpose_session = None


_cudnn_preloaded = False


def _ensure_cudnn_available():
    """Pre-load pip-installed nvidia cuDNN libs so that onnxruntime's dlopen
    can find libcudnn_adv.so.9, libcudnn_cnn.so.9, etc.

    When cuDNN is installed via ``nvidia-cudnn-cu12`` (pip), the .so files
    live under site-packages/nvidia/cudnn/lib/ which is NOT on the default
    LD_LIBRARY_PATH.  We fix this by both updating the env var (for future
    dlopen calls) and pre-loading the main libcudnn.so.9 via ctypes."""
    global _cudnn_preloaded
    if _cudnn_preloaded:
        return
    _cudnn_preloaded = True

    try:
        import nvidia.cudnn as _cudnn
        cudnn_base = list(_cudnn.__path__)[0]
        cudnn_lib_dir = os.path.join(cudnn_base, "lib")
    except (ImportError, IndexError):
        return

    if not os.path.isdir(cudnn_lib_dir):
        return

    ld_path = os.environ.get("LD_LIBRARY_PATH", "")
    if cudnn_lib_dir not in ld_path:
        os.environ["LD_LIBRARY_PATH"] = (
            cudnn_lib_dir + (":" + ld_path if ld_path else "")
        )

    import ctypes
    import glob
    for lib in sorted(glob.glob(os.path.join(cudnn_lib_dir, "libcudnn*.so.9"))):
        try:
            ctypes.CDLL(lib, mode=ctypes.RTLD_GLOBAL)
        except OSError:
            pass
    logger.info("Pre-loaded cuDNN 9 libs from %s", cudnn_lib_dir)


def _get_dwpose_session():
    """Lazy-initialize the DWPose ONNX Runtime session on first call."""
    global _dwpose_session
    if _dwpose_session is not None:
        return _dwpose_session

    onnx_path = os.path.join(project_root, "models", "musetalk", "dwpose",
                             "dw-ll_ucoco_384.onnx")
    if not os.path.exists(onnx_path):
        raise FileNotFoundError(
            f"DWPose ONNX model not found at {onnx_path}. "
            f"Download it with: hf download yzd-v/DWPose "
            f"--local-dir models/musetalk/dwpose --include dw-ll_ucoco_384.onnx"
        )

    providers = []
    if torch.cuda.is_available():
        _ensure_cudnn_available()
        providers.append("CUDAExecutionProvider")
    providers.append("CPUExecutionProvider")

    _dwpose_session = ort.InferenceSession(onnx_path, providers=providers)
    active = _dwpose_session.get_providers()
    logger.info("DWPose ONNX session initialized, active providers: %s", active)
    return _dwpose_session


# S3FD face detection: also lazy-loaded
_fa_instance = None


def _get_face_alignment():
    """Lazy-initialize S3FD FaceAlignment on first call."""
    global _fa_instance
    if _fa_instance is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        _fa_instance = FaceAlignment(LandmarksType._2D, flip_input=False,
                                     device=device)
    return _fa_instance


coord_placeholder = (0.0, 0.0, 0.0, 0.0)


# ---------------------------------------------------------------------------
# Public API (unchanged signatures)
# ---------------------------------------------------------------------------

def resize_landmark(landmark, w, h, new_w, new_h):
    w_ratio = new_w / w
    h_ratio = new_h / h
    landmark_norm = landmark / [w, h]
    landmark_resized = landmark_norm * [new_w, new_h]
    return landmark_resized


def read_imgs(img_list):
    frames = []
    logger.info('reading images...')
    for img_path in tqdm(img_list):
        frame = cv2.imread(img_path)
        frames.append(frame)
    return frames


def get_bbox_range(img_list, upperbondrange=0):
    frames = read_imgs(img_list)
    batch_size_fa = 1
    batches = [frames[i:i + batch_size_fa]
               for i in range(0, len(frames), batch_size_fa)]
    coords_list = []
    if upperbondrange != 0:
        logger.info('get key_landmark and face bounding boxes with the bbox_shift: %s',
                     upperbondrange)
    else:
        logger.info('get key_landmark and face bounding boxes with the default value')
    average_range_minus = []
    average_range_plus = []
    session = _get_dwpose_session()
    fa = _get_face_alignment()
    for fb in tqdm(batches):
        keypoints = _inference_dwpose(session, np.asarray(fb)[0])
        face_land_mark = keypoints[0][23:91]
        face_land_mark = face_land_mark.astype(np.int32)

        bbox = fa.get_detections_for_batch(np.asarray(fb))

        for j, f in enumerate(bbox):
            if f is None:
                coords_list += [coord_placeholder]
                continue

            half_face_coord = face_land_mark[29]
            range_minus = (face_land_mark[30] - face_land_mark[29])[1]
            range_plus = (face_land_mark[29] - face_land_mark[28])[1]
            average_range_minus.append(range_minus)
            average_range_plus.append(range_plus)
            if upperbondrange != 0:
                half_face_coord[1] = upperbondrange + half_face_coord[1]

    text_range = (
        f"Total frame: {len(frames)}, Manually adjust range: "
        f"[-{int(sum(average_range_minus) / len(average_range_minus))}"
        f"~{int(sum(average_range_plus) / len(average_range_plus))}], "
        f"current value: {upperbondrange}"
    )
    return text_range


def get_landmark_and_bbox(img_list, upperbondrange=0):
    frames = read_imgs(img_list)
    batch_size_fa = 1
    batches = [frames[i:i + batch_size_fa]
               for i in range(0, len(frames), batch_size_fa)]
    coords_list = []
    if upperbondrange != 0:
        logger.info('get key_landmark and face bounding boxes with the bbox_shift: %s',
                     upperbondrange)
    else:
        logger.info('get key_landmark and face bounding boxes with the default value')
    average_range_minus = []
    average_range_plus = []
    session = _get_dwpose_session()
    fa = _get_face_alignment()
    for fb in tqdm(batches):
        keypoints = _inference_dwpose(session, np.asarray(fb)[0])
        face_land_mark = keypoints[0][23:91]
        face_land_mark = face_land_mark.astype(np.int32)

        bbox = fa.get_detections_for_batch(np.asarray(fb))

        for j, f in enumerate(bbox):
            if f is None:
                coords_list += [coord_placeholder]
                continue

            half_face_coord = face_land_mark[29]
            range_minus = (face_land_mark[30] - face_land_mark[29])[1]
            range_plus = (face_land_mark[29] - face_land_mark[28])[1]
            average_range_minus.append(range_minus)
            average_range_plus.append(range_plus)
            if upperbondrange != 0:
                half_face_coord[1] = upperbondrange + half_face_coord[1]
            half_face_dist = np.max(face_land_mark[:, 1]) - half_face_coord[1]
            upper_bond = half_face_coord[1] - half_face_dist

            f_landmark = (np.min(face_land_mark[:, 0]), int(upper_bond),
                          np.max(face_land_mark[:, 0]),
                          np.max(face_land_mark[:, 1]))
            x1, y1, x2, y2 = f_landmark

            if y2 - y1 <= 0 or x2 - x1 <= 0 or x1 < 0:
                coords_list += [f]
                logger.warning("error bbox: %s", f)
            else:
                coords_list += [f_landmark]

    avg_minus = int(sum(average_range_minus) / len(average_range_minus))
    avg_plus = int(sum(average_range_plus) / len(average_range_plus))
    logger.info(
        "bbox_shift parameter adjustment — Total frames: %d, "
        "Manually adjust range: [-%d ~ %d], current value: %d",
        len(frames), avg_minus, avg_plus, upperbondrange,
    )
    return coords_list, frames


if __name__ == "__main__":
    img_list = [
        "./results/lyria/00000.png",
        "./results/lyria/00001.png",
        "./results/lyria/00002.png",
        "./results/lyria/00003.png",
    ]
    crop_coord_path = "./coord_face.pkl"
    coords_list, full_frames = get_landmark_and_bbox(img_list)
    with open(crop_coord_path, 'wb') as f:
        pickle.dump(coords_list, f)

    for bbox, frame in zip(coords_list, full_frames):
        if bbox == coord_placeholder:
            continue
        x1, y1, x2, y2 = bbox
        crop_frame = frame[y1:y2, x1:x2]
        print('Cropped shape', crop_frame.shape)

    print(coords_list)
