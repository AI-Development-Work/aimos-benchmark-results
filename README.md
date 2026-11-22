# AiMOS Local LLM Coding Benchmark Results

Standardized [Aider Polyglot](https://aider.chat/docs/leaderboards/) benchmark runs
of open-weight LLMs, self-hosted on owned hardware. This repo is a running record —
hardware and the model roster will change over time; each result row is tagged with
the hardware config and date it was run under.

## Headline: time to a correct solution

What developers actually care about is how fast they get working code, not how many tries a model needs. This table scores every run on **wall-clock time to a correct solution**: the share of all 225 exercises solved within 5, 10 and 30 minutes of starting, all tries included. The standard leaderboard number (pass within 2 tries) is shown alongside for comparison.

| Run | Leaderboard score (2 tries) | Solved (final) | Median time to solve | Solved within 5 min | within 10 min | within 30 min |
|---|---|---|---|---|---|---|
| **DeepSeek-V4.1-Flash (2-bit), thinking OFF — retry run, 2 GPUs** | 68.9% | **92.0%** | **0.8 min** | **88.4%** | **90.7%** | **92.0%** |
| DeepSeek-V4.1-Flash, thinking OFF — retry run (up to 10 tries), 1 GPU + RAM | 72.0% | **92.0%** | 1.6 min | **78.7%** | **89.8%** | 91.6% |
| Qwen3.8-27B FP8, thinking OFF — retry run (up to 10 tries) | 48.0% | 84.4% | 1.1 min | 74.7% | 82.7% | 84.4% |
| DeepSeek-V4.1-Flash, thinking ON (2 tries) | **85.8%** | 85.8% | 8.8 min | 30.2% | 45.8% | 73.8% |
| Qwen3.5-397B-A17B Q4_K_M, thinking OFF (2 tries) | 84.4% | 84.4% | 6.2 min | 33.8% | 63.6% | 79.1% |
| Qwen3.8-27B NVFP4 (4-bit), thinking ON (2 tries) | 71.1% | 71.1% | 3.3 min | 42.7% | 63.6% | 68.9% |
| Qwen3.8-27B FP8, thinking ON (2 tries) | 69.3% | 69.3% | 4.0 min | 39.1% | 53.3% | 68.9% |
| DeepSeek-V4.1-Flash (2-bit), thinking OFF (2 tries), 2 GPUs | 69.3% | 69.3% | 0.6 min | 69.3% | 69.3% | 69.3% |
| DeepSeek-V4.1-Flash, thinking OFF (2 tries), 1 GPU + RAM | 68.0% | 68.0% | 1.7 min | 61.3% | 67.1% | 68.0% |
| Qwen3-235B-A22B-Instruct-2507 NVFP4 (2 tries) | 53.8% | 53.8% | 0.7 min | 53.3% | 53.8% | 53.8% |
| gpt-oss-120b (2 tries) | 53.3% | 53.3% | 0.7 min | 52.4% | 52.9% | 53.3% |
| Qwen3.8-27B FP8, thinking OFF (2 tries) | 50.7% | 50.7% | 0.8 min | 48.4% | 50.7% | 50.7% |
| Qwen3.8-27B BF16, thinking OFF (2 tries) | 50.2% | 50.2% | 1.3 min | 43.1% | 48.4% | 50.2% |
| Qwen3.8-27B NVFP4 (4-bit), thinking OFF (2 tries) | 42.7% | 42.7% | 0.5 min | 42.2% | 42.7% | 42.7% |
| Mistral Small 4 119B NVFP4 (2 tries) | 15.1% | 15.1% | 0.2 min | 15.1% | 15.1% | 15.1% |
| Devstral Small 2 24B (2 tries) | 13.8% | 13.8% | 0.4 min | 13.8% | 13.8% | 13.8% |

**2 GPUs vs 1:** the same 2-bit DeepSeek build moved from 1 GPU + system RAM to fully on both GPUs went from 78.7% to 88.4% solved within 5 minutes, with the median time to solve halved (1.6 → 0.8 min), at the same final accuracy (92.0%).

**4-bit vs 8-bit vs 16-bit Qwen3.8-27B:** with thinking ON, 4-bit NVFP4 matched or beat FP8 (71.1% vs 69.3%) and was faster (median 3.3 vs 4.0 min; 42.7% vs 39.1% solved within 5 min). With thinking OFF, 4-bit lost about 8 points (42.7% vs 50.7% FP8, 50.2% BF16). BF16 thinking ON: pending (run in progress).

**What it shows:** a fast model that retries against test feedback gets to working code sooner than a slow "thinking" model. DeepSeek with thinking off and retries solves 79% of exercises within 5 minutes; the same model with thinking on solves 30% in that time, despite the higher leaderboard score. The two "retry run" rows are separate runs from the standard 2-try runs of the same model.

*How measured:* per-exercise wall-clock time, 4 exercises running in parallel on the same hardware (so times are under load), self-hosted on a Dell T7920 with 2× RTX PRO 6000 Blackwell Max-Q. Script and raw results: see [RESULTS.md](RESULTS.md).


> **Engines:** how llama.cpp, vLLM, SGLang, Maya, Strata and Basalt compare, and how our own engine, **Caldera**, will optimize for time to the right answer — see [ENGINES.md](ENGINES.md).

## Methodology

- Benchmark: Aider Polyglot — 225 coding exercises (from [Exercism](https://exercism.org)),
  six languages (C++, Go, Java, JavaScript, Python, Rust).
- Aider commit: `5dc9490`.
- Edit format: `diff` for every run reported here, to stay comparable with the
  [published Aider leaderboard](https://aider.chat/docs/leaderboards/), which also
  scores on the `diff` edit format.
- Scoring: standard two-try scoring (pass on first try / pass within two tries),
  as the published leaderboard does. A separate "work until correct" table (up to
  10 tries per exercise) is included for cost/time tradeoff analysis — it is
  explicitly NOT comparable to the two-try numbers.
- Serving stack: vLLM, each model in its own Docker container, run one at a time
  against the benchmark harness.

## Test environment (as of 2026-11-20)

- Dell Precision T7920 Tower
- Dual Intel Xeon Platinum 8168 CPUs (Cascade Lake)
- 512 GB DDR4 Registered ECC RAM (verified via `dmidecode`)
- 2x NVIDIA RTX PRO 6000 Blackwell Max-Q (300W variant), 96 GB VRAM each

## Results summary (two-try scoring, `diff` edit format)

| Model | First try | Within two tries | Well-formed | Sec/exercise |
|---|---|---|---|---|
| DeepSeek-V4.1-Flash-1017 (thinking ON) | 37.8% | **85.8%** | 98.7% | 1109.5 |
| Qwen3.5-397B-A17B Q4_K_M (llama.cpp, thinking OFF) | 58.2% | 84.4% | 97.8% | 838.5 |
| Qwen3.8-27B FP8 (thinking ON) | 32.0% | 69.3% | 100% | 417.1 |
| DeepSeek-V4.1-Flash-1017 2-bit, 2 GPUs (thinking OFF) | 35.1% | 69.3% | 94.2% | 59.7 |
| DeepSeek-V4.1-Flash-1017 (thinking OFF) | 32.0% | 68.0% | n/a | 153.1 |
| Qwen3-235B-A22B-Instruct-2507 NVFP4 (non-thinking) | 20.9% | 53.8% | 80.4% | 65.3 |
| gpt-oss-120b | 15.6% | 53.3% | 91.6% | 55.6 |
| Qwen3.8-27B FP8 (thinking OFF) | 16.0% | 50.7% | n/a | 108.4 |
| Qwen3.8-27B full precision BF16 (thinking OFF) | 17.3% | 50.2% | n/a | 171.2 |
| Qwen3.8-27B NVFP4 4-bit (thinking OFF) | 16.9% | 42.7% | 90.7% | 72.5 |
| Mistral Small 4 119B NVFP4 | 4.4% | 15.1% | 93.8% | 23.6 |
| Devstral Small 2 24B | 3.6% | 13.8% | n/a | 43.7 |

Full detail (per-language breakdown, token counts, error/timeout counts, notes) is
in [`RESULTS.md`](./RESULTS.md).

## For reference: published Aider leaderboard (frontier hosted models)

Pulled from [aider.chat/docs/leaderboards](https://aider.chat/docs/leaderboards/) for
context — same benchmark and edit format, but run on Aider-AI's own infrastructure
against hosted/API models, not self-hosted open-weight models on owned hardware.
Not an apples-to-apples cost or speed comparison; same scoring methodology.

| Model | Within two tries |
|---|---|
| GPT-5 (high) | 88.0% |
| o3-pro (high) | 84.9% |
| o3 (high) | 81.3% |
| Grok-4 (high) | 79.6% |
| DeepSeek-V3.2-Exp (Reasoner) | 74.2% |
| Claude Opus 4 (32k thinking) | 72.0% |
| Claude 3.7 Sonnet (32k thinking) | 64.9% |
| Claude Sonnet 4 (32k thinking) | 61.3% |
| DeepSeek-V3 (0324) | 55.1% |

Source: [aider.chat/docs/leaderboards](https://aider.chat/docs/leaderboards/), pulled 2026-11-20.

## Suggestions welcome

Open to suggestions for other open-weight coding models worth running on this
hardware class (dual 96GB GPUs, ~192GB usable VRAM total). Open an issue or drop
a note.

## Repo contents

- `README.md` — this file
- `RESULTS.md` — full detail: per-language breakdown, token counts, error/timeout
  counts, notes on invalid/repeated runs
- `logs/` — raw per-run log files (aggregate summaries; per-exercise container
  artifacts were not preserved for these runs — see note in RESULTS.md)
