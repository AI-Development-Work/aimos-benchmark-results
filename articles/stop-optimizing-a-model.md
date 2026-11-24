# Escalation on failure: a two-model local cascade solves 219 of 225 Aider Polyglot exercises

*Brian K. Hudes, MD · AiMOS Systems · 24 November 2026*

*Preliminary. Two full runs of the cascade (the second an unchanged repeat, added 24 November). A matched single-model baseline and a run without the second model were added the same day (see Matched baseline and ablation). Technical companion to "Stop Optimizing a Model. Solve the Problem."*

## Summary

Two open-weight models on one workstation, run as a fixed escalation cascade, solved 219 of 225 Aider Polyglot exercises (97.3%) in at most 8 tries per exercise. The median time to a passing solution was 11.5 s. The same fast model alone, given 10 tries, solved 204 (90.7%). The second model alone, given 10 tries, solved 207 (92.0%).

The cascade is four fast tries from the coder, two tries from the same coder with reasoning on, then two tries from a second model with reasoning on. It stops at the first passing test run.

Three points are worth a technical reader's time:

1. The per-attempt success rate of fast retries decays quickly (60% on try 2, 20% on try 4). Switching the same model to reasoning mode on try 5 brought it back to 46%.
2. Reasoning mode accounts for 20 of the 22 solves after try 4. The second model accounts for 2. This run supports mode switching. It does not yet support model switching.
3. On the leaderboard's two-try rule the cascade scores 75.1%. The 97.3% is a work-until-correct number and is not comparable with leaderboard scores.

## Setup

| Item | Value |
|---|---|
| Benchmark | Aider Polyglot, 225 Exercism exercises (C++ 26, Go 39, Java 47, JavaScript 49, Python 34, Rust 30) |
| Harness | aider commit `5dc9490`, `diff` edit format, 1 benchmark thread |
| Harness change | Chat-history summaries off (see Confounds) |
| Machine | Dell Precision T7920, dual Xeon Platinum 8168, 512 GB DDR4 ECC |
| GPUs | 2x NVIDIA RTX PRO 6000 Blackwell Max-Q, 96 GB each, PCIe 3.0 |
| Coder | Qwen3.8-Flash-Next, Unsloth Q8_0, as a 179 GiB `.basalt` pack on Basalt v0.5.5, GPU 0 plus system RAM, 64k context |
| Second model | DeepSeek-V4.1-Flash-1017, Maya-S IQ2_XXS (about 2-bit), on the Maya engine, GPU 1 |
| Run folder | `2026-11-23-23-26-13--full-team-qfn-think-ds-nosum-diff-1123-2325` |

Both models stay loaded for the whole run, one per card. Nothing leaves the machine.

Measured single-request speeds from earlier runs on this hardware: Flash-Next on Basalt reads prompts at about 1.36k tok/s and decodes at 132 to 141 tok/s, or 238 to 328 tok/s with speculative decoding (8-token drafts, 74 to 92% accepted). DeepSeek 2-bit on Maya decodes at about 35 tok/s on one card and about 72 tok/s across two.

## The cascade

| Tries | Model | Mode | Engine | Placement |
|---|---|---|---|---|
| 1 to 4 | Qwen3.8-Flash-Next Q8_0 | thinking off | Basalt v0.5.5 | GPU 0 + RAM |
| 5 and 6 | Qwen3.8-Flash-Next Q8_0 | thinking on | Basalt v0.5.5 | GPU 0 + RAM |
| 7 and 8 | DeepSeek V4.1-Flash 2-bit | thinking on | Maya | GPU 1 |

Each try after the first sees the failing test output, as in the standard benchmark.

The ordering came from the single-model runs. Flash-Next with thinking off had the shortest time to a correct answer of anything tested (median about 12 s). With thinking always on, the same model scored 85.8% on two tries, but the median rose to 2.5 min and the run took 14 h 22 min. Reasoning is worth its cost only on the exercises that fast mode cannot solve, so it sits behind four fast tries.

Stage hand-off, as configured for this run:

