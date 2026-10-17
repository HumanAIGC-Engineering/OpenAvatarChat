from types import SimpleNamespace as NS

import pytest
import weakref


@pytest.mark.parametrize(
    "name,target,width,reset",
    [
        ("h264_nvenc", 1350000, 640, False),
        ("h264_nvenc", 1200000, 640, True),
        ("h264_nvenc", 750000, 640, True),
        ("h264_nvenc", 1500000, 1280, True),
        ("libx264", 1000000, 640, True),
    ],
)
def test_encoder_preserves_upstream_bitrate_and_resolution_policy(monkeypatch, name, target, width, reset):
    from aiortc.codecs import h264
    from handlers.client.rtc_client import client_handler_rtc as rtc

    created = []

    class Codec:
        def __init__(self, name):
            self.name = name
            self.width = 640
            self.height = 480
            self.bit_rate = 1500000

        def encode(self, frame):
            return []

    def create(name, mode):
        assert mode == "w"
        codec = Codec(name)
        created.append(codec)
        return codec

    # Keep the installed PyAV frame enum; replace codec construction only.
    monkeypatch.setattr(rtc.av, "CodecContext", NS(create=create))
    monkeypatch.setattr(rtc, "_actual_h264_encoder", None)
    old = Codec(name)
    encoder = NS(codec=old, target_bitrate=target, _preferred_encoder=name, buffer_data=b"", buffer_pts=None)
    old_ref = weakref.ref(old)
    del old
    frame = NS(width=width, height=480, pict_type=None)
    assert list(h264.H264Encoder._encode_frame(encoder, frame, False)) == []
    assert bool(created) is reset
    assert (old_ref() is None) is reset
    if reset:
        assert encoder.codec is created[0]
        assert encoder.codec.bit_rate == target
        assert encoder.codec.width == width
    else:
        assert encoder.codec is old_ref()


@pytest.mark.parametrize("fails", [False, True])
def test_probe_does_not_require_close_and_releases_context(monkeypatch, fails):
    import gc
    import weakref
    from handlers.client.rtc_client import client_handler_rtc as rtc

    references = []

    class Probe:
        def open(self):
            if fails:
                raise RuntimeError("unavailable")

    def create(name, mode):
        codec = Probe()
        references.append(weakref.ref(codec))
        return codec

    monkeypatch.setattr(rtc.av, "CodecContext", NS(create=create))
    if fails:
        with pytest.raises(RuntimeError, match="unavailable"):
            rtc._probe_h264_encoder("synthetic", {})
    else:
        rtc._probe_h264_encoder("synthetic", {})
    gc.collect()
    assert all(ref() is None for ref in references)


def test_real_software_probe_with_supported_pyav():
    from handlers.client.rtc_client import client_handler_rtc as rtc

    rtc._probe_h264_encoder("libx264", {"profile": "baseline", "tune": "zerolatency"})


@pytest.mark.parametrize("failure", ["create", "encode"])
def test_hardware_failure_falls_back_to_software(monkeypatch, failure):
    from aiortc.codecs import h264
    from handlers.client.rtc_client import client_handler_rtc as rtc

    attempts = []

    class Codec:
        def __init__(self, name):
            self.name = name

        def encode(self, frame):
            if self.name == "h264_nvenc":
                raise rtc._AVCodecError(1, "synthetic hardware failure")
            return []

    def create(name, mode):
        attempts.append(name)
        if failure == "create" and name == "h264_nvenc":
            raise RuntimeError("hardware unavailable")
        return Codec(name)

    monkeypatch.setattr(rtc.av, "CodecContext", NS(create=create))
    monkeypatch.setattr(rtc, "_selected_h264_encoder", "h264_nvenc")
    monkeypatch.setattr(rtc, "_actual_h264_encoder", None)
    encoder = NS(codec=None, target_bitrate=1000000, buffer_data=b"", buffer_pts=None)
    frame = NS(width=640, height=480, pict_type=None)
    assert list(h264.H264Encoder._encode_frame(encoder, frame, False)) == []
    assert attempts == ["h264_nvenc", "libx264"]
    assert encoder._preferred_encoder == "libx264"
    assert encoder.codec.bit_rate == 1000000


def test_probe_success_is_not_misclassified_when_close_is_missing(monkeypatch):
    from aiortc import RTCPeerConnection
    from aiortc.codecs import h264
    from handlers.client.rtc_client import client_handler_rtc as rtc

    class Probe:
        def open(self):
            pass

    monkeypatch.setattr(rtc.av, "CodecContext", NS(create=lambda *args: Probe()))
    monkeypatch.setattr(rtc, "_selected_h264_encoder", "libx264")
    monkeypatch.setattr(h264.H264Encoder, "_encode_frame", h264.H264Encoder._encode_frame)
    monkeypatch.setattr(rtc.aiortc_codecs, "get_encoder", rtc.aiortc_codecs.get_encoder)
    monkeypatch.setattr(RTCPeerConnection, "setRemoteDescription", RTCPeerConnection.setRemoteDescription)
    rtc._configure_h264_hardware_encoding()
    assert rtc._selected_h264_encoder == "h264_nvenc"
