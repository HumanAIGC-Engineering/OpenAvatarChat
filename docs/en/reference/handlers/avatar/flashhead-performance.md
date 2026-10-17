# FlashHead performance candidate

This independent candidate keeps eager execution by default. `enable_compile`
is an explicit opt-in; it must be tested on the actual GPU before use. The
candidate also quantizes decoded frames to uint8 before the device-to-host
transfer. Existing downstream BGR uint8 output remains the contract.

CPU float32/float16 tests compare the new pixel values with the old floating
point conversion followed by NumPy uint8 casting. They do not prove CUDA value
equivalence, compiler compatibility, visual quality or speedup.

Use a dedicated GPU checkout with the same model, public input, seed, image and
dependency lock. Compare official main, this candidate with compile disabled,
and compile enabled. Separate cold compile/warm-up time from steady state;
measure at least 100 warmed batches. Record p50/p95/p99/max model latency,
fresh generated FPS, GPU memory peak, transfer bytes/time and failure count.
Perform a 30-minute run and compare image outputs using fixed inputs. Include
eager fallback GPUs and validate both single- and multi-session in-process use.

Do not compare different model versions or present fixed playback FPS as model
throughput. GPU and visual-quality results are pending; no benefit is claimed.
This candidate requires no worker, RTC queue or deployment changes.
