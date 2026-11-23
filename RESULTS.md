
## Standardized benchmarks: Aider Polyglot (225 exercises, six languages; aider 5dc9490, edit format "whole", benchmark container on the 7920)

| Model | Setting | Exercises finished | Passed first try | Passed within two tries | Well-formed | Seconds per exercise | Notes | Date |
|---|---|---|---|---|---|---|---|---|
| Qwen3.8-27B FP8 (GPU 0, vLLM, 4 threads) | thinking OFF (its writer setting in the router) | 224 of 225 | 40 (17.9%) | 115 (51.3% of 224; 51.1% of 225 counting the unfinished one as failed) | 99.6% | 98.7 | One exercise (go/robot-simulator) never finished: every request timed out and aider backed off for hours; the run was stopped by hand after about 9 h, of which the first ~1.7 h produced the 224 results. Per language, passed within two tries: cpp 16 of 26, go 18 of 38, java 20 of 47, javascript 27 of 49, python 17 of 34, rust 17 of 30. 2 test timeouts, 1 context-window exhaustion. | 18 Nov |
| Qwen3.8-27B FP8 (GPU 0, vLLM, 4 threads) | thinking OFF, edit format DIFF (comparable with the published leaderboard) | 225 of 225 | 36 (16.0%) | 114 (50.7%) | n/a (see stats) | 108.4 | Per language passed/total: cpp 12/26, go 17/39, java 22/47, javascript 32/49, python 16/34, rust 15/30. Tokens: 3.98 M prompt, 0.71 M completion. Per correct answer: 214 s, about 41,100 tokens. Run full-qwen38-fp8-diff-nothink. | 2026-11-18/19 |
| Qwen3.8-27B FP8 (GPU 0, vLLM) | FP8, thinking ON, diff, 4 sessions, request timeout 1800 s | 225 of 225 | 72 (32.0%) | 156 (69.3%) | 100% | 417.1 | Per language passed/total: cpp 16/26, go 26/39, java 28/47, javascript 39/49, python 29/34, rust 18/30. Tokens: 2.46 M prompt, 3.32 M completion. Per correct answer: 371 s, about 21,300 tokens (57.5 tokens/s per correct answer). vs thinking OFF (50.7%): +18.6 points within-two-tries, +16.0 points first-try, but about 3.8x slower per case (417.1 s vs 108.4 s) and about 4.7x more completion tokens. Run full-qwen38-fp8-diff-thinking. | 2026-11-19/20 |
| DeepSeek-V4.1-Flash-1017 Maya-S (GPU 1 + RAM, 4 sessions) | thinking OFF, edit format DIFF (comparable with the published leaderboard) | 225 of 225 | 72 (32.0%) | 153 (68.0%) | n/a (see stats) | 153.1 | Per language passed/total: cpp 20/26, go 24/39, java 34/47, javascript 34/49, python 22/34, rust 19/30. Tokens: 2.46 M prompt, 0.28 M completion. Per correct answer: 225 s, about 17,900 tokens. No test timeouts in Java. Run full-deepseek-diff-nothink. | 2026-11-18/19 |
| DeepSeek-V4.1-Flash-1017 Maya-S (GPU 1 + RAM, 4 sessions) | thinking ON, diff, request timeout 1800 s | 225 of 225 | 85 (37.8%) | 193 (85.8%) | 98.7% | 1109.5 | Tokens: 2.44 M prompt, 5.80 M completion. 4 error outputs (3 malformed), 1 exhausted context window, 0 test timeouts. Per correct answer: ~1,293 s, ~30,100 tokens (23.3 tok/s per correct answer). vs thinking OFF (68.0%): +17.8 points within-two-tries, +5.8 points first-try, but about 7.2x slower per case (1109.5 s vs 153.1 s) and far more completion tokens (5.80 M vs 0.28 M, ~20x). FINISHED 08:47:10 UTC 20 Nov - the last standardized Aider run of this campaign. Run full-deepseek-diff-thinking. | 2026-11-19/20 |
| Qwen3.8-27B FULL PRECISION BF16 (GPU 0, vLLM, 8 threads, 65k context) | thinking OFF, edit format DIFF | 225 of 225 | 39 (17.3%) | 113 (50.2%) | n/a (see stats) | 171.2 (ran alongside the DeepSeek 10-try run) | Precision effect vs the 8-bit build (50.7%): none measurable. Per language passed/total: cpp 15/26, go 18/39, java 22/47, javascript 25/49, python 19/34, rust 14/30. Tokens: 3.74 M prompt, 0.68 M completion. Per correct answer: 341 s, about 39,100 tokens. 1 test timeout (Java). Second attempt; first attempt invalid (see below). Run full-qwen38-bf16-diff-nothink. | 2026-11-19 |
| Mistral Small 4 119B NVFP4 (GPU 0, vLLM, 4 threads) | default, edit format DIFF | 225 of 225 | 10 (4.4%) | 34 (15.1%) | 93.8% | 23.6 | FINAL - PROVISIONAL flag cleared 20 Nov. Investigated `full-mistral-small-4-diff.log`: all `num_malformed_responses` failures are `SearchReplaceNoExactMatch` (model's SEARCH block guesses at stub content instead of copying it verbatim, e.g. affine_cipher.py's stub), not a vLLM serving or chat-template fault. 25 malformed responses across 14 of 225 exercises (6.2%); low score is primarily genuine solve-rate, not a formatting artifact. Per language passed/total: cpp 5/26, go 6/39, java 8/47, javascript 6/49, python 6/34, rust 3/30. error_outputs 25, user_asks 31, 5 test timeouts. Tokens: 2.40 M prompt, 0.31 M completion. Run full-mistral-small-4-diff. | 2026-11-19/20 |
| Devstral Small 2 24B (GPU 0, vLLM, 4 threads) | default, edit format DIFF | 225 of 225 (FINAL - continued with --cont from the 212 watchdog stop) | 8 (3.6%) | 31 (13.8%) | n/a (see stats) | 43.7 | PROVISIONAL figure confirmed by completion, low score is real, not a truncation artifact. Per language n/a (not re-pulled this check-in). 2 test timeouts. Run full-devstral-small-2-diff. | 2026-11-19/20 |
| gpt-oss-120b (GPU 0, vLLM, 4 threads) | default, edit format DIFF | 225 of 225 | 35 (15.6%) | 120 (53.3%) | 91.6% | 55.6 | 29 malformed/error outputs (19 exercises affected), 140 user-asks, 0 test timeouts, 0 exhausted context windows. Tokens: 2.97 M prompt, 0.79 M completion. Run full-gpt-oss-120b-diff. | 2026-11-19/20 |
| Qwen3-235B-A22B-Instruct-2507 NVFP4 (RedHatAI build, T7920 2x RTX PRO 6000 Blackwell Max-Q, vLLM, tensor-parallel 2) | non-thinking, edit format DIFF, run 22:20-23:29 UTC | 225 of 225 | 47 (20.9%) | 121 (53.8%) | n/a (not reproducible from counts; see notes) | 65.3 | 62 malformed responses, 63 error outputs, 3 test timeouts, 1 exhausted context window. Tokens: about 2.61 M prompt, 0.415 M completion. Published Aider leaderboard score for this model is 59.6%; ours is about 6 points lower. Likely contributors (not isolated by testing): NVFP4 4-bit weights and activations, the high malformed-response count under the diff format, no model-specific aider settings file, and a conservative context cap. | 2026-11-20 |

