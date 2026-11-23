# Inference engines: what we tested, and why we're building our own

*Draft — 2026-11-21. Engine name: **Caldera** (named for the volcanic source of basalt; MIT-licensed, working repo name `aimos-caldera`).*

Our benchmark results (see [README.md](README.md)) kept pointing at the same thing: on local hardware, **the engine matters as much as the model**. The same 2-bit DeepSeek build solved 88% of exercises within 5 minutes on one engine setup and 79% on another, and the same 397B model ran at 18 tok/s with part of it in system RAM versus an expected 3–5× that fully on GPU. This page compares the engines we use or are evaluating, and explains what our own engine will do differently.

## The engines

| Engine | What it is | Models | Where it shines | Where it falls short for us |
|---|---|---|---|---|
| [llama.cpp](https://github.com/ggml-org/llama.cpp) | The general-purpose GGUF engine; CPU+GPU, every quant format | Almost all | Runs anything; MoE expert offload (`--n-cpu-moe`) lets models larger than VRAM run at all | Offloads whole layers' experts, not the hot ones; slow when experts live in RAM (Qwen3.5-397B: ~18 tok/s, GPUs ~10% busy) |
| [vLLM](https://github.com/vllm-project/vllm) | High-throughput production server | Most HF checkpoints; FP8/NVFP4 on Blackwell | Fastest when the whole model fits in VRAM; batching, prefix caching | Needs the model fully in VRAM; new architectures need dedicated images (Qwen3.8-Flash-Next: `vllm/vllm-openai:qwen38-flash-next`) |
| [SGLang](https://github.com/sgl-project/sglang) | High-throughput server, strong on structured/agentic workloads | Most HF checkpoints | Day-0 support for new models | Same VRAM constraint as vLLM (not yet benchmarked here) |
| [Project Maya](https://github.com/mw00/project-maya) | Engine for very large MoE models on a few GPUs | DeepSeek, GLM, MiniMax, Qwen3.8-Flash-Next | Expert placement by available VRAM; fair scheduling across parallel requests; per-request context | Ran our 2-bit DeepSeek fully on 2 GPUs at ~72 tok/s — the best time-to-solution result so far |
| [Strata](https://github.com/Niko1221/Strata) | Single-model engine for Qwen3.8-Flash-Next, built on llama.cpp/ggml | Qwen3.8-Flash-Next only | Hot experts in VRAM, cold in RAM/SSD, CPU computes missing experts in parallel; MTP speculative decoding; one-click install | One model; tuned for 12–24 GB consumer GPUs |
| [Basalt](https://github.com/jesdga95/basalt) | Strata fork tuned for NVIDIA Blackwell | Qwen3.8-Flash-Next only | Blackwell (sm_120) kernels, second GPU as a peer expert tier, single-file `.basalt` packs; author reports 2.6× Strata on a 5090 + 5060 Ti | One model; context shared across parallel slots; one developer, early |

## What we learned that shapes Caldera

1. **Fit in VRAM beats everything.** Fully GPU-resident runs were 4–12× faster than RAM-offloaded ones on the same machine.
2. **Big MoE models tolerate aggressive quantization; small dense models don't.** 2-bit DeepSeek still scored 69%; Qwen3.8-27B lost 8 points from 8-bit to 4-bit.
3. **Time to a correct solution favors fast models that retry over slow "thinking" models.** DeepSeek with thinking off and test feedback solved 88% within 5 minutes; with thinking on, 30%.
4. **Malformed edits are a hidden cost.** One run lost a large share of its score to 62 broken responses, not wrong answers.

## How Caldera will be different

> **Other engines optimize a model. Caldera optimizes the solution:** a suite of models working together, measured by how fast a task ends in correct, tested code.

**The goal is wall-clock time to the right answer — not tokens per second, and not the 2-try leaderboard score.** Every other engine here optimizes how fast a model *generates*. Caldera optimizes how fast a task gets *solved*: correct, tested code, measured as the share of tasks solved within 5, 10 and 30 minutes. Every design choice below serves that one number.

**Headline metric:** median time to solve on Aider Polyglot (same model, same weights, same hardware), Caldera vs the best other engine — currently Basalt at 0.2 min (about 12 s) for Qwen3.8-Flash-Next. Total run time, 90th-percentile time to solve and solved per hour are reported alongside.

- **Blackwell only, tuned to the box it runs on:** Caldera requires an NVIDIA Blackwell GPU (native FP4/FP8 tensor cores) and drops pre-Blackwell code paths — but it is not locked to one card. At startup it probes the machine (GPU count and VRAM, PCIe generation and lanes per card, peer-to-peer/NVLink, system RAM size and bandwidth, NVMe) and plans for that configuration: which experts live on which GPU, what spills to RAM or SSD, KV-cache size, how many parallel attempts to run. Reference systems: our T7920 (2× RTX PRO 6000 Blackwell Max-Q, PCIe 3.0, 512 GB DDR4) and the planned next build (PCIe 5.0, ≥1.5 TB RAM); other Blackwell setups (RTX PRO 6000 Workstation, RTX 5090, mixed cards) should run correctly, just tuned by the same planner.
- **A suite of models that work together, not one model:** Caldera loads a team — coder, primary reviewer, secondary reviewer, escalation model — keeps them resident across the machine's GPUs, and routes each task through them to optimize accuracy and median time to solve together. Strata and Basalt each run one model. First version: one scheduler and API in front of per-model backends (Basalt-derived for Qwen3.8-Flash-Next, Maya-derived for DeepSeek), then shared kernels, memory planning and prompt cache across the suite.
- **Expert placement learned from coding work:** profile which experts our coding prompts actually use and keep those GPU-resident, instead of offloading by layer.
- **Coding-calibrated quantization:** importance matrices built from coding prompts, not generic text.
- **A built-in coder→reviewer cascade:** Qwen3.8-Flash-Next is the coder and the primary reviewer (fastest: ~240–330 tok/s on one GPU); DeepSeek-V4.1-Flash is the secondary reviewer, brought in when Qwen stalls (it solved 14 exercises Flash-Next never solved in 10 tries; together they cover 218/225 = 96.9%). Starting cascade, to be tuned in phase 2: tries 1–2 Qwen codes with test feedback; tries 3–4 Qwen reviews (diagnoses the failing test) and fixes; from try 5 DeepSeek reviews. The switch point is configurable.
- **Prompt cache (required):** reuse the processed prompt across requests — any shared prefix, including checkpoints at the point where a retry's prompt diverges, which Basalt v0.5.5 cannot do (it reused 0 tokens on our retries). Paired with a harness that puts the stable parts of the prompt first.
- **Faster retries, not just faster tokens:** run several attempts in parallel and keep the first that passes tests; reuse the prompt's processed context across retries instead of re-reading it.
- **Benchmark-driven:** every change is measured with the harness in this repo (accuracy, time to solution, solved per hour), against the engines above, on the same model.

## Status

Plan (2026-11-22): finish the benchmark queue (Flash-Next on Maya and vLLM NVFP4, Laguna, Qwen3-Coder-480B), then re-test every model on Caldera, then test the suite end to end (coder → Qwen review → DeepSeek review) against the single-model results.


First same-model result: Qwen3.8-Flash-Next Q8_0 retry run — Basalt 90.7% in 2h40m vs Strata 89.8% in 3h24m (see RESULTS.md). Next: Maya and vLLM (NVFP4), same tests. Caldera's design will follow those results; its first version will likely be a fork of one of these engines rather than a from-scratch rewrite.
