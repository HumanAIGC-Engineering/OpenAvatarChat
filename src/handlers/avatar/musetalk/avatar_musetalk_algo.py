import os
import torch
import numpy as np
import cv2
from typing import Optional, Tuple, List
import queue
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
from pydantic import BaseModel
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

from handlers.avatar.liteavatar.model.audio_input import SpeechAudio
from handlers.avatar.musetalk.musetalk_utils_preprocessing import get_landmark_and_bbox

# Now you can correctly import MuseTalk modules
from musetalk.utils.face_parsing import FaceParsing
from musetalk.utils.utils import datagen, load_all_model
from musetalk.utils.blending import get_image_prepare_material, get_image_blending
from musetalk.utils.audio_processor import AudioProcessor

builtins.input = lambda prompt='': "y"

def video2imgs(vid_path, save_path, ext='.png', cut_frame=10000000):
    cap = cv2.VideoCapture(vid_path)
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

def osmakedirs(path_list):
    for path in path_list:
        os.makedirs(path) if not os.path.exists(path) else None

class MuseAvatarV15:
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
        """Initialize MuseAvatarV15
        
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
            vae_model_dir (str): VAE model directory
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
            self.input_latent_list_cycle = torch.load(self.latents_out_path)
            with open(self.coords_path, 'rb') as f:
                self.coord_list_cycle = pickle.load(f)
            with open(self.frames_path, 'rb') as f:
                self.frame_list_cycle = pickle.load(f)
            with open(self.mask_coords_path, 'rb') as f:
                self.mask_coords_list_cycle = pickle.load(f)
            with open(self.masks_path, 'rb') as f:
                self.mask_list_cycle = pickle.load(f)

        # Warm up models is only needed in current thread
        # logger.info("Warming up models...")
        # self._warmup_models()
        # logger.info("Warmup complete")

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

    def res2combined(self, res_frame, idx):
        """Blend the generated frame with the original frame
        Args:
            res_frame: Generated frame (numpy array)
            idx: Current frame index
        Returns:
            numpy.ndarray: Blended full frame
        """
        t0 = time.time()
        # Get the face bbox and original frame for the current frame
        bbox = self.coord_list_cycle[idx % len(self.coord_list_cycle)]
        ori_frame = copy.deepcopy(self.frame_list_cycle[idx % len(self.frame_list_cycle)])
        t1 = time.time()
        x1, y1, x2, y2 = bbox
        try:
            # Resize the generated frame to face region size
            res_frame = cv2.resize(res_frame.astype(np.uint8), (x2 - x1, y2 - y1))
        except Exception as e:
            logger.opt(exception=True).error(f"res2combined error: {str(e)}")
            return ori_frame
        t2 = time.time()
        # Add protection: if res_frame is all zeros, return original frame directly
        if np.all(res_frame == 0):
            # if self.debug:
            logger.warning(f"res2combined: res_frame is all zero, return ori_frame, idx={idx}")
            return ori_frame
        # Get the corresponding mask and crop box
        mask = self.mask_list_cycle[idx % len(self.mask_list_cycle)]
        mask_crop_box = self.mask_coords_list_cycle[idx % len(self.mask_coords_list_cycle)]
        t3 = time.time()
        # Blend the generated facial expression with the original frame
        combine_frame = get_image_blending(ori_frame, res_frame, bbox, mask, mask_crop_box)
        t4 = time.time()
        if self.debug:
            logger.info(
                f"[PROFILE] res2combined: idx={idx}, ori_copy={t1-t0:.4f}s, resize={t2-t1:.4f}s, mask_fetch={t3-t2:.4f}s, blend={t4-t3:.4f}s, total={t4-t0:.4f}s"
            )
        return combine_frame
    
    def extract_whisper_feature(self, segment: np.ndarray, sampling_rate: int) -> torch.Tensor:
        """
        Extract whisper features for a single audio segment
        """
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
        return whisper_chunks  # shape: [num_frames, 50, 384]

    @torch.no_grad()
    def generate_frame(self, whisper_chunk: torch.Tensor, idx: int) -> np.ndarray:
        """
        Generate a frame based on whisper features and frame index
        """
        import time
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
        # Directly return a frame from the original frame cycle
        frame = self.frame_list_cycle[idx % len(self.frame_list_cycle)]
        return frame

    @torch.no_grad()
    def generate_frames(self, whisper_chunks: torch.Tensor, start_idx: int, batch_size: int) -> list:
        """
        Batch generate multiple frames based on whisper features and frame index
        whisper_chunks: [B, 50, 384]
        start_idx: start frame index
        batch_size: batch size
        Return: List of (recon, idx) tuples, length is batch_size
        """
        t0 = time.time()
        # Ensure whisper_chunks shape is (B, 50, 384)
        if whisper_chunks.ndim == 2:
            whisper_chunks = whisper_chunks.unsqueeze(0)
        elif whisper_chunks.ndim == 3 and whisper_chunks.shape[0] == 1:
            pass
        B = whisper_chunks.shape[0]
        assert B == batch_size, f"whisper_chunks.shape[0] ({B}) != batch_size ({batch_size})"
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
        # # Force set pred_latents to all nan for debugging： unet get nan value
        # pred_latents[:] = float('nan')
        t5 = time.time()
        pred_latents = pred_latents.to(device=self.device, dtype=self.vae.vae.dtype)
        recon = self.vae.decode_latents(pred_latents)
        t6 = time.time()
        avg_time = (t6 - t0) / B if B > 0 else 0.0
        if self.debug:
            logger.info(
                f"[PROFILE] generate_frames: start_idx={start_idx}, batch_size={batch_size}, "
                f"prep_whisper={t1-t0:.4f}s, prep_latent={t2-t1:.4f}s, pe={t3-t2:.4f}s, "
                f"latent_to={t4-t3:.4f}s, unet={t5-t4:.4f}s, vae={t6-t5:.4f}s, total={t6-t0:.4f}s, total_per_frame={avg_time:.4f}s"
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
    def inference(self, audio_path, out_vid_name, fps, skip_save_images):
        """Inference to generate talking avatar video
        
        Args:
            audio_path: Input audio file path
            out_vid_name: Output video name (based on audio file name)
            fps: Video frame rate
            skip_save_images: Whether to skip saving intermediate frame images
        """
        # Create temp directory for generated frames
        tmp_dir = os.path.join(self.avatar_path, 'tmp')
        os.makedirs(tmp_dir, exist_ok=True)
        logger.info("start inference")

        ############################################## Stage 1: Audio feature extraction ##############################################
        start_time = time.time()
        # Use Whisper to extract audio features
        whisper_input_features, librosa_length = self.audio_processor.get_audio_feature(
            audio_path, 
            weight_dtype=self.weight_dtype
        )
        # Chunk audio features
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
        logger.info(f"processing audio:{audio_path} costs {(time.time() - start_time) * 1000}ms")

        ############################################## Stage 2: Batch generation ##############################################
        # Calculate total number of frames to generate
        video_num = len(whisper_chunks)
        # Create result frame queue for multithreaded processing
        res_frame_queue = queue.Queue()
        self.idx = 0

        # Create processing thread
        process_thread = threading.Thread(
            target=self.process_frames, 
            args=(res_frame_queue, video_num, skip_save_images)
        )
        process_thread.start()

        # Create data generator for batch processing
        gen = datagen(
            whisper_chunks,
            self.input_latent_list_cycle,
            self.batch_size
        )
        
        start_time = time.time()

        # Batch generate facial expressions
        for i, (whisper_batch, latent_batch) in enumerate(tqdm(gen, total=int(np.ceil(float(video_num) / self.batch_size)))):
            # 1. Process audio features
            audio_feature_batch = self.pe(whisper_batch.to(self.device))
            # 2. Prepare latent features
            latent_batch = latent_batch.to(device=self.device, dtype=self.unet.model.dtype)

            # 3. Use UNet to generate facial expressions
            pred_latents = self.unet.model(
                latent_batch,
                self.timesteps,
                encoder_hidden_states=audio_feature_batch
            ).sample
            
            # 4. Decode generated latent features
            pred_latents = pred_latents.to(device=self.device, dtype=self.vae.vae.dtype)
            recon = self.vae.decode_latents(pred_latents)
            
            # 5. Put generated frames into queue
            for res_frame in recon:
                res_frame_queue.put(res_frame)

        # Wait for processing thread to finish
        process_thread.join()

        ############################################## Stage 3: Post-processing ##############################################
        # Output processing time statistics
        if skip_save_images:
            logger.info('Total process time of {} frames without saving images = {}s'.format(
                video_num,
                time.time() - start_time))
        else:
            logger.info('Total process time of {} frames including saving images = {}s'.format(
                video_num,
                time.time() - start_time))

        # Save video if needed
        if out_vid_name is not None and not skip_save_images:
            # 1. Convert image sequence to video
            temp_video = os.path.join(self.avatar_path, "temp.mp4")
            cmd_img2video = f"ffmpeg -y -v warning -r {fps} -f image2 -i {tmp_dir}/%08d.png -vcodec libx264 -vf format=yuv420p -crf 18 {temp_video}"
            logger.info(cmd_img2video)
            os.system(cmd_img2video)

            # 2. Combine audio into video
            os.makedirs(self.video_out_path, exist_ok=True)
            output_vid = os.path.join(self.video_out_path, f"{out_vid_name}.mp4")
            cmd_combine_audio = f"ffmpeg -y -v warning -i {audio_path} -i {temp_video} {output_vid}"
            logger.info(cmd_combine_audio)
            os.system(cmd_combine_audio)

            # 3. Clean up temp files
            os.remove(temp_video)
            shutil.rmtree(tmp_dir)
            logger.info(f"Result saved to: {output_vid}")
        logger.info("\n")

    def process_frames(self, res_frame_queue, video_len, skip_save_images):
        """Process generated video frames
        
        This method runs in a separate thread and is responsible for processing generated video frames, including:
        1. Get generated frames from the queue
        2. Resize frames to match the original video
        3. Blend generated facial expressions with the original frame
        4. Save processed frames (if needed)
        
        Args:
            res_frame_queue: Queue for generated frames
            video_len: Total number of frames to process
            skip_save_images: Whether to skip saving intermediate frame images
        """
        logger.info(video_len)
        while True:
            # Exit if all frames have been processed
            if self.idx >= video_len - 1:
                break
                
            try:
                # Get generated frame from queue, 1s timeout
                start = time.time()
                res_frame = res_frame_queue.get(block=True, timeout=1)
            except queue.Empty:
                continue

            # Get the face bbox and original frame for the current frame
            bbox = self.coord_list_cycle[self.idx % (len(self.coord_list_cycle))]
            ori_frame = copy.deepcopy(self.frame_list_cycle[self.idx % (len(self.frame_list_cycle))])
            x1, y1, x2, y2 = bbox
            
            try:
                # Resize the generated frame to face region size
                res_frame = cv2.resize(res_frame.astype(np.uint8), (x2 - x1, y2 - y1))
            except:
                continue
                
            # Get the corresponding mask and crop box
            mask = self.mask_list_cycle[self.idx % (len(self.mask_list_cycle))]
            mask_crop_box = self.mask_coords_list_cycle[self.idx % (len(self.mask_coords_list_cycle))]
            
            # Blend the generated facial expression with the original frame
            combine_frame = get_image_blending(ori_frame, res_frame, bbox, mask, mask_crop_box)

            # Save processed frame if needed
            if skip_save_images is False:
                cv2.imwrite(f"{self.avatar_path}/tmp/{str(self.idx).zfill(8)}.png", combine_frame)
                
            self.idx = self.idx + 1

def read_audio_file(audio_path: str) -> Tuple[bytes, int]:
    """Read audio file and return byte stream and sample rate
    
    Args:
        audio_path: Audio file path
        
    Returns:
        Tuple[bytes, int]: (audio byte stream, sample rate)
    """
    try:
        # Use librosa to read audio file
        audio_data, sampling_rate = librosa.load(audio_path, sr=16000)  # Fixed sample rate 16kHz
        
        # Convert numpy array to byte stream
        audio_bytes = audio_data.astype(np.float32).tobytes()
        
        logger.info("Successfully read audio file: {}", audio_path)
        logger.info("Sample Rate: {}, Duration: {:.2f}s", sampling_rate, len(audio_data)/sampling_rate)
        
        return audio_bytes, sampling_rate
        
    except Exception as e:
        logger.error("Error reading audio file {}: {}", audio_path, str(e))
        return None, None


def run_batch_test(args):
    """Run batch audio test"""
    # Initialize digital avatar
    avatar = MuseAvatarV15(
        avatar_id=args.avatar_id,
        video_path=args.video_path,
        bbox_shift=args.bbox_shift,
        batch_size=args.batch_size,
        force_preparation=args.force_preparation,
        parsing_mode=args.parsing_mode,
        left_cheek_width=args.left_cheek_width,
        right_cheek_width=args.right_cheek_width,
        audio_padding_length_left=args.audio_padding_length_left,
        audio_padding_length_right=args.audio_padding_length_right,
        fps=args.fps,
        version=args.version,
        result_dir=args.result_dir,
        extra_margin=args.extra_margin,
        vae_model_dir=args.vae_model_dir,
        unet_model_path=args.unet_model_path,
        unet_config=args.unet_config,
        whisper_dir=args.whisper_dir,
        gpu_id=args.gpu_id
    )

    # Get all audio files in the audio directory
    audio_files = []
    for ext in ['*.wav', '*.mp3']:
        audio_files.extend(glob.glob(os.path.join(args.audio_dir, ext)))
    audio_files.sort()

    # Process each audio file
    for audio_path in audio_files:
        # Use audio file name as output video name
        audio_name = os.path.splitext(os.path.basename(audio_path))[0]
        
        logger.info(f"\nProcessing audio: {audio_path}")
        
        # Run inference
        avatar.inference(
            audio_path=audio_path,
            out_vid_name=audio_name,  # Use audio file name directly
            fps=args.fps,
            skip_save_images=args.skip_save_images
        )

def run_realtime_test(args):
    """Run real-time processing test, using pipeline to process audio
    
    Args:
        args: Command line arguments
    """
    import time

    # Initialize digital avatar
    avatar = MuseAvatarV15(
        avatar_id=args.avatar_id,
        video_path=args.video_path,
        bbox_shift=args.bbox_shift,
        batch_size=args.batch_size,
        force_preparation=args.force_preparation,
        parsing_mode=args.parsing_mode,
        left_cheek_width=args.left_cheek_width,
        right_cheek_width=args.right_cheek_width,
        audio_padding_length_left=args.audio_padding_length_left,
        audio_padding_length_right=args.audio_padding_length_right,
        fps=args.fps,
        version=args.version,
        result_dir=args.result_dir,
        extra_margin=args.extra_margin,
        vae_model_dir=args.vae_model_dir,
        unet_model_path=args.unet_model_path,
        unet_config=args.unet_config,
        whisper_dir=args.whisper_dir,
        gpu_id=args.gpu_id
    )

    # Get all audio files in the audio directory
    audio_files = []
    for ext in ['*.wav', '*.mp3']:
        audio_files.extend(glob.glob(os.path.join(args.audio_dir, ext)))
    audio_files.sort()

    # Process each audio file
    for audio_path in audio_files:
        try:
            # Read audio file
            audio_bytes, sample_rate = read_audio_file(audio_path)
            if audio_bytes is None or sample_rate is None:
                logger.error(f"Skip audio {audio_path}: failed to read")
                continue
                
            # Check audio length
            audio_data = np.frombuffer(audio_bytes, dtype=np.float32)
            duration = len(audio_data) / sample_rate                
            logger.info(f"\nProcessing audio: {audio_path} (duration: {duration:.2f}s)")
            
            # Add start time record
            start_time = time.time()
            
            # Create SpeechAudio object
            speech_audio = SpeechAudio(
                audio_data=audio_bytes,
                speech_id="1",
                end_of_speech=True,
                sample_rate=sample_rate
            )
            
            # Use real-time processing
            logger.info("Start real-time processing...")
            frames, audio_len = avatar.realtime_audio2image(speech_audio)
            logger.info(f"Real-time processing complete, generated {len(frames)} frames")
            
            # Save results
            if not args.skip_save_images:
                # Create temp directory
                tmp_dir = os.path.join(avatar.avatar_path, 'tmp')
                os.makedirs(tmp_dir, exist_ok=True)
                
                # Save frames
                logger.info("Saving video frames...")
                for i, frame in enumerate(frames):
                    cv2.imwrite(os.path.join(tmp_dir, f"{str(i).zfill(8)}.png"), frame)
                
                # Generate video
                temp_video = os.path.join(avatar.avatar_path, "temp.mp4")
                output_name = f"{os.path.splitext(os.path.basename(audio_path))[0]}_pipeline"  # Use pipeline suffix to indicate pipeline processing version
                output_vid = os.path.join(avatar.video_out_path, f"{output_name}.mp4")
                
                # 1. Convert image sequence to video
                logger.info("Generating video...")
                cmd_img2video = f"ffmpeg -y -v warning -r {args.fps} -f image2 -i {tmp_dir}/%08d.png -vcodec libx264 -vf format=yuv420p -crf 18 {temp_video}"
                logger.info(cmd_img2video)
                os.system(cmd_img2video)

                # 2. Combine audio into video
                os.makedirs(avatar.video_out_path, exist_ok=True)
                cmd_combine_audio = f"ffmpeg -y -v warning -i {audio_path} -i {temp_video} {output_vid}"
                logger.info(cmd_combine_audio)
                os.system(cmd_combine_audio)

                # 3. Clean up temp files
                os.remove(temp_video)
                shutil.rmtree(tmp_dir)
                logger.info(f"Result saved to: {output_vid}")

            process_time = time.time() - start_time
            logger.info(f'Processing complete, {len(frames)} frames in {process_time:.2f}s, average {len(frames)/process_time:.2f} fps')
            
        except Exception as e:
            logger.opt(exception=True).error(f"Error processing audio {audio_path}: {str(e)}")
            import traceback
            traceback.print_exc()
            continue

# Run main function
if __name__ == "__main__":
    parser.add_argument("--version", type=str, default="v15", choices=["v1", "v15"], help="MuseTalk version")
    parser.add_argument("--ffmpeg_path", type=str, default="./ffmpeg-4.4-amd64-static/", help="ffmpeg path")
    parser.add_argument("--gpu_id", type=int, default=0, help="GPU id")
    parser.add_argument("--vae_model_dir", type=str, default=None, help="VAE model directory")
    parser.add_argument("--unet_config", type=str, default=None, help="UNet config file path")
    parser.add_argument("--unet_model_path", type=str, default=None, help="UNet weights path")
    parser.add_argument("--whisper_dir", type=str, default=None, help="Whisper model directory")
    parser.add_argument("--bbox_shift", type=int, default=0, help="Face bbox offset")
    parser.add_argument("--result_dir", type=str, default='./results', help="Result output directory")
    parser.add_argument("--extra_margin", type=int, default=10, help="Face crop extra margin")
    parser.add_argument("--fps", type=int, default=25, help="Video frame rate")
    parser.add_argument("--audio_padding_length_left", type=int, default=2, help="Audio left padding")
    parser.add_argument("--audio_padding_length_right", type=int, default=2, help="Audio right padding")
    parser.add_argument("--batch_size", type=int, default=20, help="Inference batch size")
    parser.add_argument("--parsing_mode", type=str, default='jaw', help="Face fusion mode")
    parser.add_argument("--left_cheek_width", type=int, default=90, help="Left cheek width")
    parser.add_argument("--right_cheek_width", type=int, default=90, help="Right cheek width")
    parser.add_argument("--skip_save_images", action="store_true", help="Whether to skip saving images")
    parser.add_argument("--avatar_id", type=str, default="avator_2", help="Avatar ID")
    parser.add_argument("--force_preparation", type=lambda x: x.lower() == 'true', default=False, help="Whether to force data regeneration (True/False)")
    parser.add_argument("--video_path", type=str, default=os.path.join(musetalk_module_path, "data", "video", "sun.mp4"), help="Video path")
    parser.add_argument("--audio_dir", type=str, default=os.path.join(musetalk_module_path, "data", "audio"), help="Audio directory path")
    parser.add_argument("--test_mode", type=str, default="realtime", choices=["batch", "realtime"], help="Test mode: batch or realtime")

    args = parser.parse_args()

    # Automatically infer model and config file paths
    project_root = os.getcwd()
    model_dir = os.path.join(project_root, "models", "musetalk")
    if args.unet_model_path is None:
        args.unet_model_path = os.path.join(model_dir, "musetalkV15", "unet.pth")
    if args.unet_config is None:
        args.unet_config = os.path.join(model_dir, "musetalkV15", "musetalk.json")
    if args.whisper_dir is None:
        args.whisper_dir = os.path.join(model_dir, "whisper")
    if args.vae_model_dir is None:
        args.vae_model_dir = os.path.join(model_dir, "sd-vae")

    logger.info("Current config:")
    for arg in vars(args):
        logger.info(f"  {arg}: {getattr(args, arg)}")

    # Run different tests according to test mode
    if args.test_mode == "realtime":
        run_realtime_test(args)
    else:
        run_batch_test(args)


