import base64
import io
import time
import uuid
from typing import Any, Dict, Optional, List

import numpy as np
from loguru import logger

from chat_engine.data_models.chat_data.chat_data_model import ChatData
from chat_engine.data_models.chat_data_type import ChatDataType
from chat_engine.data_models.chat_signal import ChatSignal
from chat_engine.data_models.chat_stream import ChatStreamIdentity
from .data_tool_models import DataToolConfig, DataToolContext
from service.manager_service.manager_service_register import get_data_tool_base_dir


def stream_to_dict(stream: Optional[ChatStreamIdentity]):
    if stream is None:
        return None
    return {
        "data_type": stream.data_type.value,
        "builder_id": int(stream.builder_id),
        "stream_id": int(stream.stream_id),
        "name": stream.name,
        "producer": stream.producer_name,
    }


def safe_value(value: Any):
    if isinstance(value, np.generic):
        return value.item()
    return value


def safe_obj(obj: Any):
    if isinstance(obj, dict):
        return {str(k): safe_obj(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [safe_obj(v) for v in obj]
    return safe_value(obj)


def encode_preview(array: np.ndarray, limit: int):
    if limit <= 0:
        return None
    try:
        preview_bytes = array.tobytes()[:limit]
        if not preview_bytes:
            return None
        return base64.b64encode(preview_bytes).decode("ascii")
    except Exception:
        return None


def to_int16_audio(array: np.ndarray):
    audio_np = np.asarray(array)
    if audio_np.ndim > 1:
        audio_np = audio_np.reshape(-1)
    if audio_np.dtype != np.int16:
        if np.issubdtype(audio_np.dtype, np.floating):
            audio_np = np.clip(audio_np, -1.0, 1.0)
            audio_np = (audio_np * 32767.0).astype(np.int16)
        else:
            audio_np = audio_np.astype(np.int16)
    return audio_np


def write_binary_file(session_id: str, suffix: str, content: bytes) -> Optional[str]:
    try:
        base_dir = get_data_tool_base_dir()
        target_dir = base_dir / session_id
        target_dir.mkdir(parents=True, exist_ok=True)
        filename = f"{int(time.time() * 1000)}_{uuid.uuid4().hex}{suffix}"
        file_path = target_dir / filename
        file_path.write_bytes(content)
        return str(file_path.relative_to(base_dir))
    except Exception as e:
        logger.warning(f"Failed to write data_tool file: {e}")
        return None


def dump_audio_to_file(session_id: str, main_data: np.ndarray, sample_rate: Optional[int], channels: Optional[int]):
    audio_np = to_int16_audio(main_data)
    sample_rate = sample_rate or 16000
    channels = channels or 1
    import wave

    buffer = io.BytesIO()
    with wave.open(buffer, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(2)  # int16
        wf.setframerate(sample_rate)
        wf.writeframes(audio_np.tobytes())
    return write_binary_file(session_id, ".wav", buffer.getvalue())


def dump_image_to_file(session_id: str, main_data: np.ndarray):
    array = np.asarray(main_data)
    if array.ndim == 3 and array.shape[2] in (1, 3, 4):
        try:
            from PIL import Image  # type: ignore

            mode = "L" if array.shape[2] == 1 else "RGB" if array.shape[2] == 3 else "RGBA"
            img = Image.fromarray(array.astype(np.uint8), mode=mode)
            buffer = io.BytesIO()
            img.save(buffer, format="PNG")
            return write_binary_file(session_id, ".png", buffer.getvalue())
        except Exception as e:
            logger.warning(f"PIL save failed, fallback to npy: {e}")
    try:
        with io.BytesIO() as buffer:
            np.save(buffer, array)
            return write_binary_file(session_id, ".npy", buffer.getvalue())
    except Exception as e:
        logger.warning(f"Numpy save failed: {e}")
        return None


def extract_frame(array: np.ndarray) -> Optional[np.ndarray]:
    arr = np.asarray(array)
    if arr.ndim == 4:
        return arr[0]
    if arr.ndim == 3:
        return arr
    if arr.ndim == 2:
        return arr[..., np.newaxis]
    return None


def concat_audio(arrays: List[np.ndarray]) -> np.ndarray:
    if len(arrays) == 1:
        return arrays[0]
    shapes = [arr.shape for arr in arrays if arr is not None]
    if not shapes:
        return arrays[0]
    max_channels = max(s[0] if len(s) > 1 else 1 for s in shapes)
    processed = []
    for arr in arrays:
        if arr is None:
            continue
        arr_np = np.asarray(arr)
        if arr_np.ndim == 1:
            arr_np = arr_np[np.newaxis, ...]
        if arr_np.shape[0] != max_channels:
            if arr_np.shape[0] == 1 and max_channels > 1:
                arr_np = np.repeat(arr_np, max_channels, axis=0)
            else:
                arr_np = arr_np[:max_channels]
        processed.append(arr_np)
    return np.concatenate(processed, axis=-1)


def stream_key(chat_data: ChatData) -> Optional[str]:
    if chat_data.stream_id is not None:
        key = chat_data.stream_id
        if key is not None:
            return f"{key.builder_id}_{key.stream_id}"
    return None


def build_chat_data_event(
    context: DataToolContext,
    chat_data: ChatData,
    config: DataToolConfig,
    file_path: Optional[str] = None,
):
    data_bundle = chat_data.data
    metadata = safe_obj(data_bundle.metadata) if data_bundle is not None else {}
    main_entry_name = None
    main_shape = None
    main_dtype = None
    text_preview = None
    binary_preview = None
    data_kind = None
    sample_rate = None
    channel_count = None
    ref_streams = None
    stream_meta = None
    stream_obj = None
    if data_bundle is not None:
        definition = data_bundle.definition
        main_entry = definition.get_main_entry() if definition is not None else None
        if main_entry is not None:
            main_entry_name = main_entry.name
        main_data = data_bundle.get_main_data()
        stream_mgr = context.stream_manager
        if stream_mgr is not None and chat_data.stream_id is not None:
            try:
                stream_obj = stream_mgr.find_stream(chat_data.stream_id)
            except Exception:
                stream_obj = None
            if stream_obj is not None:
                stream_meta = stream_obj.metadata
        if chat_data.type in (ChatDataType.AVATAR_AUDIO, ChatDataType.HUMAN_TEXT, ChatDataType.HUMAN_DUPLEX_TEXT):
            # Try to fetch referenced upstream streams (e.g., text) for client side pairing.
            if stream_obj is not None:
                ref_streams = [stream_to_dict(s) for s in stream_obj.source_streams.values()]
        
        if chat_data.type is ChatDataType.MIC_AUDIO:
            data_kind = "heartbeat"
            text_preview = ''
        elif isinstance(main_data, str):
            data_kind = "text"
            text_preview = main_data[: config.preview_chars]
        elif file_path is not None:
            data_kind = "file"
            text_preview = ''
        elif main_data is not None:
            data_kind = type(main_data).__name__
            text_preview = str(main_data)

    return {
        "event": "chat_data",
        "session_id": context.session_id,
        "owner": context.owner,
        "data_type": chat_data.type.value,
        "timestamp": time.time(),
        "is_first": bool(chat_data.is_first_data),
        "is_last": bool(chat_data.is_last_data),
        "source": chat_data.source,
        "stream": stream_to_dict(chat_data.stream_id),
        "stream_meta": stream_meta,
        "ref_streams": ref_streams,
        "start_of_stream": chat_data.is_first_data,
        "end_of_stream": chat_data.is_last_data,
        "meta": metadata,
        "data": {
            "kind": data_kind,
            "main_entry": main_entry_name,
            "shape": main_shape,
            "dtype": main_dtype,
            "text": text_preview,
            "preview_base64": binary_preview,
            "sample_rate": sample_rate,
            "channels": channel_count,
            "file_path": file_path,
        },
    }


def build_signal_event(context: DataToolContext, signal: ChatSignal):
     # Try to fetch referenced upstream streams (e.g., text) for client side pairing.
    stream_mgr = getattr(context, "stream_manager", None)
    if stream_mgr is not None and signal.related_stream is not None:
        try:
            stream_obj = stream_mgr.find_stream(signal.related_stream)
        except Exception:
            stream_obj = None
        if stream_obj is not None:
            ref_streams = [stream_to_dict(s) for s in stream_obj.source_streams.values()]
    else:
        ref_streams = None
    return {
        "event": "signal",
        "session_id": context.session_id,
        "owner": context.owner,
        "timestamp": time.time(),
        "type": signal.type,
        "source_type": signal.source_type,
        "source_name": getattr(signal, "source_name", None),
        "stream": stream_to_dict(signal.related_stream),
        "ref_streams": ref_streams,
        "payload": safe_obj(signal.signal_data),
    }

