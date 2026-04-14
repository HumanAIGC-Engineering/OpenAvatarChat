import os
import torch

# Patch torch.load for PyTorch 2.6+ (weights_only defaults to True).
# Same approach as src/demo.py — needed here because musetalk_algo.py can run standalone.
_original_torch_load = torch.load
def _patched_torch_load(*args, **kwargs):
    if 'weights_only' not in kwargs or kwargs['weights_only'] != True:
        kwargs['weights_only'] = False
    return _original_torch_load(*args, **kwargs)
torch.load = _patched_torch_load

import numpy as np
import cv2
from typing import Optional, List
import threading
import time
from tqdm import tqdm
import copy
import sys
from transformers import WhisperModel
import argparse
import shutil
import json
import pickle
import glob
import builtins
import librosa
from loguru import logger

# Add MuseTalk module path
current_dir = os.path.dirname(os.path.abspath(__file__))
musetalk_module_path = os.path.join(current_dir, "MuseTalk")
if musetalk_module_path not in sys.path:
    sys.path.append(musetalk_module_path)

handlers_dir = os.getcwd()
handlers_dir = os.path.join(handlers_dir, "src")
if handlers_dir not in sys.path:
    sys.path.append(handlers_dir)

from handlers.avatar.musetalk.musetalk_utils_preprocessing import get_landmark_and_bbox

# Now you can correctly import MuseTalk modules
from musetalk.utils.face_parsing import FaceParsing
from musetalk.utils.utils import load_all_model
from musetalk.utils.blending import get_image_prepare_material
from musetalk.utils.audio_processor import AudioProcessor

_original_input = builtins.input

def video2imgs(vid_path, save_path, ext='.png', cut_frame=10000000):
    cap = cv2.VideoCapture(vid_path)
    try:
        count = 0
        while True:
            if count > cut_frame:
                break
            ret, frame = cap.read()
            if ret:
                cv2.imwrite(f"{save_path}/{count:08d}.png", frame)
                count += 1
            else:
                break
    finally:
        cap.release()

def osmakedirs(path_list):
    for path in path_list:
        os.makedirs(path) if not os.path.exists(path) else None

