import importlib
import os
import sys
import unittest
from types import SimpleNamespace
from unittest.mock import patch

import av

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
SRC_ROOT = os.path.join(PROJECT_ROOT, "src")
for path in (PROJECT_ROOT, SRC_ROOT):
    if path not in sys.path:
        sys.path.insert(0, path)

rtc_module = importlib.import_module("src.handlers.client.rtc_client.client_handler_rtc")

class FakePacket:
    def __init__(self, data: bytes):
        self._data = data

    def __bytes__(self):
        return self._data


class FakeCodec:
    def __init__(self, name: str, ok: bool):
        self.name = name
        self._ok = ok
        self.closed = False
        self.width = 0
        self.height = 0
        self.bit_rate = 0
        self.pix_fmt = None
        self.framerate = None
        self.time_base = None
        self.options = {}
        self.profile = ""

    def encode(self, _frame):
        if not self._ok:
            raise av.error.ExternalError(-542398533, "encode failure")
        return [FakePacket(b"\x00\x01")]

    def close(self):
        self.closed = True


class TestH264EncoderFallback(unittest.TestCase):
    def test_encode_error_triggers_fallback(self):
        original_selected = rtc_module._selected_h264_encoder
        dummy_encoder = SimpleNamespace(
            codec=None,
            target_bitrate=rtc_module.h264.DEFAULT_BITRATE,
            buffer_data=b"",
            buffer_pts=None,
            _preferred_encoder=None,
        )
        frame = SimpleNamespace(width=640, height=480, pict_type=None)
        emitted_chunks = []
        codecs_created = []

        def fake_split_bitstream(data):
            emitted_chunks.append(data)
            yield data

        dummy_encoder._split_bitstream = fake_split_bitstream

        def fake_create(name, mode):
            self.assertEqual(mode, "w")
            codec = FakeCodec(name, ok=(name == "libx264"))
            codecs_created.append(codec)
            return codec

        rtc_module._selected_h264_encoder = "h264_nvenc"

        try:
            fake_codec_context = SimpleNamespace(create=lambda name, mode: fake_create(name, mode))
            with patch.object(rtc_module.av, "CodecContext", fake_codec_context):
                list(rtc_module.h264.H264Encoder._encode_frame(dummy_encoder, frame, False))
            selected_after = rtc_module._selected_h264_encoder
        finally:
            rtc_module._selected_h264_encoder = original_selected

        self.assertEqual(dummy_encoder._preferred_encoder, "libx264")
        self.assertEqual(selected_after, "libx264")
        self.assertTrue(emitted_chunks)
        self.assertTrue(emitted_chunks[0])
        self.assertEqual(frame.pict_type, av.video.frame.PictureType.I)
        self.assertTrue(codecs_created[0].closed)


if __name__ == "__main__":
    unittest.main()

