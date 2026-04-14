"""Face detection and cropping utility for FlashHead handler.

Uses OpenCV Haar cascade for face detection, avoiding the dependency on
mediapipe.solutions which was removed in mediapipe >= 0.10.20.
"""
import os
import cv2
import numpy as np
from PIL import Image
from loguru import logger


def _detect_face_opencv(image_rgb: np.ndarray):
    """Detect the most prominent face using OpenCV Haar cascade.

    Returns (x1, y1, x2, y2) in absolute pixel coordinates, or None.
    """
    gray = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2GRAY)
    cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml",
    )
    faces = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    if len(faces) == 0:
        return None
    # Pick the largest face by area
    areas = [w * h for (_, _, w, h) in faces]
    idx = int(np.argmax(areas))
    x, y, w, h = faces[idx]
    return (x, y, x + w, y + h)


def crop_face(
    image_path: str,
    face_ratio: float = 2.0,
    target_size: tuple = (512, 512),
) -> Image.Image:
    """Detect and crop the face region from an image.

    Replicates the algorithm from SoulX-FlashHead's facecrop.process_image
    but uses OpenCV instead of mediapipe for face detection.

    Raises ValueError if the file does not exist or no face is detected.
    """
    if not os.path.isfile(image_path):
        raise ValueError(f"File not found: {image_path}")

    image = Image.open(image_path).convert("RGB")
    image_rgb = np.array(image)
    img_h, img_w = image_rgb.shape[:2]

    bbox = _detect_face_opencv(image_rgb)
    if bbox is None:
        raise ValueError(f"No face detected in {image_path}")

    x1, y1, x2, y2 = bbox
    center_x = (x1 + x2) / 2
    center_y = (y1 + y2) / 2
    width = x2 - x1

    new_width = width * face_ratio
    new_height = new_width

    # Vertical bias: 55% above center, 45% below (keeps forehead in frame)
    dis_x_left = new_width * 0.5
    dis_x_right = new_width - dis_x_left
    dis_y_up = new_height * 0.55
    dis_y_down = new_height - dis_y_up

    crop_box = (
        int(max(0, center_x - dis_x_left)),
        int(max(0, center_y - dis_y_up)),
        int(min(img_w, center_x + dis_x_right)),
        int(min(img_h, center_y + dis_y_down)),
    )

    cropped = image.crop(crop_box).resize(target_size)
    logger.info(
        f"Face crop succeeded: bbox={bbox}, crop_region={crop_box}, "
        f"result={cropped.size}"
    )
    return cropped