class MuseTalkAlgoV15:
    def __init__(self, avatar_id, video_path, bbox_shift, batch_size, force_preparation=False,
                 parsing_mode='jaw', left_cheek_width=90, right_cheek_width=90,
                 audio_padding_length_left=2, audio_padding_length_right=2, fps=25,
                 version="v15",
                 result_dir='./results',
                 extra_margin=10,
                 vae_type="sd-vae",
                 unet_model_path=None,
                 unet_config=None,
                 whisper_dir=None,
                 gpu_id=0,
                 debug=False):
        """Initialize MuseTalkAlgoV15
        
        Args:
            avatar_id (str): Avatar ID
            video_path (str): Video path
            bbox_shift (int): Face bounding box offset
            batch_size (int): Batch size
            force_preparation (bool): Whether to force data preparation
            parsing_mode (str): Face parsing mode, default 'jaw'
            left_cheek_width (int): Left cheek width
            right_cheek_width (int): Right cheek width
            audio_padding_length_left (int): Audio left padding length
            audio_padding_length_right (int): Audio right padding length
            fps (int): Video frame rate
            version (str): MuseTalk version
            result_dir (str): Output directory for results
            extra_margin (int): Extra margin
            vae_type (str): VAE model type (e.g. "sd-vae")
            unet_model_path (str): UNet model path
            unet_config (str): UNet config file path
            whisper_dir (str): Whisper model directory
            gpu_id (int): GPU device ID
        """
        self.avatar_id = avatar_id
        self.video_path = video_path
        self.bbox_shift = bbox_shift
        self.batch_size = batch_size
        self.force_preparation = force_preparation
        self.parsing_mode = parsing_mode
        self.left_cheek_width = left_cheek_width
        self.right_cheek_width = right_cheek_width
        self.audio_padding_length_left = audio_padding_length_left
        self.audio_padding_length_right = audio_padding_length_right
        self.fps = fps
        self.version = version
        self.result_dir = result_dir
        self.extra_margin = extra_margin
        self.unet_model_path = unet_model_path
        self.vae_type = vae_type
        self.unet_config = unet_config
        self.whisper_dir = whisper_dir
        self.gpu_id = gpu_id
        self.debug = debug
        
        # Set paths
        if self.version == "v15":
            self.base_path = os.path.join(self.result_dir, self.version, "avatars", avatar_id)
        else:  # v1
            self.base_path = os.path.join(self.result_dir, "avatars", avatar_id)
            
        self.avatar_path = self.base_path
        self.full_imgs_path = os.path.join(self.avatar_path, "full_imgs")
        self.coords_path = os.path.join(self.avatar_path, "coords.pkl")
        self.latents_out_path = os.path.join(self.avatar_path, "latents.pt")
        self.video_out_path = os.path.join(self.avatar_path, "vid_output")
        self.mask_out_path = os.path.join(self.avatar_path, "mask")
        self.mask_coords_path = os.path.join(self.avatar_path, "mask_coords.pkl")
        self.avatar_info_path = os.path.join(self.avatar_path, "avator_info.json")
        self.frames_path = os.path.join(self.avatar_path, "frames.pkl")
        self.masks_path = os.path.join(self.avatar_path, "masks.pkl")
        
        self.avatar_info = {
            "avatar_id": avatar_id,
            "video_path": video_path,
            "bbox_shift": bbox_shift,
            "version": self.version
        }
        
        # Model related
        self.device = None
        self.vae = None
        self.unet = None
        self.pe = None
        self.whisper = None
        self.fp = None
        self.audio_processor = None
        self.weight_dtype = None
        self.timesteps = None
        
        # Data related
        self.input_latent_list_cycle = None
        self.coord_list_cycle = None
        self.frame_list_cycle = None
        self.mask_coords_list_cycle = None
        self.mask_list_cycle = None

        # Inference lock for multi-session GPU access serialization
        self._inference_lock = threading.Lock()
        
        # Initialization
        self.init()

    def init(self):
        """Initialize digital avatar
        
        Automatically determine whether to regenerate data by checking the integrity of files in the avatar directory.
        If force_preparation is True, force regeneration.
        Files to check include:
        1. latents.pt - latent features file
        2. coords.pkl - face coordinates file
        3. mask_coords.pkl - mask coordinates file
        4. avator_info.json - config info file
        5. frames.pkl - frame data file
        6. masks.pkl - mask data file
        """
        # 1. Check if data preparation is needed
        required_files = [
            self.latents_out_path,      # latent features file
            self.coords_path,           # face coordinates file
            self.mask_coords_path,      # mask coordinates file
            self.avatar_info_path,      # config info file
            self.frames_path,           # frame data file
            self.masks_path,            # mask data file
        ]

        # Check if data needs to be generated
        need_preparation = self.force_preparation  # If force regeneration, set to True
        
        if not need_preparation and os.path.exists(self.avatar_path):
            # Check if all required files exist
            for file_path in required_files:
                if not os.path.exists(file_path):
                    need_preparation = True
                    break
            
            # If config file exists, check if bbox_shift has changed
            if os.path.exists(self.avatar_info_path):
                with open(self.avatar_info_path, "r") as f:
                    avatar_info = json.load(f)
                if avatar_info['bbox_shift'] != self.avatar_info['bbox_shift']:
                    logger.error(f"bbox_shift changed from {avatar_info['bbox_shift']} to {self.avatar_info['bbox_shift']}, need re-preparation")
                    need_preparation = True
        else:
            need_preparation = True

        # 2. Initialize device and models
        self.device = torch.device(f"cuda:{self.gpu_id}" if torch.cuda.is_available() else "cpu")
        self.timesteps = torch.tensor([0], device=self.device)

        # Load models
        self.vae, self.unet, self.pe = load_all_model(
            unet_model_path=self.unet_model_path,
            vae_type=self.vae_type,
            unet_config=self.unet_config,
            device=self.device
        )

        # Convert to half precision
        self.pe = self.pe.half().to(self.device)
        self.vae.vae = self.vae.vae.half().to(self.device)
        self.unet.model = self.unet.model.half().to(self.device)
        self.weight_dtype = self.unet.model.dtype

        # Initialize audio processor and Whisper model
        self.audio_processor = AudioProcessor(feature_extractor_path=self.whisper_dir)
        self.whisper = WhisperModel.from_pretrained(self.whisper_dir)
        self.whisper = self.whisper.to(device=self.device, dtype=self.weight_dtype).eval()
        self.whisper.requires_grad_(False)

        # Initialize face parser
        if self.version == "v15":
            self.fp = FaceParsing(
                left_cheek_width=self.left_cheek_width,
                right_cheek_width=self.right_cheek_width
            )
        else:
            self.fp = FaceParsing()
            
        # 3. Prepare or load data
        if need_preparation:
            logger.info("*********************************")
            if self.force_preparation:
                logger.info(f"  force creating avatar: {self.avatar_id}")
            else:
                logger.info(f"  creating avatar: {self.avatar_id}")
            logger.info("*********************************")
            # If directory exists but needs regeneration, delete it first
            if os.path.exists(self.avatar_path):
                shutil.rmtree(self.avatar_path)
            # Create required directories
            osmakedirs([self.avatar_path, self.full_imgs_path, self.video_out_path, self.mask_out_path])
            # Generate data
            self.prepare_material()
        else:
            logger.info(f"Avatar {self.avatar_id} exists and is complete, loading existing data...")
            # Load existing data
            self.input_latent_list_cycle = torch.load(self.latents_out_path, weights_only=True)
            with open(self.coords_path, 'rb') as f:
                self.coord_list_cycle = pickle.load(f)
            with open(self.frames_path, 'rb') as f:
                self.frame_list_cycle = pickle.load(f)
            with open(self.mask_coords_path, 'rb') as f:
                self.mask_coords_list_cycle = pickle.load(f)
            with open(self.masks_path, 'rb') as f:
                self.mask_list_cycle = pickle.load(f)

        # Warmup is skipped here; each worker thread warms up its own GPU path on start.

    def _warmup_models(self):
        """
        Warm up all models and feature extraction pipeline to avoid first-frame delay.
        """
        import time
        t_warmup_start = time.time()
        whisper_warmup_time = 0
        generate_frames_warmup_time = 0
        whisper_warmup_ok = False
        generate_frames_warmup_ok = False
       
        try:
            t0 = time.time()
            self._warmup_whisper_feature()
            whisper_warmup_time = time.time() - t0
            whisper_warmup_ok = True
        except Exception as e:
            logger.opt(exception=True).error(f"extract_whisper_feature warmup error: {str(e)}")
        
        try:
            t0 = time.time()
            dummy_whisper = torch.zeros(self.batch_size, 50, 384, device=self.device, dtype=self.weight_dtype)
            _ = self.generate_frames(dummy_whisper, 0, self.batch_size)
            generate_frames_warmup_time = time.time() - t0
            generate_frames_warmup_ok = True
        except Exception as e:
            logger.opt(exception=True).error(f"generate_frames warmup error: {str(e)}")
        
        if torch.cuda.is_available():
            torch.cuda.synchronize()
        t_warmup_end = time.time()
        logger.info(
            f"All models warmed up via generate_frames pipeline (batch_size={self.batch_size}, zeros) | "
            f"extract_whisper_feature: {whisper_warmup_time*1000:.1f} ms ({'OK' if whisper_warmup_ok else 'FAIL'}), "
            f"generate_frames: {generate_frames_warmup_time*1000:.1f} ms ({'OK' if generate_frames_warmup_ok else 'FAIL'}), "
            f"total: {(t_warmup_end - t_warmup_start)*1000:.1f} ms (with CUDA sync)"
        )

    def _warmup_whisper_feature(self):
        warmup_sr = 16000
        dummy_audio = np.zeros(warmup_sr, dtype=np.float32)
        _ = self.extract_whisper_feature(dummy_audio, warmup_sr)

    def prepare_material(self):
        """Prepare all materials needed for the digital avatar
        
        This method is the core of the first stage, mainly completes the following tasks:
        1. Save basic avatar info
        2. Process input video/image sequence
        3. Extract face features and bounding boxes
        4. Generate face masks
        5. Save all processed data
        """
        builtins.input = lambda prompt='': "y"
        try:
            self._prepare_material_impl()
        finally:
            builtins.input = _original_input

    def _prepare_material_impl(self):
        logger.info("preparing data materials ... ...")
        
        # Step 1: Save basic avatar config info
        with open(self.avatar_info_path, "w") as f:
            json.dump(self.avatar_info, f)

        # Step 2: Process input source (support video file or image sequence)
        if os.path.isfile(self.video_path):
            # If input is a video file, use video2imgs to extract frames
            video2imgs(self.video_path, self.full_imgs_path, ext='png')
        else:
            # If input is an image directory, copy all png images directly
            logger.info(f"copy files in {self.video_path}")
            files = os.listdir(self.video_path)
            files.sort()
            files = [file for file in files if file.split(".")[-1] == "png"]
            for filename in files:
                shutil.copyfile(f"{self.video_path}/{filename}", f"{self.full_imgs_path}/{filename}")
                
        # Get all input image paths and sort
        input_img_list = sorted(glob.glob(os.path.join(self.full_imgs_path, '*.[jpJP][pnPN]*[gG]')))

        # Step 3: Extract face landmarks and bounding boxes
        logger.info("extracting landmarks...")
        coord_list, frame_list = get_landmark_and_bbox(input_img_list, self.bbox_shift)
        
        # Step 4: Extract latent features
        input_latent_list = []
        idx = -1
        # coord_placeholder is used to mark invalid bounding boxes
        coord_placeholder = (0.0, 0.0, 0.0, 0.0)
        for bbox, frame in zip(coord_list, frame_list):
            idx = idx + 1
            if bbox == coord_placeholder:
                continue
            x1, y1, x2, y2 = bbox
            
            # Extra margin handling for v15 version
            if self.version == "v15":
                y2 = y2 + self.extra_margin  # Add extra chin area
                y2 = min(y2, frame.shape[0])  # Ensure not out of image boundary
                y1 = max(y1, 0) # Ensure not out of image boundary
                coord_list[idx] = [x1, y1, x2, y2]  # Update bbox in coord_list
                
            # Crop face region and resize to 256x256
            crop_frame = frame[y1:y2, x1:x2]
            resized_crop_frame = cv2.resize(crop_frame, (256, 256), interpolation=cv2.INTER_LANCZOS4)
            
            # Use VAE to extract latent features
            latents = self.vae.get_latents_for_unet(resized_crop_frame)
            input_latent_list.append(latents)

        # Step 5: Build cycle sequence (by forward + reverse order)
        self.frame_list_cycle = frame_list + frame_list[::-1]
        self.coord_list_cycle = coord_list + coord_list[::-1]
        self.input_latent_list_cycle = input_latent_list + input_latent_list[::-1]
        self.mask_coords_list_cycle = []
        self.mask_list_cycle = []

        # Step 6: Generate and save masks
        for i, frame in enumerate(tqdm(self.frame_list_cycle)):
            # Save processed frame
            cv2.imwrite(f"{self.full_imgs_path}/{str(i).zfill(8)}.png", frame)

            # Get current frame's face bbox
            x1, y1, x2, y2 = self.coord_list_cycle[i]
            
            # Select face parsing mode by version
            if self.version == "v15":
                mode = self.parsing_mode  # v15 supports different parsing modes
            else:
                mode = "raw"  # v1 only supports raw mode
                
            # Generate mask and crop box
            mask, crop_box = get_image_prepare_material(frame, [x1, y1, x2, y2], fp=self.fp, mode=mode)

            # Save mask and related info
            cv2.imwrite(f"{self.mask_out_path}/{str(i).zfill(8)}.png", mask)
            self.mask_coords_list_cycle += [crop_box]
            self.mask_list_cycle.append(mask)

        # Step 7: Save all processed data
        # Save mask coordinates
        with open(self.mask_coords_path, 'wb') as f:
            pickle.dump(self.mask_coords_list_cycle, f)

        # Save face coordinates
        with open(self.coords_path, 'wb') as f:
            pickle.dump(self.coord_list_cycle, f)

        # Save latent features
        torch.save(self.input_latent_list_cycle, self.latents_out_path)

        # Save frame data
        with open(self.frames_path, 'wb') as f:
            pickle.dump(self.frame_list_cycle, f)

        # Save mask data
        with open(self.masks_path, 'wb') as f:
            pickle.dump(self.mask_list_cycle, f)


    def acc_get_image_blending(self, image, face, face_box, mask_array, crop_box):
        """Blend generated face into the full frame in-place.

        IMPORTANT: caller must pass a *copy* of the original frame as `image`,
        because this method writes directly into `image` to avoid an extra
        full-frame allocation.
        """
        x, y, x1, y1 = face_box
        x_s, y_s, x_e, y_e = crop_box

        body_crop = image[y_s:y_e, x_s:x_e].copy()
        face_large1 = body_crop.copy()

        face_large1[y-y_s:y1-y_s, x-x_s:x1-x_s] = face

        mask_f = mask_array.astype(np.float32) * (1.0 / 255.0)
        mask_f = mask_f[:, :, np.newaxis]  # (H, W, 1) — broadcasts to 3-ch

        if face_large1.shape[:2] != mask_f.shape[:2]:
            min_h = min(face_large1.shape[0], mask_f.shape[0])
            min_w = min(face_large1.shape[1], mask_f.shape[1])
            face_large1 = face_large1[:min_h, :min_w]
            body_crop = body_crop[:min_h, :min_w]
            mask_f = mask_f[:min_h, :min_w]

        blended = (face_large1 * mask_f + body_crop * (1.0 - mask_f)).astype(np.uint8)

        image[y_s:y_e, x_s:x_e] = blended
        return image

    def res2combined(self, res_frame, idx):
        """Blend the generated frame with the original frame
        Args:
            res_frame: Generated frame (numpy array)
            idx: Current frame index
        Returns:
            numpy.ndarray: Blended full frame
        """
        debug = self.debug
        t0 = time.time()

        cycle_idx = idx % len(self.coord_list_cycle)
        bbox = self.coord_list_cycle[cycle_idx]
        ori_frame = self.frame_list_cycle[cycle_idx].copy()

        if debug:
            t1 = time.time()

        x1, y1, x2, y2 = bbox
        try:
            res_frame = cv2.resize(res_frame.astype(np.uint8), (x2 - x1, y2 - y1))
        except Exception as e:
            logger.opt(exception=True).error(f"res2combined error: {str(e)}")
            return ori_frame

        if debug:
            t2 = time.time()

        if not np.any(res_frame):
            logger.warning(f"res2combined: res_frame is all zero, return ori_frame, idx={idx}")
            return ori_frame

        mask = self.mask_list_cycle[cycle_idx]
        mask_crop_box = self.mask_coords_list_cycle[cycle_idx]

        if debug:
            t3 = time.time()

        combine_frame = self.acc_get_image_blending(ori_frame, res_frame, bbox, mask, mask_crop_box)

        t4 = time.time()
        total_time = t4 - t0
        fps = 1.0 / total_time if total_time > 0 else 0
        if fps < self.fps:
            logger.warning(f"[PROFILE] res2combined fps is not enough, fps={fps:.2f}, self.fps={self.fps}")
        if debug:
            logger.info(
                f"[PROFILE] res2combined: idx={idx}, ori_copy={t1-t0:.4f}s, resize={t2-t1:.4f}s, mask_fetch={t3-t2:.4f}s, blend={t4-t3:.4f}s, total={total_time:.4f}s, fps={fps:.2f}"
            )
        return combine_frame
    
    @torch.no_grad()
    def extract_whisper_feature(self, segment: np.ndarray, sampling_rate: int) -> torch.Tensor:
        """
        Extract whisper features for a single audio segment.
        Thread-safe: protected by _inference_lock for multi-session GPU sharing.
        Return: whisper_chunks, shape: [num_frames, 50, 384]
        """
        with self._inference_lock:
            t0 = time.time()
            audio_feature = self.audio_processor.feature_extractor(
                segment,
                return_tensors="pt",
                sampling_rate=sampling_rate
            ).input_features
            if self.weight_dtype is not None:
                audio_feature = audio_feature.to(dtype=self.weight_dtype)
            whisper_chunks = self.audio_processor.get_whisper_chunk(
                [audio_feature],
                self.device,
                self.weight_dtype,
                self.whisper,
                len(segment),
                fps=self.fps,
                audio_padding_length_left=self.audio_padding_length_left,
                audio_padding_length_right=self.audio_padding_length_right,
            )
            t1 = time.time()
            if self.debug:
                logger.info(f"[PROFILE] extract_whisper_feature: duration={t1-t0:.4f}s, segment_len={len(segment)}, sampling_rate={sampling_rate}")
            return whisper_chunks

    @torch.no_grad()
    def generate_frame(self, whisper_chunk: torch.Tensor, idx: int) -> np.ndarray:
        """
        Generate a single frame based on whisper features and frame index.
        Thread-safe: protected by _inference_lock for multi-session GPU sharing.
        """
        with self._inference_lock:
            return self._generate_frame_impl(whisper_chunk, idx)

    def _generate_frame_impl(self, whisper_chunk: torch.Tensor, idx: int) -> np.ndarray:
        t0 = time.time()
        # Ensure whisper_chunk shape is (B, 50, 384)
        if whisper_chunk.ndim == 2:
            whisper_chunk = whisper_chunk.unsqueeze(0)
        t1 = time.time()
        latent = self.input_latent_list_cycle[idx % len(self.input_latent_list_cycle)]
        if latent.dim() == 3:
            latent = latent.unsqueeze(0)
        t2 = time.time()
        audio_feature = self.pe(whisper_chunk.to(self.device))
        t3 = time.time()
        latent = latent.to(device=self.device, dtype=self.unet.model.dtype)
        t4 = time.time()
        pred_latents = self.unet.model(
            latent,
            self.timesteps,
            encoder_hidden_states=audio_feature
        ).sample

        t5 = time.time()
        pred_latents = pred_latents.to(device=self.device, dtype=self.vae.vae.dtype)
        recon = self.vae.decode_latents(pred_latents)
        t6 = time.time()
        res_frame = recon[0]  # Only one frame, take the first
        combined_frame = self.res2combined(res_frame, idx)
        t7 = time.time()

        # Profile statistics, print average every 1 second
        if self.debug:
            if not hasattr(self, '_profile_stat'):
                self._profile_stat = {
                    'count': 0,
                    'sum': [0.0]*7,  # 7 stages
                    'last_time': time.time()
                }
            self._profile_stat['count'] += 1
            self._profile_stat['sum'][0] += t1-t0
            self._profile_stat['sum'][1] += t2-t1
            self._profile_stat['sum'][2] += t3-t2
            self._profile_stat['sum'][3] += t4-t3
            self._profile_stat['sum'][4] += t5-t4
            self._profile_stat['sum'][5] += t6-t5
            self._profile_stat['sum'][6] += t7-t0
            now = time.time()
            if now - self._profile_stat['last_time'] >= 1.0:
                cnt = self._profile_stat['count']
                avg = [s/cnt for s in self._profile_stat['sum']]
                logger.info(
                    f"[PROFILE_AVG] count={cnt} "
                    f"prep_whisper={avg[0]:.4f}s, "
                    f"prep_latent={avg[1]:.4f}s, "
                    f"pe={avg[2]:.4f}s, "
                    f"latent_to={avg[3]:.4f}s, "
                    f"unet={avg[4]:.4f}s, "
                    f"vae={avg[5]:.4f}s, "
                    f"total={avg[6]:.4f}s"
                )
                self._profile_stat['count'] = 0
                self._profile_stat['sum'] = [0.0]*7
                self._profile_stat['last_time'] = now
        return combined_frame

    def generate_idle_frame(self, idx: int) -> np.ndarray:
        """
        Generate an idle static frame (no inference, for avatar idle/no audio)
        """
        return self.frame_list_cycle[idx % len(self.frame_list_cycle)].copy()

    @torch.no_grad()
    def generate_frames(self, whisper_chunks: torch.Tensor, start_idx: int, batch_size: int) -> list:
        """
        Batch generate multiple frames based on whisper features and frame index.
        Thread-safe: protected by _inference_lock for multi-session GPU sharing.
        whisper_chunks: [B, 50, 384]
        start_idx: start frame index
        batch_size: batch size
        Return: List of (recon, idx) tuples, length is batch_size
        """
        with self._inference_lock:
            return self._generate_frames_impl(whisper_chunks, start_idx, batch_size)

    def _generate_frames_impl(self, whisper_chunks: torch.Tensor, start_idx: int, batch_size: int) -> list:
        t0 = time.time()
        # Ensure whisper_chunks shape is (B, 50, 384)
        if whisper_chunks.ndim == 2:
            whisper_chunks = whisper_chunks.unsqueeze(0)
        elif whisper_chunks.ndim == 3 and whisper_chunks.shape[0] == 1:
            pass
        B = whisper_chunks.shape[0]
        if B != batch_size:
            logger.error(f"whisper_chunks.shape[0] ({B}) != batch_size ({batch_size})")
            return [(np.zeros((256, 256, 3), dtype=np.uint8), start_idx + i) for i in range(batch_size)]
        idx_list = [start_idx + i for i in range(batch_size)]
        latent_list = []
        t1 = time.time()
        for idx in idx_list:
            latent = self.input_latent_list_cycle[idx % len(self.input_latent_list_cycle)]
            if latent.dim() == 3:
                latent = latent.unsqueeze(0)
            latent_list.append(latent)
        latent_batch = torch.cat(latent_list, dim=0)  # [B, ...]
        t2 = time.time()
        audio_feature = self.pe(whisper_chunks.to(self.device))
        t3 = time.time()
        latent_batch = latent_batch.to(device=self.device, dtype=self.unet.model.dtype)
        t4 = time.time()
        pred_latents = self.unet.model(
            latent_batch,
            self.timesteps,
            encoder_hidden_states=audio_feature
        ).sample
        t5 = time.time()
        pred_latents = pred_latents.to(device=self.device, dtype=self.vae.vae.dtype)
        recon = self.vae.decode_latents(pred_latents)
        t6 = time.time()
        avg_time = (t6 - t0) / B if B > 0 else 0.0
        fps = 1.0 / avg_time if avg_time > 0 else 0.0
        if self.debug:
            logger.info(
                f"[PROFILE] generate_frames: start_idx={start_idx}, batch_size={batch_size}, "
                f"prep_whisper={t1-t0:.4f}s, prep_latent={t2-t1:.4f}s, pe={t3-t2:.4f}s, "
                f"latent_to={t4-t3:.4f}s, unet={t5-t4:.4f}s, vae={t6-t5:.4f}s, total={t6-t0:.4f}s, total_per_frame={avg_time:.4f}s, fps={fps:.2f}"
            )
            # debug for nan value
            logger.info(f"latent_batch stats: min={latent_batch.min().item()}, max={latent_batch.max().item()}, mean={latent_batch.mean().item()}, nan_count={(torch.isnan(latent_batch).sum().item() if torch.isnan(latent_batch).any() else 0)}")
            logger.info(f"pred_latents stats: min={pred_latents.min().item()}, max={pred_latents.max().item()}, mean={pred_latents.mean().item()}, nan_count={(torch.isnan(pred_latents).sum().item() if torch.isnan(pred_latents).any() else 0)}")
            if isinstance(recon, np.ndarray):
                logger.info(f"recon stats: min={recon.min()}, max={recon.max()}, mean={recon.mean()}, nan_count={np.isnan(recon).sum()}")
            elif isinstance(recon, torch.Tensor):
                logger.info(f"recon stats: min={recon.min().item()}, max={recon.max().item()}, mean={recon.mean().item()}, nan_count={(torch.isnan(recon).sum().item() if torch.isnan(recon).is_floating_point() else 0)}")
            else:
                logger.info(f"recon type: {type(recon)}")
        return [(recon[i], idx_list[i]) for i in range(B)]

    @torch.no_grad()
    def generate_frames_unet(self, whisper_chunks: torch.Tensor, start_idx: int, batch_size: int):
        """
        Batch UNet-only stage: whisper features -> pred_latents.
        Thread-safe: protected by _inference_lock for multi-session GPU sharing.
        Returns: (pred_latents, idx_list)
        """
        with self._inference_lock:
            return self._generate_frames_unet_impl(whisper_chunks, start_idx, batch_size)

    def _generate_frames_unet_impl(self, whisper_chunks: torch.Tensor, start_idx: int, batch_size: int):
        t0 = time.time()
        if whisper_chunks.ndim == 2:
            whisper_chunks = whisper_chunks.unsqueeze(0)
        B = whisper_chunks.shape[0]
        if B != batch_size:
            logger.error(f"whisper_chunks.shape[0] ({B}) != batch_size ({batch_size})")
            return torch.zeros((batch_size, 4, 32, 32), dtype=self.unet.model.dtype, device=self.device), [start_idx + i for i in range(batch_size)]
        idx_list = [start_idx + i for i in range(batch_size)]
        latent_list = []
        t1 = time.time()
        for idx in idx_list:
            latent = self.input_latent_list_cycle[idx % len(self.input_latent_list_cycle)]
            if latent.dim() == 3:
                latent = latent.unsqueeze(0)
            latent_list.append(latent)
        latent_batch = torch.cat(latent_list, dim=0)
        t2 = time.time()
        audio_feature = self.pe(whisper_chunks.to(self.device))
        t3 = time.time()
        latent_batch = latent_batch.to(device=self.device, dtype=self.unet.model.dtype)
        t4 = time.time()
        pred_latents = self.unet.model(
            latent_batch,
            self.timesteps,
            encoder_hidden_states=audio_feature
        ).sample
        t5 = time.time()
        if self.debug:
            avg_time = (t5 - t0) / B if B > 0 else 0.0
            logger.info(
                f"[PROFILE] generate_frames_unet: start_idx={start_idx}, batch_size={batch_size}, "
                f"prep_whisper={t1-t0:.4f}s, prep_latent={t2-t1:.4f}s, pe={t3-t2:.4f}s, "
                f"latent_to={t4-t3:.4f}s, unet={t5-t4:.4f}s, total={t5-t0:.4f}s, total_per_frame={avg_time:.4f}s"
            )
        return pred_latents, idx_list

    @torch.no_grad()
    def generate_frames_vae(self, pred_latents: torch.Tensor, idx_list: list, batch_size: int) -> list:
        """
        Batch VAE decode stage: pred_latents -> face crops.
        Thread-safe: protected by _inference_lock for multi-session GPU sharing.
        Returns: List of (recon, idx) tuples
        """
        with self._inference_lock:
            return self._generate_frames_vae_impl(pred_latents, idx_list, batch_size)

    def _generate_frames_vae_impl(self, pred_latents: torch.Tensor, idx_list: list, batch_size: int) -> list:
        t0 = time.time()
        B = pred_latents.shape[0]
        if B != batch_size:
            logger.error(f"pred_latents.shape[0] ({B}) != batch_size ({batch_size})")
            return [(np.zeros((256, 256, 3), dtype=np.uint8), idx_list[0] + i) for i in range(batch_size)]
        pred_latents = pred_latents.to(device=self.device, dtype=self.vae.vae.dtype)
        recon = self.vae.decode_latents(pred_latents)
        t1 = time.time()
        if self.debug:
            avg_time = (t1 - t0) / B if B > 0 else 0.0
            logger.info(
                f"[PROFILE] generate_frames_vae: start_idx={idx_list[0]}, batch_size={batch_size}, "
                f"vae={t1-t0:.4f}s, total_per_frame={avg_time:.4f}s"
            )
        return [(recon[i], idx_list[i]) for i in range(B)]

    @torch.no_grad()
    def offline_inference(self, audio_path: str, output_path: str, fps: int = None):
        """Offline synthesis: read a complete audio file, generate video and save to file.

        Uses the same pipeline as realtime inference:
        - Full audio whisper feature extraction (no 1s segmentation)
        - Same UNet+VAE inference via generate_frames()
        - Same blending via res2combined() (pre-computed mask + acc_get_image_blending)

        This produces output using the identical compositing path as realtime,
        enabling direct A/B comparison of audio processing differences only.

        Args:
            audio_path: Input audio file path
            output_path: Output video file path (e.g. "output/result.mp4")
            fps: Video frame rate (default: self.fps)
        """
        if fps is None:
            fps = self.fps

        tmp_dir = os.path.join(self.avatar_path, 'tmp_offline')
        os.makedirs(tmp_dir, exist_ok=True)

        # --- Stage 1: Full-audio whisper feature extraction ---
        t_start = time.time()
        whisper_input_features, librosa_length = self.audio_processor.get_audio_feature(
            audio_path,
            weight_dtype=self.weight_dtype
        )
        whisper_chunks = self.audio_processor.get_whisper_chunk(
            whisper_input_features,
            self.device,
            self.weight_dtype,
            self.whisper,
            librosa_length,
            fps=fps,
            audio_padding_length_left=self.audio_padding_length_left,
            audio_padding_length_right=self.audio_padding_length_right,
        )
        video_num = len(whisper_chunks)
        logger.info(f"[offline] Audio feature extraction: {audio_path}, "
                     f"{(time.time() - t_start) * 1000:.1f}ms, {video_num} frames")

        # --- Stage 2: Batch UNet + VAE inference (same pipeline as realtime) ---
        t_infer = time.time()
        res_frame_list = []
        batch_size = self.batch_size
        for batch_start in tqdm(range(0, video_num, batch_size), desc="Inference"):
            batch_end = min(batch_start + batch_size, video_num)
            actual_batch = batch_end - batch_start
            whisper_batch = whisper_chunks[batch_start:batch_end]
            if isinstance(whisper_batch, torch.Tensor) and whisper_batch.shape[0] < batch_size:
                pad_size = batch_size - whisper_batch.shape[0]
                whisper_batch = torch.cat([
                    whisper_batch,
                    torch.zeros(pad_size, *whisper_batch.shape[1:],
                                dtype=whisper_batch.dtype, device=whisper_batch.device)
                ], dim=0)
            recon_idx_list = self.generate_frames(whisper_batch, batch_start, whisper_batch.shape[0])
            for i in range(actual_batch):
                res_frame_list.append(recon_idx_list[i][0])

        logger.info(f"[offline] Inference: {video_num} frames in {time.time() - t_infer:.2f}s")

        # --- Stage 3: Blending via res2combined (same as realtime) ---
        t_blend = time.time()
        for i, res_frame in enumerate(tqdm(res_frame_list, desc="Blending")):
            combine_frame = self.res2combined(res_frame, i)
            cv2.imwrite(f"{tmp_dir}/{str(i).zfill(8)}.png", combine_frame)

        logger.info(f"[offline] Blending: {video_num} frames in {time.time() - t_blend:.2f}s")

        # --- Stage 4: ffmpeg encode ---
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        temp_video = os.path.join(self.avatar_path, "temp_offline.mp4")
        cmd_img2video = (f"ffmpeg -y -v warning -r {fps} -f image2 "
                         f"-i {tmp_dir}/%08d.png -vcodec libx264 "
                         f"-vf format=yuv420p -crf 18 {temp_video}")
        logger.info(cmd_img2video)
        os.system(cmd_img2video)

        cmd_combine = f"ffmpeg -y -v warning -i {audio_path} -i {temp_video} {output_path}"
        logger.info(cmd_combine)
        os.system(cmd_combine)

        os.remove(temp_video)
        shutil.rmtree(tmp_dir)
        total_time = time.time() - t_start
        logger.info(f"[offline] Done: {output_path} ({video_num} frames, {total_time:.2f}s total)")