FOUNDER RULING 2026-11-18 18:27 ET: all Aider runs use the "diff" edit format, as the published leaderboard does. The first row is the only "whole"-format run; it is NOT comparable and is superseded by the diff-format runs (queue ~/df-bench/std/aq3.sh: Qwen3.8 FP8 diff thinking off; full precision diff thinking off; full precision diff thinking on; then Devstral Small 2, gpt-oss-120b, Mistral Small 4).

INVALID RUN 2026-11-19: the first attempt at run B (Qwen3.8-27B full precision, diff, thinking off) was stopped at 115 results and set aside (folder suffix -INVALID-gradle): the Gradle download inside the benchmark container stalled on a slow internet link (about 70-100 KB/s), so 23 of 24 Java exercises timed out in the test step (0 of 23 passed) - a harness fault, not a model result. Fix: Gradle 8.7 distribution kept on the host (~/df-bench/std/gradle-dists) and mounted into every benchmark container (aider-run.sh); queues restarted by fixq.sh (aq4.sh, aqd2.sh). Runs A and DeepSeek were not affected (0 Java test timeouts).

FOUNDER REQUEST 2026-11-18 20:22 ET: add a 'work until correct' test (raise aider --tries above 2, with a cap) and report per model the share solved, average tries, time and tokens per correct answer, to compare cost-effectiveness of models and hardware. Separate table; not comparable with published two-try scores.

