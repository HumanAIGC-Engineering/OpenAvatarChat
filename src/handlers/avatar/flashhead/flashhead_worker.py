"""Spawned FlashHead model owner with one bounded shared-memory batch slot.

The parent never loads CUDA weights in process mode. RPC is serialized, so the
worker may reuse the slot only after the parent has copied the previous batch.
No private hostnames, fixed socket paths, or model-specific image sizes are used.
"""
import multiprocessing as mp
import os
from multiprocessing import shared_memory
import threading
import time

import numpy as np


def _worker_main(connection, config_data, engine_data, handler_root):
    memory = None
    try:
        os.environ.setdefault('USE_TF', '0')
        os.environ.setdefault('USE_FLAX', '0')
        os.environ.setdefault('TORCHINDUCTOR_COMPILE_THREADS', '4')
        import cv2
        import torch
        from handlers.avatar.flashhead.flashhead_config import FlashHeadConfig
        from handlers.avatar.flashhead.avatar_handler_flashhead import HandlerAvatarFlashHead
        from handlers.avatar.flashhead.flashhead_processor import FlashHeadProcessor
        from chat_engine.data_models.chat_engine_config_data import ChatEngineConfigModel

        torch.set_num_threads(config_data['worker_threads'])
        cv2.setNumThreads(1)
        config_data = dict(config_data, execution_mode='in_process')
        config = FlashHeadConfig(**config_data)
        handler = HandlerAvatarFlashHead()
        handler.handler_root = handler_root
        handler.load(ChatEngineConfigModel(**engine_data), config)
        handler._validate_timing(config)
        processor = FlashHeadProcessor(handler.pipeline, handler.infer_params)
        audio = np.zeros(processor.sample_rate * processor.cached_audio_duration)
        # Exercise the real embedding, diffusion, VAE, device copy and conversion.
        for _ in range(config.worker_warmup_batches):
            frames = processor._infer_bgr(audio)
        shape = tuple(frames.shape)
        connection.send(dict(type='ready', infer_params=handler.infer_params,
                             idle_frame=processor._idle_frame, shape=shape))
        request = connection.recv()
        if request['type'] != 'attach':
            raise RuntimeError('Expected shared-memory attachment')
        memory = shared_memory.SharedMemory(name=request['name'])
        slot = np.ndarray(shape, dtype=np.uint8, buffer=memory.buf)
        connection.send(dict(type='attached'))
        states = {}
        initial = processor._initial_latent_1slice
        while True:
            request = connection.recv()
            kind = request['type']
            if kind == 'stop':
                break
            session_id = request['session_id']
            if kind == 'release':
                states.pop(session_id, None)
                connection.send(dict(type='released'))
                continue
            if kind != 'generate':
                raise RuntimeError('Unknown FlashHead worker request')
            if request['reset'] or session_id not in states:
                handler.pipeline.generator.manual_seed(config.base_seed)
            processor._latent_motion_frames = (
                initial.clone() if request['reset'] or session_id not in states
                else states[session_id]
            )
            frames = processor._infer_bgr(request['audio'])
            states[session_id] = processor._latent_motion_frames
            if frames.shape != shape:
                raise RuntimeError('FlashHead output shape changed after warmup')
            np.copyto(slot, frames)
            connection.send(dict(type='frames'))
    except (EOFError, BrokenPipeError):
        pass
    except Exception as exc:
        try:
            connection.send(dict(type='error', error=f'{type(exc).__name__}: {exc}'))
        except (EOFError, BrokenPipeError, OSError):
            pass
    finally:
        if memory is not None:
            memory.close()
        connection.close()