def _collect_audio_files(audio_dir: str) -> list:
    """Collect and sort audio files from a directory."""
    audio_files = []
    for ext in ['*.wav', '*.mp3']:
        audio_files.extend(glob.glob(os.path.join(audio_dir, ext)))
    audio_files.sort()
    return audio_files


def _find_musetalk_handler_config(yaml_path: str) -> dict:
    """Load YAML config and find the MuseTalk handler config section.

    Searches handler_configs for a handler whose 'module' field contains 'musetalk'.
    This matches the same config section used by the realtime inference pipeline.
    """
    import yaml
    with open(yaml_path, 'r') as f:
        config = yaml.safe_load(f)

    handler_configs = config.get('default', {}).get('chat_engine', {}).get('handler_configs', {})

    for name, cfg in handler_configs.items():
        module = cfg.get('module', '')
        if 'musetalk' in module.lower():
            logger.info(f"Found MuseTalk handler config: [{name}]")
            return cfg

    raise ValueError(f"No MuseTalk handler config found in {yaml_path}")


def _create_avatar_from_config(handler_cfg: dict, gpu_id: int = 0,
                                batch_size_override: int = None,
                                force_preparation: bool = None) -> MuseTalkAlgoV15:
    """Create MuseTalkAlgoV15 from handler config dict.

    Replicates the same parameter derivation logic as avatar_handler_musetalk.py load(),
    ensuring offline test uses identical avatar configuration as realtime inference.
    """
    import hashlib

    fps = handler_cfg.get('fps', 25)
    batch_size = batch_size_override if batch_size_override is not None else handler_cfg.get('batch_size', 5)
    avatar_video_path = handler_cfg.get('avatar_video_path', '')
    avatar_model_dir = handler_cfg.get('avatar_model_dir', 'models/musetalk/avatar_model')
    force_create = force_preparation if force_preparation is not None else handler_cfg.get('force_create_avatar', False)
    debug = handler_cfg.get('debug', False)
    model_dir_rel = handler_cfg.get('model_dir', 'models/musetalk')

    project_root = os.getcwd()
    model_dir = os.path.join(project_root, model_dir_rel)
    vae_type = "sd-vae"
    unet_model_path = os.path.join(model_dir, "musetalkV15", "unet.pth")
    unet_config = os.path.join(model_dir, "musetalkV15", "musetalk.json")
    whisper_dir = os.path.join(model_dir, "whisper")
    result_dir = os.path.join(project_root, avatar_model_dir)

    video_basename = os.path.splitext(os.path.basename(avatar_video_path))[0]
    video_hash = hashlib.md5(avatar_video_path.encode()).hexdigest()[:8]
    auto_avatar_id = f"avatar_{video_basename}_{video_hash}"
    logger.info(f"Auto generated avatar_id: {auto_avatar_id}")

    return MuseTalkAlgoV15(
        avatar_id=auto_avatar_id,
        video_path=avatar_video_path,
        bbox_shift=0,
        batch_size=batch_size,
        force_preparation=force_create,
        parsing_mode="jaw",
        left_cheek_width=90, right_cheek_width=90,
        audio_padding_length_left=2, audio_padding_length_right=2,
        fps=fps,
        version="v15",
        result_dir=result_dir,
        extra_margin=10,
        vae_type=vae_type,
        unet_model_path=unet_model_path,
        unet_config=unet_config,
        whisper_dir=whisper_dir,
        gpu_id=gpu_id,
        debug=debug,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="MuseTalk Offline Synthesis - uses the same YAML config as realtime inference",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples (run from project root):
  # Smoke test script
  ./tests/inttest/musetalk/run_offline_smoke.sh

  # Single audio file
  python src/handlers/avatar/musetalk/musetalk_algo.py \\
      --config config/chat_with_openai_compatible_bailian_cosyvoice_musetalk_duplex.yaml \\
      --audio_path tests/inttest/musetalk/assets/audio/test-audio-1.wav \\
      --output_dir tests/inttest/musetalk/outputs/offline

  # Override batch size for faster offline processing
  python src/handlers/avatar/musetalk/musetalk_algo.py \\
      --config config/chat_with_openai_compatible_bailian_cosyvoice_musetalk_duplex.yaml \\
      --audio_path tests/inttest/musetalk/assets/audio/test-audio-1.wav \\
      --output_dir tests/inttest/musetalk/outputs/offline --batch_size 20
""")

    parser.add_argument("--config", type=str, required=True,
                        help="Path to YAML config file (same as realtime inference)")
    parser.add_argument("--audio_path", type=str, default=None,
                        help="Single audio file to synthesize")
    parser.add_argument("--audio_dir", type=str, default=None,
                        help="Directory of audio files to batch synthesize")
    parser.add_argument("--output_dir", type=str, default=None,
                        help="Output directory (default: avatar vid_output dir)")
    parser.add_argument("--batch_size", type=int, default=None,
                        help="Override batch size from config (offline can use larger batches, e.g. 20)")
    parser.add_argument("--gpu_id", type=int, default=0,
                        help="GPU device id (default: 0)")
    parser.add_argument("--force_preparation", action='store_true', default=None,
                        help="Force regenerate avatar preparation data")

    args = parser.parse_args()

    if args.audio_path is None and args.audio_dir is None:
        parser.error("Must specify --audio_path or --audio_dir")

    handler_cfg = _find_musetalk_handler_config(args.config)

    logger.info(f"Loaded config from: {args.config}")
    for k, v in handler_cfg.items():
        if k == 'module':
            continue
        logger.info(f"  {k}: {v}")
    if args.batch_size is not None:
        logger.info(f"  [override] batch_size: {args.batch_size}")
    if args.force_preparation:
        logger.info(f"  [override] force_preparation: True")

    avatar = _create_avatar_from_config(
        handler_cfg,
        gpu_id=args.gpu_id,
        batch_size_override=args.batch_size,
        force_preparation=args.force_preparation,
    )
    output_dir = args.output_dir or avatar.video_out_path
    os.makedirs(output_dir, exist_ok=True)

    if args.audio_path:
        audio_files = [args.audio_path]
    else:
        audio_files = _collect_audio_files(args.audio_dir)

    if not audio_files:
        logger.error("No audio files found")
        sys.exit(1)

    fps = handler_cfg.get('fps', 25)
    logger.info(f"Processing {len(audio_files)} audio file(s), fps={fps}, output_dir={output_dir}")

    for audio_path in audio_files:
        audio_name = os.path.splitext(os.path.basename(audio_path))[0]
        output_path = os.path.join(output_dir, f"{audio_name}_offline.mp4")
        logger.info(f"\nProcessing: {audio_path} -> {output_path}")
        try:
            avatar.offline_inference(
                audio_path=audio_path,
                output_path=output_path,
                fps=fps,
            )
        except Exception as e:
            logger.opt(exception=True).error(f"Error processing {audio_path}: {e}")
            continue