## Work until correct (founder request 2026-11-18 20:22 ET): Aider Polyglot, diff format, up to 10 tries per exercise

Not comparable with published two-try scores. "Per correct answer" divides ALL time and tokens of the run (including unsolved exercises) by the number solved.

| Model | Setting | Solved within 10 tries | Unsolved after 10 tries | Tries needed (solved ones) | Average tries | Standard score inside this run (within two tries) | Seconds per correct answer | Tokens per correct answer | Notes | Date |
|---|---|---|---|---|---|---|---|---|---|---|
| DeepSeek-V4.1-Flash-1017 Maya-S (GPU 1 + RAM, 4 sessions) | thinking OFF | 207 of 225 (92.0%) | 18 (all used the full 10 tries) | 1: 81, 2: 81, 3: 23, 4: 17, 5: 4, 6: 1 | 1.96 | 162 of 225 (72.0%); the separate standard run gave 68.0% | 270 | about 29,300 (5.66 M prompt, 0.41 M completion in total) | Per language solved/total: cpp 23/26, go 37/39, java 41/47, javascript 46/49, python 32/34, rust 28/30. 6 test timeouts, no context exhaustion. Nothing was solved after try 6. Run until10-deepseek-diff-nothink. | 2026-11-19 |
| Qwen3.8-27B FP8 (GPU 0, vLLM, 4 sessions) | thinking OFF | 190 of 225 (84.4%) | 35 (all used the full 10 tries) | 1: 42, 2: 66, 3: 45, 4: 15, 5: 7, 6: 11, 7: 2, 8: 1, 9: 1 | 2.64 | 108 of 225 (48.0%); the separate standard run gave 50.7% | 261 | about 88,900 (15.49 M prompt, 1.40 M completion in total) | Per language solved/total: cpp 25/26, go 34/39, java 36/47, javascript 41/49, python 28/34, rust 26/30. 5 test timeouts, no context exhaustion. Run until10-qwen38-fp8-diff-nothink. | 2026-11-19 |

Reading (2026-11-19): with up to ten tries the smaller model closes most of the gap (84.4% vs 92.0%) in about the same time per correct answer (261 s vs 270 s) but needs about three times the tokens (88,900 vs 29,300) and 2.64 tries vs 1.96. Queue state 09:05 ET 19 Nov: founder asked for a power-down to inspect cooling/cabling - GPU 0 queue stopped after this run; DeepSeek thinking-on run drained at about 50 of 225 (175 unstarted exercises set aside in tmp.benchmarks/_held--full-deepseek-diff-thinking, to be restored and continued with --cont). Still to run after power-on: Qwen thinking-on, gpt-oss-120b, Devstral remainder.

RUNS THAT DID NOT COMPLETE 2026-11-19 (causes found, repeated by ~/df-bench/std/aq5.sh and aqd3.sh, started 10:16 UTC):
- Qwen3.8-27B full precision, thinking ON: stopped by the watchdog at 34 results (22 passed) - aider's 600 s request timeout was too short for thinking replies with 8 parallel sessions. Repeated on the standing FP8 server (full precision showed no score difference), 4 sessions, request timeout 1800 s, watchdog 90 min.
- DeepSeek thinking ON: stopped by the watchdog at 8 results (7 passed) - same cause. Repeated with request timeout 1800 s, watchdog 90 min.
- gpt-oss-120b: killed at 8 results by the benchmark container's 12 GB memory limit (kernel log: memory cgroup out of memory). Limit raised to 32 GB; repeated.
- Devstral Small 2: stopped by the watchdog at 212 of 225; continued with aider --cont.
- Added to the GPU 0 queue first: Qwen3.8-27B FP8 thinking off, up to 10 tries (until10-qwen38-fp8-diff-nothink).

