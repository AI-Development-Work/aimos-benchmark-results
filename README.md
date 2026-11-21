# AiMOS Local LLM Coding Benchmark Results

Standardized [Aider Polyglot](https://aider.chat/docs/leaderboards/) benchmark runs
of open-weight LLMs, self-hosted on owned hardware. This repo is a running record —
hardware and the model roster will change over time; each result row is tagged with
the hardware config and date it was run under.

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
| Qwen3.8-27B FP8 (thinking ON) | 32.0% | 69.3% | 100% | 417.1 |
| DeepSeek-V4.1-Flash-1017 (thinking OFF) | 32.0% | 68.0% | n/a | 153.1 |
| Qwen3-235B-A22B-Instruct-2507 NVFP4 (non-thinking) | 20.9% | 53.8% | 80.4% | 65.3 |
| gpt-oss-120b | 15.6% | 53.3% | 91.6% | 55.6 |
| Qwen3.8-27B FP8 (thinking OFF) | 16.0% | 50.7% | n/a | 108.4 |
| Qwen3.8-27B full precision BF16 (thinking OFF) | 17.3% | 50.2% | n/a | 171.2 |
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