- **Fast to thinking (same model):** the chat is kept. The thinking tries see the earlier attempts and their test output.
- **Flash-Next to DeepSeek:** a fresh chat. DeepSeek receives a brief with the original task, a one-line list of earlier attempts and the latest test output. The solution files are passed in their current state.
- **Sampling:** temperature 0 to both models in every stage (aider's default). No top_p is sent, so each server's own value applies (0.95 on Basalt, 1.0 on Maya).
- **Request timeouts:** 600 s for fast tries, 1800 s for Flash-Next thinking, 3600 s for DeepSeek. There is no per-exercise time cap beyond the 8-try limit and a 3-minute test timeout.

## Results

| Measure | Cascade (8 tries) | Flash-Next alone (10 tries) | DeepSeek alone (10 tries) |
|---|---|---|---|
| Solved | 219 / 225 (97.3%) | 204 / 225 (90.7%) | 207 / 225 (92.0%) |
| Solved within 2 tries | 169 (75.1%) | 169 (75.1%) | 155 (68.9%) |
| Median time to solve | 11.5 s | 13.6 s | 48 s |
| Wall clock | 3 h 39 min | 2 h 40 min | 2 h 04 min (4 sessions, both GPUs) |

Baselines: `until10-qfn-basalt-diff-nothink` (Basalt, one GPU plus RAM, 1 thread) and `until10-deepseek-2gpu-diff-nothink` (Maya, both GPUs, 4 sessions).

Time to solve for the cascade: mean 32.1 s, 90th percentile 81.6 s among solved exercises. Of all 225 exercises, 39.1% were solved within 10 s, 73.8% within 30 s and 96.4% within 5 min. There were no infrastructure errors and no timeouts.

### Per-try yield

"Started" is the number of exercises still unsolved when that try began. It is derived from the per-try solve counts and assumes every unsolved exercise went on to the next try, which holds for a run without errors.

| Try | Stage | Started | Solved | Attempt success rate | Cumulative solved |
|---|---|---|---|---|---|
| 1 | Flash-Next, fast | 225 | 85 | 37.8% | 85 (37.8%) |
| 2 | Flash-Next, fast | 140 | 84 | 60.0% | 169 (75.1%) |
| 3 | Flash-Next, fast | 56 | 21 | 37.5% | 190 (84.4%) |
| 4 | Flash-Next, fast | 35 | 7 | 20.0% | 197 (87.6%) |
| 5 | Flash-Next, thinking | 28 | 13 | 46.4% | 210 (93.3%) |
| 6 | Flash-Next, thinking | 15 | 7 | 46.7% | 217 (96.4%) |
| 7 | DeepSeek, thinking | 8 | 1 | 12.5% | 218 (96.9%) |
| 8 | DeepSeek, thinking | 7 | 1 | 14.3% | 219 (97.3%) |

The run used 514 attempts in total: 456 fast, 43 Flash-Next thinking and 15 DeepSeek. That is 2.28 attempts per exercise. Only 58 attempts (11%) used reasoning.

### Where the wall clock went

The 219 solved exercises account for about 117 minutes (219 x 32.1 s). The six unsolved exercises took 78 minutes of model and test time between them. The rest of the 219-minute run is harness overhead between exercises.

| Unsolved exercise | Time across all 8 tries |
|---|---|
| go/robot-simulator | 27 min 12 s (4 test timeouts) |
| java/hangman | 19 min 20 s |
| java/rational-numbers | 14 min 26 s |
| java/zipper | 14 min 24 s |
| cpp/kindergarten-garden | 1 min 40 s |
| cpp/spiral-matrix | 1 min 00 s |

About a third of the run went to six exercises that were never solved, and four of them account for nearly all of it. A time budget on the reasoning stages is the obvious next control.

![Time to a correct solution, all runs](../images/time_to_solution.png)

## Replication

The cascade was run a second time with nothing changed (same configuration, harness commit, models and servers; the benchmark container image was rebuilt from the same build file after a routine cleanup removed it).

| Measure | Run 1 | Run 2 (repeat) |
|---|---|---|
| Solved | 219 / 225 (97.3%) | 219 / 225 (97.3%) |
| Solved within 2 tries | 169 (75.1%) | 161 (71.6%) |
| Median time to solve | 11.5 s | 12.8 s |
| Mean / 90th percentile | 32.1 s / 81.6 s | 39.8 s / 56.9 s |
| Wall clock | 3 h 39 min | 3 h 26 min |
| Solved by Flash-Next, fast (tries 1-4) | 197 | 200 |
| Solved by Flash-Next, thinking (tries 5-6) | 20 | 14 |
| Solved by DeepSeek (tries 7-8) | 2 | 5 |
| Infrastructure errors | 0 | 0 |

Paired by exercise: 217 solved in both runs, 2 solved only in run 1 (cpp/grade-school, rust/xorcism), 2 solved only in run 2 (java/hangman, java/zipper), and 4 unsolved in both (cpp/kindergarten-garden, cpp/spiral-matrix, go/robot-simulator, java/rational-numbers). Across the two runs, 221 of the 225 exercises were solved at least once.

Per-try yield in the repeat:

| Try | Stage | Started | Solved | Attempt success rate |
|---|---|---|---|---|
| 1 | Flash-Next, fast | 225 | 83 | 36.9% |
| 2 | Flash-Next, fast | 142 | 78 | 54.9% |
| 3 | Flash-Next, fast | 64 | 31 | 48.4% |
| 4 | Flash-Next, fast | 33 | 8 | 24.2% |
| 5 | Flash-Next, thinking | 25 | 12 | 48.0% |
| 6 | Flash-Next, thinking | 13 | 2 | 15.4% |
| 7 | DeepSeek, thinking | 11 | 3 | 27.3% |
| 8 | DeepSeek, thinking | 8 | 2 | 25.0% |

What held and what did not:

- **The headline held.** The same number of exercises was solved, and only 4 of 225 final outcomes differed between runs. The final result is much more stable than the first-two-try score, which moved by 3.5 points (75.1% to 71.6%).
- **The decay of fast retries held** in both cascade runs (about 20 to 24% by try 4), and so did the recovery on the first thinking try (46% and 48%). The later run without a second model showed the same direction with a smaller step: 29% on try 4 and 38% on the first thinking try.
- **The second thinking try did not hold.** It solved 7 of 15 in run 1 and 2 of 13 in the repeat. The first thinking try carries most of the benefit.
- **DeepSeek's share rose from 2 to 5.** Thinking mode plus the second model solved 22 in run 1 and 19 in the repeat, but the split between them moved. The evidence for a separate benefit from the second model is still thin; the run without DeepSeek, now in progress, addresses it.

## Matched baseline and ablation

Two further runs, both with the cascade's exact settings (chat-history summaries off, 1 thread, same harness, same Basalt server):

- **Matched baseline:** Flash-Next alone, thinking off, up to 10 tries.
- **No second model:** Flash-Next with four fast tries, then four thinking tries. DeepSeek is not used.

| Measure | Cascade, run 1 | Cascade, run 2 | No second model (4 fast + 4 thinking) | Matched baseline (10 fast) |
|---|---|---|---|---|
| Solved | 219 (97.3%) | 219 (97.3%) | 216 (96.0%) | 205 (91.1%) |
| Solved within 2 tries | 75.1% | 71.6% | 75.1% | 76.9% |
| Median time to solve | 11.5 s | 12.8 s | 10.9 s | 10.3 s |
| Mean / 90th percentile | 32.1 / 81.6 s | 39.8 / 56.9 s | 27.0 / 68.4 s | 17.5 / 37.0 s |
| Wall clock | 3 h 39 min | 3 h 26 min | 2 h 33 min | 2 h 07 min |
| GPUs used | 2 | 2 | 1 | 1 |

Solved at each try:

| Run | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9-10 |
|---|---|---|---|---|---|---|---|---|---|
| Matched baseline (all fast) | 90 | 83 | 23 | 2 | 4 | 2 | 0 | 1 | 0 |
| No second model (thinking from try 5) | 85 | 84 | 22 | 10 | 9 | 5 | 1 | 0 | - |

Paired per-exercise outcomes (exact McNemar test on the discordant pairs):

| Comparison | Solved only by first | Solved only by second | p |
|---|---|---|---|
| Cascade run 1 vs matched baseline | 14 | 0 | 0.0001 |
| Cascade run 2 vs matched baseline | 15 | 1 | 0.0005 |
| No second model vs matched baseline | 15 | 4 | 0.019 |
| Cascade run 1 vs no second model | 5 | 2 | 0.45 |
| Cascade run 2 vs no second model | 6 | 3 | 0.51 |

What this settles and what it does not:

- **The gain survives matched settings.** With identical settings the single model solved 205 and the cascade 219 in both runs. After four fast tries the baseline had 198 solved and 27 open; six more fast tries solved 7 of them. In the no-second-model run, 201 were solved after four fast tries and four thinking tries solved 15 of the remaining 24.
- **The cascade is not faster on the typical exercise.** The matched baseline has the lowest median (10.3 s). Escalation buys solve rate, at the cost of a longer tail and a longer run.
- **Most of the gain needs only one model.** Switching Flash-Next to thinking mode, with no second model and one GPU, reached 216. The two cascade runs reached 219. The paired difference between them (5 vs 2, and 6 vs 3) is not distinguishable from run-to-run variation, which changed 4 outcomes between two identical cascade runs.
- **A second model may still add a little.** Both cascade runs finished 3 above the single-model run, and DeepSeek solved 2 and 5 exercises that had survived six attempts. Three runs are not enough to tell a small real effect from noise. It costs a second GPU and about an hour per run.

## Where the gain comes from

**Fast retries stop paying.** The single-model retry runs show what further fast tries buy. In the vLLM run of the same model (`until10-qfn-vllm-nvfp4-diff-nothink`, 4-bit, same accuracy within noise), 196 exercises were solved after four tries. Tries 5 to 10 added 5 more, out of 29 still open. In the cascade, 197 were solved after four tries, and two reasoning tries added 20 out of 28.

| After four fast tries | Next step | Further solves |
|---|---|---|
| 196 solved, 29 open (Flash-Next alone, vLLM) | six more fast tries | 5 |
| 197 solved, 28 open (cascade) | two thinking tries, same model | 20 |

This is the central observation. It compares two different runs, so it shares the single-run caveat below.

**DeepSeek's contribution is small in this run.** Eight exercises reached DeepSeek and it solved two. Those eight had already survived six attempts by Flash-Next, so they are the hardest in the set, and 2 of 8 says little about DeepSeek in general. An earlier offline comparison of the two single-model retry runs found that DeepSeek solved 14 exercises Flash-Next never solved in 10 tries, for a union of 218 of 225. The cascade reached 219, about that union, with reasoning mode doing most of the work DeepSeek would otherwise have done. Whether a second model adds anything beyond reasoning mode is open. The run without DeepSeek will answer it.

**Repetition is not useless for every model.** DeepSeek alone on two GPUs kept finding solutions late: tries 5 to 8 added 14 of the 32 exercises still open after try 4. On one GPU the same model added 5 of 23 and nothing after try 6. The decay of fast retries is clear for Flash-Next and mixed for DeepSeek.

## How much of this is noise

There are three independent 10-try runs of Flash-Next with thinking off, on three engines: 201 (vLLM, 4-bit), 202 (Strata, 8-bit) and 204 (Basalt, 8-bit). That is a spread of 1.3 points (3 of 225). The cascade's 219 sits 6.7 points above the best of them.

Treating exercises as independent trials, the 95% Wilson interval for 219 of 225 is 94.3 to 98.8%. For 204 of 225 it is 86.2 to 93.8%. A Fisher exact test of 219 versus 204 gives p = 0.005, and 219 versus 207 gives p = 0.02. These are rough. The same 225 exercises are used in every run, so the correct test is paired (McNemar on per-exercise outcomes), and exercises differ greatly in difficulty.

Aggregate scores are stable while individual exercises are not. First-two-try scores for Flash-Next ranged only from 72.0% to 75.1% across six runs on three engines, yet about a third of exercises changed between solved and unsolved from one run to the next, and outputs differed between runs even at temperature 0. Per-language counts move the same way: for the same model on two engines, Rust was 17 of 30 in one two-try run and 20 of 30 in the other, and Python 27 and 31 of 34. Early evidence that one model was better at Rust and another at Python did not survive repeat runs, which is why the cascade routes on failure and not on language.

## Confounds

- **Chat-history summaries (resolved for the matched baseline).** The matched baseline above has summaries off like the cascade. The earlier single-model retry runs in the Results table had them on, which is why they are no longer the main comparison. For reference: the cascade ran with aider's summaries off. The earlier single-model retry runs had them on. With the benchmark's default (`max_chat_history_tokens` = 1024), aider sends a summary request after nearly every coder reply, about half of all requests and 26% of prompt tokens. Turning them off, in a paired test on the same engine, cut wall clock by 29% (1 h 54 min to 1 h 21 min) and median time to solve by 27% (13.9 s to 10.1 s) with the same solve rate (74.2% both). So the 11.5 s versus 13.6 s median difference should not be credited to the cascade. Whether summaries change the solve rate over 10 tries has not been measured.
- **Try caps differ.** 8 versus 10. This favors the baselines.
- **The DeepSeek baseline had both GPUs.** In the cascade it has one. Its 1-GPU plus RAM retry run reached the same 92.0% with a median of 1.6 min.
- **One thread versus four.** The cascade and the Flash-Next baseline ran one exercise at a time. The DeepSeek baseline ran four sessions, so its times are under load.
- **The order was tuned on this benchmark.** The stage boundaries (4, 2, 2) were chosen after looking at single-model results on the same 225 exercises. There is no held-out set.

## What did not work

| Attempt | Result | Reading |
|---|---|---|
| Larger model: Qwen3.5-397B-A17B Q4_K_M, llama.cpp, 18 layers' experts in RAM | 84.4% on 2 tries, median 6.2 min, 13.3 h run, about 18.5 tok/s | About 68 GB of expert weights ran from system RAM with the GPUs near 10% busy. Accuracy without speed. |
| Reasoning always on: Flash-Next on Strata | 85.8% on 2 tries, median 2.5 min, 14 h 22 min | Plus 11.6 points on the 2-try score for about 8x the run time. The fast retry run reached 89.8% in 3 h 24 min. |
| Four concurrent requests: Basalt `--parallel 4` | 71.1%, median 0.9 min versus 0.2 min, run 1 h 46 min versus 1 h 40 min | Each request fell to about 40 tok/s (about 135 total) against 240 to 330 for a single request with speculative decoding. No throughput gain. |
| Prompt caching: stock cache flags, then a longest-common-prefix fork | 0.9% and 1.1% of prompt tokens reused | Summary and coder prompts share 3 tokens, and Basalt drops checkpoints when a different conversation arrives. With summaries off, reuse rose to 16%. An offline replay estimates 41 to 47% is reachable with checkpoints at turn boundaries. |
| Routing by language | Dropped | The per-language differences were run-to-run variation. |

For scale, a median 13.6 s solve on Basalt breaks down as 5.8 s reading the prompt, 6.0 s writing the answer and about 2 s running tests. Prompt reading is as large as generation, which is why prompt reuse is the next engine change.

## Comparison with published results

On the two-try rule the cascade scores 75.1%. The official [Aider leaderboard](https://aider.chat/docs/leaderboards/) tops out at GPT-5 (high) with 88.0%. Its best open-weight entry is DeepSeek-V3.2-Exp (Reasoner) at 74.2%. The page was last refreshed in November 2025, so newer models are absent.

The nearer comparison is with systems that iterate until tests pass. The highest such published result I found is [Refact.ai's agent on Claude 3.7 Sonnet](https://refact.ai/blog/2025/refact-ai-agent-achieves-93-3-on-aider-polyglot-benchmark/): 93.3% with thinking, 92.9% without. That is a different harness (an agent with a step cap, not aider with a try cap) on a hosted frontier model, so it is a reference point and not a like-for-like comparison. I found nothing published at or above 97%, and I did not search exhaustively. GPT-5 has no published work-until-correct result on this benchmark and would very likely exceed its 88% under these rules.

## Limits

- Two runs of the cascade, both 219 of 225. The single-model baselines it is compared with are not yet matched in settings (see Confounds), so the size of the gain over a matched baseline is not established.
- Small, self-contained exercises with complete test suites. This says nothing about large repositories, ambiguous requirements or tasks with no tests.
- The benchmark is public and old enough that some exercises may be in the training data of both models. That affects absolute scores more than the comparison between the cascade and the same models alone.
- Attempts are unequal in cost. A try count is a poor unit. Wall-clock time to a passing solution is the measure I report and the one I would ask others to report.
- The cascade harness is not yet published.

## Next runs

1. Done: the cascade was repeated unchanged (see Replication).
2. Done: the matched baseline (see Matched baseline and ablation).
3. Done: the cascade without DeepSeek (see Matched baseline and ablation). More repeats are needed to tell whether the second model's small apparent contribution is real.
4. A time budget on the reasoning stages, to recover the wall clock spent on unsolved exercises.
5. Earlier escalation (two fast tries, then thinking), since the attempt success rate has already fallen to 37.5% by try 3.
6. Other line-ups and other hardware.

## Data

Every run, including the failed and abandoned ones, is in [github.com/AI-Development-Work/aimos-benchmark-results](https://github.com/AI-Development-Work/aimos-benchmark-results). [RESULTS.md](../RESULTS.md) holds the full tables and run folders, [ENGINES.md](../ENGINES.md) describes the engines, and new runs are posted there as they finish. The cascade harness will be released once the result has been repeated.