## Time to solution (added 2026-11-21)

Founder priority: the measure that matters is wall-clock time to a correct solution, not the number of tries. Share of all 225 exercises solved within N minutes of starting (per-exercise wall time, all tries included; 4 parallel sessions share the GPU, so times are under load). Script: `~/df-bench/std/ttsolve.py` on the T7920. All rows are complete 225-exercise runs.

| Run | Benchmark (2 tries) | Solved (final) | Median time to solve | Solved within 5 min | within 10 min | within 30 min |
|---|---|---|---|---|---|---|
| DeepSeek-V4.1-Flash thinking OFF — retry run (up to 10 tries; separate run) | 72.0% | 92.0% | 1.6 min | 78.7% | 89.8% | 91.6% |
| Qwen3.8-Flash-Next Q8_0 on Strata, thinking OFF — retry run (up to 10 tries; separate run) | 73.8% | 89.8% | 0.2 min | 89.8% | 89.8% | 89.8% |
| Qwen3.8-Flash-Next Q8_0 on Basalt, thinking OFF — retry run (up to 10 tries; separate run) | 75.1% | 90.7% | 0.2 min | 90.7% | 90.7% | 90.7% |
| Qwen3.8-27B FP8 thinking OFF — retry run (up to 10 tries; separate run) | 48.0% | 84.4% | 1.1 min | 74.7% | 82.7% | 84.4% |
| DeepSeek-V4.1-Flash thinking ON, 2 tries | 85.8% | 85.8% | 8.8 min | 30.2% | 45.8% | 73.8% |
| Qwen3.5-397B-A17B Q4_K_M thinking OFF, 2 tries | 84.4% | 84.4% | 6.2 min | 33.8% | 63.6% | 79.1% |
| Qwen3.8-27B BF16 thinking ON, 2 tries | 75.1% | 75.1% | 7.3 min | 27.1% | 45.3% | 68.4% |
| Qwen3.8-27B NVFP4 thinking ON, 2 tries | 71.1% | 71.1% | 3.3 min | 42.7% | 63.6% | 68.9% |
| Qwen3.8-27B FP8 thinking ON, 2 tries | 69.3% | 69.3% | 4.0 min | 39.1% | 53.3% | 68.9% |
| DeepSeek-V4.1-Flash thinking OFF — standard benchmark run (2 tries) | 68.0% | 68.0% | 1.7 min | 61.3% | 67.1% | 68.0% |
| Qwen3-235B-A22B-Instruct-2507 NVFP4, 2 tries | 53.8% | 53.8% | 0.7 min | 53.3% | 53.8% | 53.8% |
| gpt-oss-120b, 2 tries | 53.3% | 53.3% | 0.7 min | 52.4% | 52.9% | 53.3% |
| Qwen3.8-27B FP8 thinking OFF — standard benchmark run (2 tries) | 50.7% | 50.7% | 0.8 min | 48.4% | 50.7% | 50.7% |
| Qwen3.8-27B NVFP4 thinking OFF, 2 tries | 42.7% | 42.7% | 0.5 min | 42.2% | 42.7% | 42.7% |
| Qwen3.8-27B BF16 thinking OFF, 2 tries | 50.2% | 50.2% | 1.3 min | 43.1% | 48.4% | 50.2% |
| Mistral Small 4 119B NVFP4, 2 tries | 15.1% | 15.1% | 0.2 min | 15.1% | 15.1% | 15.1% |
| Devstral Small 2 24B, 2 tries | 13.8% | 13.8% | 0.4 min | 13.8% | 13.8% | 13.8% |

Reading: a fast non-thinking model in a test-feedback loop reaches a correct solution sooner than a slow thinking model. DeepSeek thinking OFF with retries solves 78.7% within 5 minutes vs 30.2% for the same model thinking ON.


## Qwen3.5-397B-A17B Q4_K_M — llama.cpp, thinking OFF (2026-11-21)

