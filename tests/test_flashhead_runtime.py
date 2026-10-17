"""CPU regression tests; no weights, CUDA device, network or production session."""

from multiprocessing import shared_memory
from types import SimpleNamespace as NS
import threading
import time

import numpy as np
import pytest
import torch

from handlers.avatar.flashhead.flashhead_config import FlashHeadConfig
from handlers.avatar.flashhead.flashhead_processor import (
    FlashHeadProcessor,
    FlashHeadProcessorCallbacks,
    FrameQueueItem,
)
from handlers.avatar.flashhead.flashhead_worker import FlashHeadWorker


PARAMS = dict(sample_rate=16000, tgt_fps=25, frame_num=33, motion_frames_num=9, cached_audio_duration=8)


class Backend:
    idle_frame = np.zeros((2, 2, 3), dtype=np.uint8)

    def __init__(self, block=False):
        self.entered = threading.Event()
        self.release = threading.Event()
        self.block = block
        self.resets = []

    def generate(self, audio, reset=False):
        self.resets.append(reset)
        self.entered.set()
        if self.block:
            assert self.release.wait(3)
        return np.zeros((24, 2, 2, 3), dtype=np.uint8)


def processor(backend=None):
    return FlashHeadProcessor(None, PARAMS, backend=backend or Backend(), max_buffer_seconds=0.96)


def item(speech="speech"):
    return FrameQueueItem(np.zeros((2, 2, 3), np.uint8), np.zeros(960), speech, False)


def test_capacity_and_cancel_blocked_producer():
    p = processor()
    for _ in range(24):
        assert p._enqueue(item(), 0)
    assert p._output_queue.qsize() == p._output_queue.maxsize == 24
    result = []
    thread = threading.Thread(target=lambda: result.append(p._enqueue(item(), 0)))
    thread.start()
    time.sleep(0.03)
    assert thread.is_alive()
    p.interrupt()
    p.reset_interrupt()
    thread.join(1)
    assert not thread.is_alive() and result == [False]
    assert p._output_queue.empty()


def test_stop_unblocks_backpressure():
    p = processor()
    for _ in range(24):
        p._enqueue(item(), 0)
    thread = threading.Thread(target=lambda: p._enqueue(item(), 0))
    thread.start()
    p.stop()
    thread.join(1)
    assert not thread.is_alive()


def test_late_inference_cannot_enter_new_generation():
    backend = Backend(block=True)
    p = processor(backend)
    thread = threading.Thread(
        target=p.add_audio,
        args=(
            np.zeros(15360 * 2),
            np.zeros(23040 * 2),
            "old",
            True,
        ),
    )
    thread.start()
    assert backend.entered.wait(1)
    begin = time.monotonic()
    p.interrupt()
    assert time.monotonic() - begin < 0.2  # Does not acquire the GPU lock.
    p.reset_interrupt()
    backend.release.set()
    thread.join(2)
    assert not thread.is_alive()
    assert p._output_queue.empty() and len(p._pending_audio) == 0
    p.add_audio(np.zeros(15360), np.zeros(23040), "new", True)
    pairs = list(p._output_queue.queue)
    assert len(pairs) == 24
    assert all(x.speech_id == "new" and x.generation == 1 for x in pairs)
    assert sum(x.end_of_speech for x in pairs) == 1
    assert backend.resets[-1] is True


