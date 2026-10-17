# Experimental isolated FlashHead inference

This candidate keeps the default `in_process` mode and eager model execution.
It adds a `process` mode for testing model ownership independently from media
collection. It does not claim improved GPU performance before an A/B test.

```yaml
FlashHead:
  # Keep the usual model and condition-image settings.
  execution_mode: process
  max_buffer_seconds: 2.0
  worker_threads: 4
  worker_warmup_batches: 3
  worker_start_timeout: 600
  worker_request_timeout: 60
```

Set the engine's `concurrent_limit` to 1 for process mode. The child uses spawn,
loads the model once and completes real inference warm-up before reporting
ready. One shared-memory slot holds a batch; serialized requests and a parent
copy prevent overwriting a batch still in use. A worker error or timeout closes
the worker and releases the slot. Recovery requires a service restart; there is
no automatic restart or silent fallback.

The paired output queue applies backpressure. Capacity is at least one batch,
or `ceil(max_buffer_seconds * fps)`, whichever is larger. Cancellation changes
the generation and discards late results. Idle frames include matching silence
so audio and video clocks advance together. This is not a bound on every engine
or RTC queue and cannot retract media already buffered by a browser.

The pipeline currently requires 25 FPS and 16 kHz model input. Positive output
sample rates divisible by FPS remain accepted; the default is 24 kHz. Process
mode allows one active session. Other Avatar implementations are unchanged.
The idle paired-silence behavior also applies to in-process FlashHead and needs
end-to-end validation with the selected client before production use.

## Validation and GPU acceptance

CPU tests exercise actual spawn/shared memory with synthetic backends, warm-up
messages, paired output, cancellation, backpressure, startup failures, timeouts,
and cleanup. These tests do not load the FlashHead weights or prove GPU quality.

Use an isolated GPU test checkout, not a running deployment. Compare official
main, this candidate in `in_process`, and this candidate in `process`, with the
same dependency lock, public input, seed, image, model, GPU and compile disabled.
Record cold startup separately from warmed inference. Report raw model batch
latency (p50/p95/p99/max), fresh generated FPS, input-audio seconds per wall
second, first non-silent audio latency, queue occupancy, peak GPU memory for
both parent and worker, late-generation outputs, and resource cleanup.

Run at least 100 warmed batches and a 30-minute playback session, 100 interrupts
and repeated reconnects. Include worker crash/timeout and shutdown during
inference. Report failures and p99, not only averages. Queue bounds must hold,
no old-generation output may be accepted after cancellation, and no child or
shared-memory segment may remain after shutdown. Do not infer model throughput
from the collector's fixed 25 FPS or count idle frames as fresh inference.

GPU results are pending. No before/after speedup or memory reduction is claimed.