- Setup: unsloth-style GGUF Q4_K_M (228 GB, 6 shards), llama.cpp server-cuda (build 12464), both GPUs, `--n-cpu-moe 18` (18 layers' experts in system RAM), `--tensor-split 13,7`, 131072 total context (4 slots × 32K), `-b 4096 -ub 2048 --threads 48`, `--reasoning off`, `--reasoning-format deepseek`. VRAM ~94 GB / ~81 GB. Launcher `~/df-bench/std/llama_up.sh`, run `aq8.sh`.
- Result (225 of 225, diff format, 4 sessions): first try 131 (58.2%), within two tries 190 (84.4%), well-formed 97.8% (6 malformed responses, 35 error outputs, 1 context exhaustion, 0 test timeouts).
- Per language within two tries: cpp 23/26, go 34/39, java 38/47, javascript 42/49, python 32/34, rust 21/30.
- Speed: wall clock 13.3 h (01:29–14:46 UTC); avg 838.5 s, median 423.5 s per exercise (4 parallel); ~14.3 solved per hour; ~252 s wall clock per solved exercise. Tokens 1.74 M prompt, 0.38 M completion. Speed test (single request): ~150 tok/s prompt, ~18.5 tok/s decode; 4 concurrent: ~8 tok/s decode each.
- Time to solution: median 6.2 min; 33.8% solved within 5 min, 63.6% within 10 min, 79.1% within 30 min.
- Reading: accuracy on par with DeepSeek thinking ON (85.8%) without thinking, and the best first-try rate so far (58.2%), but slow on this hardware because ~68 GB of expert weights run on the CPU from RAM (GPUs ~10% utilized). Should run several times faster fully GPU-resident (4 GPUs, or a 3-bit build on 2).
- Thinking-ON run skipped (projected far beyond the 20 h cap at this speed); its smoke run was stopped and set aside as ABANDONED-smoke-qwen35-397b-q4km-think.


## DeepSeek-V4.1-Flash-1017 Maya-S IQ2_XXS (~2-bit) on 2 GPUs — retry run (2026-11-21)

- Setup: same 2-bit Maya-S GGUF as the earlier runs, served by the maya-ds4 engine (container `maya`, config maya-ds4-p4.json): `--tp 2` (falls back to a layer split: GPU0 layers 0-17, GPU1 18-39 + head), all 15,360 experts in VRAM (no RAM offload), `--max-context 65536 --parallel 4`, temperature 1.0, thinking OFF per request (`chat_template_kwargs.enable_thinking=false`). VRAM 79.8 / 96.4 GB. Earlier runs: GPU 1 + system RAM.
- Speed test (single request): decode ~72 tok/s (1-GPU clean single stream ~35), prompt 1.5K tok/s (~1K) to 3.5K tok/s (~29K); 4 concurrent ~127 tok/s aggregate.
- Run `until10-deepseek-2gpu-diff-nothink` (aq10.sh), diff, 4 sessions, up to 10 tries: 225 of 225; first try 76 (33.8%); by try 2 155 (68.9%); final 207 (92.0%); 18 unsolved after 10 tries. Solved at try: 1: 76, 2: 79, 3: 31, 4: 7, 5: 6, 6: 3, 7: 4, 8: 1. Average 2.12 tries per solved exercise. 19 malformed, 69 error outputs, 3 context exhaustions, 2 test timeouts.
- Speed: wall clock 2.07 h (15:24:53–17:29:05 UTC) vs 4.2 h for the 1-GPU retry run; ~100 solved per hour; avg 120.5 s, median 52.2 s per exercise. Tokens 6.22 M prompt, 0.41 M completion.
- Time to solution: median 0.8 min; 88.4% solved within 5 min, 90.7% within 10, 92.0% within 30 (1-GPU: 1.6 min, 78.7%, 89.8%, 91.6%).
- Reading: same accuracy, about twice as fast; the fastest route to a correct solution measured so far.

- Standard 2-try run `full-deepseek-2gpu-diff-nothink` (same server, aq10.sh): 225 of 225; first try 79 (35.1%); within two tries 156 (69.3%) vs 68.0% on 1 GPU + RAM; well-formed 94.2% (16 malformed, 19 error outputs, 1 context exhaustion, 2 test timeouts). Per language: cpp 19/26, go 26/39, java 26/47, javascript 36/49, python 27/34, rust 22/30. Wall clock 1.04 h (17:29–18:31 UTC) vs 2.5 h on 1 GPU; avg 59.7 s, median 43.3 s per exercise (1 GPU: 153.1 s avg); ~150 solved per hour. Tokens 2.34 M prompt, 0.26 M completion. Median time to solve 0.6 min.
- Context: the server reports 65,536 tokens. maya-ds4 docs say each conversation under `--parallel` keeps its own KV cache, and a single 29K-token prompt ran with 4 slots configured (it would not fit a 16K share), so 64K is per request, not shared.

## Qwen3-235B-A22B-Thinking-2507 Q8_0 (8-bit) — stopped as impractical on this hardware (2026-11-21)

- Setup: unsloth GGUF Q8_0 (~250 GB), llama.cpp server-cuda, both GPUs, `--n-cpu-moe 40` (40 layers' experts in system RAM), `--tensor-split 2,1`, 4 slots × 32K context, `-b 4096 -ub 2048 --threads 48`, `--reasoning on`. VRAM 82.1 / 85.5 GB. Launcher `~/df-bench/std/llama_up_q235t.sh`.
- Speed test: decode ~6 tok/s single request (6.2 at 1K, 6.0 at 30K); prompt 64 tok/s at ~1K, ~185 tok/s at 16–30K; 4 concurrent ~2.2 tok/s each (~7–9 aggregate).
- Smoke run (5 exercises, diff, 4 sessions, aider timeout 1800 s): 0 of 5 finished after 95 minutes — each thinking turn ran 25–40 minutes (3,000+ reasoning tokens at ~2 tok/s per slot). Projected full run 60–100+ h, far past the 20 h cap, so the run was stopped and no accuracy score exists. Partial folder kept: `2026-11-21-19-24-36--smoke-qwen3-235b-think-q8`.
- Reading: an 8-bit 235B thinking model needs to be fully GPU-resident (~250 GB → 4× 96 GB GPUs) to be usable; on 2 GPUs with ~half the experts in RAM it is ~12x slower than DeepSeek 2-bit on 2 GPUs (6 vs 72 tok/s).


## Qwen3.8-27B NVFP4 (4-bit) — thinking OFF (2026-11-21)

- Setup: nvidia/Qwen3.8-27B-NVFP4 (19.9 GiB weights), vLLM (image vllm/vllm-openai:qwen38), GPU 0 only, same flags as the FP8 runs (`--max-model-len 262144 --max-num-seqs 4 --reasoning-parser qwen3`). Load ~13 min (FP4 kernel autotuning). Chain aq12.sh.
- Speed test: decode 66.5 tok/s single (~1K prompt), 64.1 at ~16K; prompt ~7,265 tok/s at ~16K; 4 concurrent ~59 tok/s each, ~237 aggregate.
- Result (225 of 225, diff, 4 sessions): first try 38 (16.9%), within two tries 96 (42.7%), well-formed 90.7% (25 malformed, 26 error outputs, 1 context exhaustion, 2 test timeouts). Per language: cpp 11/26, go 13/39, java 17/47, javascript 24/49, python 17/34, rust 14/30.
- Speed: wall clock 1.23 h (21:23–22:37 UTC); avg 72.5 s, median 43.9 s per exercise; ~78 solved per hour. Tokens 3.82 M prompt, 0.65 M completion. Median time to solve 0.5 min.
- Precision comparison, thinking OFF: BF16 50.2%, FP8 50.7%, NVFP4 42.7% — 4-bit costs about 8 points on this 27B dense model, while 8-bit costs nothing measurable. It also produced more malformed edits (25 vs ~0 for FP8).


## Qwen3.8-27B NVFP4 (4-bit) — thinking ON (2026-11-22)

- Setup: nvidia/Qwen3.8-27B-NVFP4, vLLM (image vllm/vllm-openai:qwen38), GPU 0 only, thinking ON (`--reasoning-parser qwen3`), Aider Polyglot 225, diff format, 2 tries. Run folder `2026-11-21-22-44-16--full-qwen38-nvfp4-diff-thinking` (run name `full-qwen38-nvfp4-diff-thinking`).
- Result (225 of 225): solved 71.1% (160/225), 2-try 71.1%. Error outputs 4, malformed 3, exhausted context 1, test timeouts 0. Per language passed/total: cpp 17/26, go 27/39, java 28/47, javascript 37/49, python 28/34, rust 23/30.
- Time to solution: median 3.3 min; solved within 5 min 42.7%, within 10 min 63.6%, within 30 min 68.9%.
- Speed: wall clock 22:44:02 to 05:27:24 UTC (6h43m).
- 4-bit vs 8-bit vs 16-bit Qwen3.8-27B: thinking ON, NVFP4 71.1% vs FP8 69.3% (median 3.3 vs 4.0 min; within 5 min 42.7% vs 39.1%; within 10 min 63.6% vs 53.3%; within 30 min 68.9% both). Thinking OFF: NVFP4 42.7%, FP8 50.7%, BF16 50.2%. With thinking on, 4-bit matched or beat FP8 and was faster; with thinking off it lost about 8 points. BF16 thinking ON: 75.1% (median 7.3 min), see the BF16 section below.


## Qwen3.8-Flash-Next Q8_0 on Strata 0.1.64 — thinking OFF, retry run (2026-11-22)

- Setup: Qwen3.8-Flash-Next Unsloth Q8_0 GGUF (54.4 GB), Strata engine 0.1.64 (prebuilt, CUDA), GPU 0 only plus system RAM, 64k context, one request at a time (`--parallel 1`, so 1 benchmark thread), vision off, thinking OFF per request via the Aider settings file. Aider Polyglot 225, diff format, retry run (`--tries 10`). Run folder `2026-11-22-07-02-11--until10-qfn-strata-diff-nothink`.
- Speed test (2K-token prompt): prefill about 1.4-1.5K tok/s, decode about 190-206 tok/s.
- Result (225 of 225): solved 89.8% (202/225); first try 78 (34.7%); the first two tries alone gave 73.8%. Error outputs 71, malformed 10, exhausted context 3, test timeouts 14. Per language solved/total: cpp 23/26, go 35/39, java 38/47, javascript 44/49, python 34/34, rust 28/30. (Per-language counts are from the aggregation script's final pass/fail, which counts any pass within the 10 tries.)
- Time to solution: median 0.2 min; solved within 5, 10 and 30 min all 89.8% (every solve finished inside 5 minutes; the remaining 10.2% were never solved).
- Speed: wall clock 07:01:56 to 10:25:50 UTC (3h24m); total duration 2.29 h, average 36.7 s per exercise; 6.99 M prompt tokens, 0.99 M completion tokens.
- Comparison with the earlier best retry run, Qwen3.8-27B FP8 thinking OFF (`until10-qwen38-fp8-diff-nothink`): 84.4% solved, 2-try 48.0%, median 1.1 min. Flash-Next on Strata is now the best time-to-solution result on this hardware (89.8% solved, 73.8% in the first two tries, median 0.2 min). DeepSeek-V4.1-Flash 2-bit still solves more in total (92.0%) on a retry run.
- License: Qwen Community License 1.0. Commercial use is allowed; offering the model as an AI work assistant or model-as-a-service to third parties needs a separate license.
- Next: the standard 2-try run (`full-qfn-strata-diff-nothink`) is recorded below.


## Qwen3.8-Flash-Next Q8_0 on Strata 0.1.64 — thinking OFF, standard 2-try run (2026-11-22)

- Setup: same as the retry run above (Strata 0.1.64 prebuilt, GPU 0 plus system RAM, 64k context, 1 thread, thinking OFF). Aider Polyglot 225, diff format, standard 2 tries. Run folder `2026-11-22-10-47-45--full-qfn-strata-diff-nothink`.
- Result (225 of 225): passed within two tries 74.2% (167/225); first try 79 (35.1%). Error outputs 12, malformed 10, exhausted context 0, test timeouts 2. Per language passed/total: cpp 20/26, go 27/39, java 32/47, javascript 37/49, python 31/34, rust 20/30.
- Time to solution: median 0.2 min; solved within 5, 10 and 30 min all 74.2%.
- Speed: wall clock 10:47:30 to 12:31:03 UTC (1h44m); total duration 1.36 h, average 21.7 s per exercise; 2.87 M prompt tokens, 0.57 M completion tokens.
- Comparison: the 2-try run reproduces the first-two-tries number of the retry run (74.2% vs 73.8%), so the retry run's 89.8% is the same model given up to 10 tries. Thinking ON on the same server is next (`full-qfn-strata-diff-thinking`).


## Qwen3.8-Flash-Next Q8_0 on Basalt v0.5.5 — thinking OFF, retry run (2026-11-22)

- Setup: same Unsloth Q8_0 weights converted to a 179 GiB `.basalt` pack; Basalt v0.5.5 prebuilt; GPU 1 only plus system RAM (92 GiB VRAM, 33 GiB RAM); 64k context; 1 thread; thinking OFF. Aider Polyglot 225, diff format, retry run (`--tries 10`). Run folder `2026-11-22-19-59-22--until10-qfn-basalt-diff-nothink`.
- Wall clock 19:59 → 22:39 UTC (2h40m). Speed (~2k prompt, warm): prefill ~1.36k tok/s, decode ~224 tok/s.
- Result: solved 90.7% (204/225); first try 38.2%; first two tries 75.1%; median time to solve 0.2 min; every solve within 5 minutes.
- Per language (solved/total): cpp 24/26, go 34/39, java 41/47, javascript 43/49, python 34/34, rust 28/30. Error outputs 54, malformed 8, exhausted context 2, test timeouts 2.
- Strata vs Basalt on the same model: Strata 89.8% (2-try 73.8%) in 3h24m; Basalt 90.7% (75.1%) in 2h40m — ~22% faster with equal or better accuracy.

## Qwen3.8-Flash-Next Q8_0 on Basalt v0.5.5 — thinking OFF, standard 2-try run (2026-11-23)

- Setup: same as the Basalt retry run (GPU 1 + RAM, 64k context, `--parallel 1`, 1 thread). Run folder `2026-11-22-23-41-45--full-qfn-basalt-diff-nothink`. Wall clock 23:41 → 01:21 UTC (1h40m).
- Result: 72.0% within two tries, median time to solve 0.2 min. Strata's 2-try run on the same weights: 74.2% in 1h44m. The two engines are within run-to-run noise on 2-try accuracy (Basalt's retry run gave 75.1% in its first two tries); Basalt is slightly faster.

## Qwen3.8-27B BF16 (16-bit) — thinking ON (2026-11-22)

- Setup: Qwen3.8-27B BF16 (full precision), vLLM, GPU 1 only, thinking ON, Aider Polyglot 225, diff format, 2 tries. Run folder `2026-11-22-02-58-31--full-qwen38-bf16-diff-thinking` (run name `full-qwen38-bf16-diff-thinking`).
- Run history: started 02:58 UTC, interrupted at 05:36 UTC after 59 exercises by a container-name collision, then resumed with `--cont` from 06:32 to 19:12 UTC. Total active time about 15h20m.
- Result (225 of 225): solved 75.1% (169/225); first try 74 (32.9%). Error outputs 7, malformed 2, exhausted context 1, test timeouts 0. Per language passed/total: cpp 20/26, go 28/39, java 31/47, javascript 40/49, python 25/34, rust 25/30.
- Time to solution: median 7.3 min; solved within 5 min 27.1%, within 10 min 45.3%, within 30 min 68.4%.
- Speed: total per-exercise duration 57.5 h summed over exercises (average 920.7 s per exercise); 2.65 M prompt tokens, 3.29 M completion tokens.
- 4-bit vs 8-bit vs 16-bit Qwen3.8-27B, thinking ON: NVFP4 71.1% (median 3.3 min), FP8 69.3% (4.0 min), BF16 75.1% (7.3 min). 16-bit is about 4-6 points more accurate but about 2x slower to a correct answer; 4-bit is the fastest.