@pytest.mark.parametrize("count", [0, 100, 15360])
def test_end_marker_once_and_audio_pairing(count):
    p = processor()
    p.add_audio(np.zeros(count), np.zeros(count * 3 // 2), "speech", True)
    pairs = list(p._output_queue.queue)
    assert sum(x.end_of_speech for x in pairs) == 1
    if count:
        assert len(pairs) == 24
        assert all(x.audio_segment.shape == (960,) for x in pairs)


def test_bgr_conversion():
    pipeline = NS(ref_img_latent=torch.zeros((1, 1)), original_color_reference=torch.zeros((1, 3, 1, 2, 2)))
    p = FlashHeadProcessor(pipeline, PARAMS)
    p._get_audio_embedding = lambda _: None
    p._run_pipeline = lambda _: torch.tensor([1, 2, 3]).expand(33, 2, 2, 3)
    result = p._infer_bgr(np.zeros(128000))
    assert result.shape == (24, 2, 2, 3)
    assert result[0, 0, 0].tolist() == [3, 2, 1]
    assert result.flags.c_contiguous


@pytest.mark.parametrize("kind", ["empty", "idle", "speech", "end", "interrupted"])
def test_collector_keeps_audio_video_paired(kind):
    p = processor()
    video, audio, end = [], [], []
    p.set_callbacks(FlashHeadProcessorCallbacks(video.append, audio.append, end.append))
    if kind in ("idle", "speech"):
        for _ in range(8):
            pair = item(None if kind == "idle" else "speech")
            if kind == "idle":
                pair.audio_segment = None
            p._enqueue(pair, 0)
    if kind == "end":
        p._enqueue(FrameQueueItem(None, None, "speech", True), 0)
    if kind == "interrupted":
        p._enqueue(item(), 0)
        p.interrupt()
    thread = threading.Thread(target=p._frame_collector_worker)
    thread.start()
    time.sleep(0.22)
    p._stop_event.set()
    thread.join(1)
    assert not thread.is_alive()
    assert len(video) == len(audio) >= 4
    assert all(x.shape == (960,) for x in audio)
    assert len(end) == (1 if kind == "end" else 0)


@pytest.mark.parametrize(
    "overrides",
    [
        dict(fps=24),
        dict(fps=0),
        dict(output_audio_sample_rate=16001),
        dict(algo_audio_sample_rate=22050),
        dict(max_buffer_seconds=0),
    ],
)
def test_config_rejects_unsupported_timing(overrides):
    with pytest.raises(ValueError):
        FlashHeadConfig(**overrides)


def fake_worker(connection, config, engine, root):
    memory = None
    try:
        if config.get("fail_start"):
            connection.send(dict(type="error", error="deliberate startup failure"))
            return
        if config.get("hang_start"):
            time.sleep(10)
            return
        connection.send(
            dict(type="ready", infer_params=PARAMS, idle_frame=np.zeros((2, 2, 3), np.uint8), shape=(24, 2, 2, 3))
        )
        request = connection.recv()
        memory = shared_memory.SharedMemory(name=request["name"])
        slot = np.ndarray((24, 2, 2, 3), np.uint8, buffer=memory.buf)
        connection.send(dict(type="attached"))
        while True:
            request = connection.recv()
            if request["type"] == "stop":
                return
            if request["type"] == "release":
                connection.send(dict(type="released"))
                continue
            if config.get("hang_request"):
                time.sleep(10)
                continue
            if config.get("fail_request"):
                connection.send(dict(type="error", error="deliberate inference failure"))
                return
            slot.fill(int(request["audio"][0]))
            connection.send(dict(type="frames"))
    finally:
        if memory is not None:
            memory.close()
        connection.close()


def worker(**changes):
    config = dict(worker_start_timeout=10, worker_request_timeout=2)
    config.update(changes)
    return FlashHeadWorker(config, {}, "", target=fake_worker)


def test_spawn_single_slot_copies_and_cleans_up():
    w = worker()
    name = w._memory.name
    try:
        session = w.session("one")
        with pytest.raises(RuntimeError, match="one active"):
            w.session("two")
        a = session.generate(np.array([17]))
        b = session.generate(np.array([29]))
        assert np.all(a == 17) and np.all(b == 29)
        session.close()
        session.close()
        w.session("two").close()
    finally:
        w.close()
        w.close()
    with pytest.raises(FileNotFoundError):
        shared_memory.SharedMemory(name=name)


def test_worker_startup_error():
    with pytest.raises(RuntimeError, match="deliberate startup"):
        worker(fail_start=True)


def test_worker_startup_timeout():
    with pytest.raises(TimeoutError):
        worker(hang_start=True, worker_start_timeout=0.05)


@pytest.mark.parametrize("failure", ["hang_request", "fail_request"])
def test_worker_failed_rpc_is_not_reused(failure):
    w = worker(**{failure: True}, worker_request_timeout=0.1)
    name = w._memory.name
    session = w.session("one")
    with pytest.raises((TimeoutError, RuntimeError)):
        session.generate(np.array([1]))
    assert w._closed
    with pytest.raises(RuntimeError, match="closed"):
        session.generate(np.array([2]))
    session.close()
    w.close()
    with pytest.raises(FileNotFoundError):
        shared_memory.SharedMemory(name=name)


def test_close_interrupts_inflight_rpc_without_waiting_request_timeout():
    w = worker(hang_request=True, worker_request_timeout=30)
    session = w.session("one")
    errors = []

    def run():
        try:
            session.generate(np.array([1]))
        except Exception as exc:
            errors.append(exc)

    thread = threading.Thread(target=run)
    thread.start()
    time.sleep(0.1)
    begin = time.monotonic()
    w.close()
    thread.join(1)
    assert time.monotonic() - begin < 5
    assert not thread.is_alive() and errors


def test_reset_session_drops_queue_and_invalidates_old_generation():
    p = processor()
    p._enqueue(item(), 0)
    p.reset_session()
    assert p._generation == 1 and p._output_queue.empty()
    assert not p._interrupted and p._motion_reset_pending
    assert not p._enqueue(item(), 0)


class CPUOnlyPipeline:
    def __init__(self):
        self.ref_img_latent = torch.zeros((1, 1, 1))
        self.original_color_reference = torch.zeros((1, 3, 1, 2, 2))
        self.latent_motion_frames = self.ref_img_latent.clone()
        self.generator = torch.Generator()
        self.device = "cpu"

    def preprocess_audio(self, audio, sr, fps):
        return torch.zeros((400, 1))

    def generate(self, embedding):
        value = self.latent_motion_frames.mean().item()
        self.latent_motion_frames = self.latent_motion_frames + 1
        return torch.full((3, 33, 2, 2), value / 10)


def cpu_worker_entry(connection, config, engine, root):
    # Keep the real worker entry point, processor, warmup and IPC. Replace only
    # weight loading with a CPU pipeline implementing the model's public API.
    import sys
    from types import ModuleType
    from handlers.avatar.flashhead.flashhead_worker import _worker_main

    class CPUOnlyHandler:
        def load(self, engine, config):
            self.pipeline = CPUOnlyPipeline()
            self.infer_params = PARAMS

        def _validate_timing(self, config):
            assert config.fps == 25

    module = ModuleType("handlers.avatar.flashhead.avatar_handler_flashhead")
    module.HandlerAvatarFlashHead = CPUOnlyHandler
    sys.modules[module.__name__] = module
    _worker_main(connection, config, engine, root)


def test_real_worker_entrypoint_warms_up_and_keeps_session_motion_state():
    config = FlashHeadConfig(worker_start_timeout=10, worker_request_timeout=2).model_dump()
    w = FlashHeadWorker(config, {}, "", target=cpu_worker_entry)
    try:
        session = w.session("one")
        a = session.generate(np.zeros(128000))
        b = session.generate(np.zeros(128000))
        reset = session.generate(np.zeros(128000), reset=True)
        assert a.shape == (24, 2, 2, 3)
        assert not np.array_equal(a, b)
        assert np.array_equal(a, reset)
        session.close()
        next_session = w.session("two")
        assert np.array_equal(a, next_session.generate(np.zeros(128000)))
        next_session.close()
    finally:
        w.close()


@pytest.mark.parametrize("rate", [16000, 24000, 44100, 48000])
def test_output_clock_retains_compatible_sample_rates(rate):
    config = FlashHeadConfig(output_audio_sample_rate=rate)
    assert config.output_audio_sample_rate == rate
    backend = Backend()
    p = FlashHeadProcessor(None, PARAMS, output_audio_sample_rate=rate, backend=backend)
    assert p._original_audio_per_frame == rate // 25