class FlashHeadWorker:
    def __init__(self, config, engine, handler_root, *, target=_worker_main):
        self._lock = threading.RLock()
        self._closed = False
        self._close_lock = threading.Lock()
        self._memory = None
        self._slot = None
        self._timeout = config['worker_request_timeout']
        self._sessions = set()
        context = mp.get_context('spawn')  # Never fork a CUDA-initialized parent.
        self._connection, child = context.Pipe()
        self._process = context.Process(
            target=target, args=(child, config, engine, handler_root),
            name='FlashHead-Inference', daemon=True,
        )
        try:
            self._process.start()
            child.close()
            ready = self._receive(config['worker_start_timeout'])
            if ready['type'] != 'ready':
                raise RuntimeError('FlashHead worker did not become ready')
            self.infer_params = ready['infer_params']
            self.idle_frame = ready['idle_frame']
            shape = tuple(ready['shape'])
            self._memory = shared_memory.SharedMemory(
                create=True, size=int(np.prod(shape)),
            )
            self._slot = np.ndarray(shape, dtype=np.uint8, buffer=self._memory.buf)
            self._connection.send(dict(type='attach', name=self._memory.name))
            if self._receive(self._timeout)['type'] != 'attached':
                raise RuntimeError('FlashHead worker failed to attach its frame slot')
        except BaseException:
            child.close()
            self.close()
            raise

    def _receive(self, timeout):
        deadline = time.monotonic() + timeout
        while True:
            if self._closed:
                raise RuntimeError('FlashHead inference worker is closed')
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise TimeoutError('FlashHead inference worker response timed out')
            if self._connection.poll(min(remaining, .05)):
                break
            if not self._process.is_alive():
                raise RuntimeError('FlashHead inference worker exited without a response')
        message = self._connection.recv()
        if message.get('type') == 'error':
            raise RuntimeError(message['error'])
        return message

    def _request(self, message):
        with self._lock:
            if self._closed:
                raise RuntimeError('FlashHead inference worker is closed')
            try:
                self._connection.send(message)
                return self._receive(self._timeout)
            except Exception:
                # A timed-out RPC cannot be reused: its late reply could otherwise
                # be mistaken for the next request's response.
                self.close()
                raise

    def session(self, session_id):
        with self._lock:
            if self._closed:
                raise RuntimeError('FlashHead inference worker is closed')
            if self._sessions and session_id not in self._sessions:
                raise RuntimeError('FlashHead process mode supports one active session')
            self._sessions.add(session_id)
        return WorkerSession(self, session_id)

    def close(self):
        # Wake an in-flight _receive before acquiring its RPC lock.
        with self._close_lock:
            if self._closed:
                return
            self._closed = True
        with self._lock:
            if self._process.pid is not None:
                if self._process.is_alive():
                    try:
                        self._connection.send(dict(type='stop'))
                    except (BrokenPipeError, EOFError, OSError):
                        pass
                    self._process.join(timeout=2)
                    if self._process.is_alive():
                        self._process.terminate()
                        self._process.join(timeout=2)
                    if self._process.is_alive():
                        self._process.kill()
                        self._process.join(timeout=2)
                self._process.close()
            self._connection.close()
            self._slot = None
            if self._memory is not None:
                self._memory.close()
                self._memory.unlink()
                self._memory = None


class WorkerSession:
    def __init__(self, worker, session_id):
        self._worker = worker
        self._session_id = session_id
        self.idle_frame = worker.idle_frame
        self._closed = False

    def generate(self, audio, reset=False):
        with self._worker._lock:
            if self._closed:
                raise RuntimeError('FlashHead session is closed')
            message = self._worker._request(dict(
                type='generate', session_id=self._session_id,
                audio=np.asarray(audio, dtype=np.float32), reset=reset,
            ))
            if message['type'] != 'frames':
                self._worker.close()
                raise RuntimeError('Unexpected FlashHead worker response')
            # The caller owns this copy; the shared slot may now be overwritten.
            return self._worker._slot.copy()

    def close(self):
        with self._worker._lock:
            if self._closed:
                return
            self._closed = True
            try:
                if not self._worker._closed:
                    self._worker._request(dict(type='release', session_id=self._session_id))
            finally:
                self._worker._sessions.discard(self._session_id)
