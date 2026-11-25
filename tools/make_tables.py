"""Render the time-to-solution table and the T6-vs-7960 table as PNG images for posting.
Images keep formatting on any platform (Facebook, LinkedIn, X), unlike markdown tables."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def render(path, title, subtitle, cols, rows, widths, bold_rows=(), note=""):
    """Draw a table figure: header row shaded, alternating row stripes, optional bold rows."""
    fig_h = 1.3 + 0.42 * (len(rows) + 1) + (0.4 if note else 0)
    fig, ax = plt.subplots(figsize=(sum(widths), fig_h), dpi=200)
    ax.axis("off")
    ax.set_position([0.01, 0.0, 0.98, 1.0])  # use the full figure width so the table is not offset right
    fig.text(0.02, 1 - 0.38 / fig_h, title, fontsize=15, weight="bold", va="top")
    fig.text(0.02, 1 - 0.80 / fig_h, subtitle, fontsize=9.5, color="#444", va="top")
    top = 1 - 1.15 / fig_h
    bottom = (0.6 / fig_h) if note else 0.02  # leave room for the footnote
    t = ax.table(cellText=rows, colLabels=cols, colWidths=[w / sum(widths) for w in widths],
                 cellLoc="center", loc="upper left", bbox=[0, bottom, 1, top - bottom])
    t.auto_set_font_size(False); t.set_fontsize(9)
    for (r, c), cell in t.get_celld().items():
        cell.set_edgecolor("#d0d0d0")
        if c == 0: cell.set_text_props(ha="left"); cell.PAD = 0.02
        if r == 0:
            cell.set_facecolor("#1f3b5c"); cell.set_text_props(color="white", weight="bold")
        else:
            cell.set_facecolor("#f4f6f9" if r % 2 else "white")
            if (r - 1) in bold_rows: cell.set_text_props(weight="bold")
    if note: fig.text(0.02, 0.15 / fig_h, note, fontsize=8, color="#555", va="bottom")
    fig.savefig(path, bbox_inches="tight", facecolor="white"); plt.close(fig)

render("time_to_solution.png",
       "Local LLM coding: time to a correct solution",
       "Aider Polyglot, 225 exercises (C++, Go, Java, JS, Python, Rust) · self-hosted on 2× RTX PRO 6000 Blackwell Max-Q · Nov 2026",
       ["Model / run", "Engine", "Hardware", "Leaderboard\n(2 tries)", "Solved\n(final)", "Median time\nto solve", "Solved\n≤5 min", "Solved\n≤10 min", "Solved\n≤30 min"],
       [['Flash-Next alone: 4+4, fresh, corrected hand-off note', 'Basalt', '1 GPU + RAM', '77.8%', '98.7%', '0.2 min', '96.4%', '97.3%', '98.7%'],
        ['Flash-Next alone: 2+4, fresh, corrected hand-off note', 'Basalt', '1 GPU + RAM', '72.4%', '98.7%', '0.2 min', '93.3%', '98.2%', '98.7%'],
        ['Flash-Next alone: 3 fast tries, then 4 thinking tries — repeat', 'Basalt', '1 GPU + RAM', '73.3%', '98.2%', '0.2 min', '96.9%', '98.2%', '98.2%'],
        ['Team: Flash-Next (fast, then thinking), then DeepSeek — up to 8 tries', 'Basalt + Maya', '2 GPUs + RAM', '75.1%', '97.3%', '0.2 min', '96.4%', '97.3%', '97.3%'],
        ['Team repeat (unchanged): Flash-Next (fast, then thinking), then DeepSeek — up to 8 tries', 'Basalt + Maya', '2 GPUs + RAM', '71.6%', '97.3%', '0.2 min', '96.4%', '96.9%', '96.9%'],
        ['Flash-Next alone: 4+4, fresh, corrected hand-off note — run 2', 'Basalt', '1 GPU + RAM', '76.9%', '97.3%', '0.2 min', '96.0%', '97.3%', '97.3%'],
        ['Flash-Next alone: 2+4, fresh, corrected hand-off note — run 2', 'Basalt', '1 GPU + RAM', '74.2%', '97.3%', '0.2 min', '94.2%', '96.9%', '97.3%'],
        ['Flash-Next alone: fast, then thinking (4 + 4 tries), no second model', 'Basalt', '1 GPU + RAM', '75.1%', '96.0%', '0.2 min', '96.0%', '96.0%', '96.0%'],
        ['Flash-Next alone: 2 fast tries, then 4 thinking tries — repeat', 'Basalt', '1 GPU + RAM', '71.1%', '96.0%', '0.2 min', '94.2%', '96.0%', '96.0%'],
        ['Flash-Next alone: 2 fast tries, then 4 thinking tries', 'Basalt', '1 GPU + RAM', '75.1%', '97.8%', '0.2 min', '96.0%', '97.3%', '97.8%'],
        ['Flash-Next alone: 4+4, fresh, original hand-off note, provisional', 'Basalt', '1 GPU + RAM', '79.6%', '97.8%', '0.2 min', '95.6%', '97.8%', '97.8%'],
        ['Flash-Next alone: 3 fast tries, then 4 thinking tries', 'Basalt', '1 GPU + RAM', '72.4%', '97.3%', '0.2 min', '96.4%', '97.3%', '97.3%'],
        ['Flash-Next alone: 4 fast + 4 thinking, 300 s cap (never triggered)', 'Basalt', '1 GPU + RAM', '75.6%', '96.4%', '0.2 min', '96.0%', '96.4%', '96.4%'],
        ['Flash-Next alone: 4 fast + 4 thinking — repeat', 'Basalt', '1 GPU + RAM', '74.7%', '95.6%', '0.2 min', '95.1%', '95.6%', '95.6%'],
        ['Qwen3.8-Flash-Next Q8_0, thinking OFF — retry run, matched to team runs', 'Basalt', '1 GPU + RAM', '76.9%', '91.1%', '0.2 min', '91.1%', '91.1%', '91.1%'],
        ['Qwen3.8-Flash-Next 2-bit (IQ2_XS), thinking OFF — retry run', 'Maya', '1 GPU', '72.0%', '91.1%', '1.2 min', '82.2%', '89.8%', '91.1%'],
        ['Qwen3.8-Flash-Next 2-bit (IQ2_XS), thinking OFF', 'Maya', '1 GPU', '73.3%', '73.3%', '1.0 min', '69.3%', '73.3%', '73.3%'],
        ['DeepSeek V4.1-Flash (2-bit), thinking OFF — retry run', 'Maya', '2 GPUs', '68.9%', '92.0%', '0.8 min', '88.4%', '90.7%', '92.0%'],
        ['DeepSeek V4.1-Flash (2-bit), thinking OFF — retry run', 'Maya', '1 GPU + RAM', '72.0%', '92.0%', '1.6 min', '78.7%', '89.8%', '91.6%'],
        ['Qwen3.8-Flash-Next Q8_0, thinking OFF — retry run', 'Basalt', '1 GPU + RAM', '75.1%', '90.7%', '0.2 min', '90.7%', '90.7%', '90.7%'],
        ['Qwen3.8-Flash-Next Q8_0, thinking OFF — retry run', 'Strata', '1 GPU + RAM', '73.8%', '89.8%', '0.2 min', '89.8%', '89.8%', '89.8%'],
        ['Qwen3.8-Flash-Next NVFP4 (4-bit), thinking OFF — retry run', 'vLLM', '2 GPUs', '72.9%', '89.3%', '0.4 min', '89.3%', '89.3%', '89.3%'],
        ['Qwen3.8-27B FP8, thinking OFF — retry run', 'vLLM', '1 GPU', '48.0%', '84.4%', '1.1 min', '74.7%', '82.7%', '84.4%'],
        ['DeepSeek V4.1-Flash (2-bit), thinking ON', 'Maya', '1 GPU + RAM', '85.8%', '85.8%', '8.8 min', '30.2%', '45.8%', '73.8%'],
        ['Qwen3.5-397B-A17B Q4_K_M, thinking OFF', 'llama.cpp', '2 GPUs + RAM', '84.4%', '84.4%', '6.2 min', '33.8%', '63.6%', '79.1%'],
        ['Qwen3.8-Flash-Next Q8_0, thinking ON', 'Strata', '1 GPU + RAM', '85.8%', '85.8%', '2.5 min', '72.9%', '81.3%', '85.8%'],
        ['Qwen3.8-27B BF16 (16-bit), thinking ON', 'vLLM', '1 GPU', '75.1%', '75.1%', '7.3 min', '27.1%', '45.3%', '68.4%'],
        ['Qwen3.8-Flash-Next Q8_0, thinking OFF', 'Strata', '1 GPU + RAM', '74.2%', '74.2%', '0.2 min', '74.2%', '74.2%', '74.2%'],
        ['Qwen3.8-Flash-Next NVFP4 (4-bit), thinking OFF', 'vLLM', '2 GPUs', '72.9%', '72.9%', '0.3 min', '72.9%', '72.9%', '72.9%'],
        ['Qwen3.8-Flash-Next Q8_0, thinking OFF', 'Basalt', '1 GPU + RAM', '72.0%', '72.0%', '0.2 min', '72.0%', '72.0%', '72.0%'],
        ['Qwen3.8-Flash-Next Q8_0, thinking OFF, 4 requests at once', 'Basalt', '1 GPU + RAM', '71.1%', '71.1%', '0.9 min', '69.8%', '71.1%', '71.1%'],
        ['Qwen3.8-27B NVFP4 (4-bit), thinking ON', 'vLLM', '1 GPU', '71.1%', '71.1%', '3.3 min', '42.7%', '63.6%', '68.9%'],
        ['Qwen3.8-27B FP8, thinking ON', 'vLLM', '1 GPU', '69.3%', '69.3%', '4.0 min', '39.1%', '53.3%', '68.9%'],
        ['DeepSeek V4.1-Flash (2-bit), thinking OFF', 'Maya', '2 GPUs', '69.3%', '69.3%', '0.6 min', '69.3%', '69.3%', '69.3%'],
        ['DeepSeek V4.1-Flash (2-bit), thinking OFF', 'Maya', '1 GPU + RAM', '68.0%', '68.0%', '1.7 min', '61.3%', '67.1%', '68.0%'],
        ['Qwen3-235B-A22B-Instruct-2507 NVFP4', 'vLLM', '2 GPUs', '53.8%', '53.8%', '0.7 min', '53.3%', '53.8%', '53.8%'],
        ['gpt-oss-120b', 'vLLM', '1 GPU', '53.3%', '53.3%', '0.7 min', '52.4%', '52.9%', '53.3%'],
        ['Qwen3.8-27B FP8, thinking OFF', 'vLLM', '1 GPU', '50.7%', '50.7%', '0.8 min', '48.4%', '50.7%', '50.7%'],
        ['Qwen3.8-27B BF16, thinking OFF', 'vLLM', '1 GPU', '50.2%', '50.2%', '1.3 min', '43.1%', '48.4%', '50.2%'],
        ['Laguna S 2.1 FP8, thinking OFF', 'vLLM', '2 GPUs', '46.7%', '46.7%', '0.3 min', '46.7%', '46.7%', '46.7%'],
        ['Laguna S 2.1 NVFP4 (4-bit), thinking OFF', 'vLLM', '2 GPUs', '44.4%', '44.4%', '0.3 min', '44.0%', '44.0%', '44.4%'],
        ['Qwen3.8-27B NVFP4 (4-bit), thinking OFF', 'vLLM', '1 GPU', '42.7%', '42.7%', '0.5 min', '42.2%', '42.7%', '42.7%'],
        ['Mistral Small 4 119B NVFP4', 'vLLM', '1 GPU', '15.1%', '15.1%', '0.2 min', '15.1%', '15.1%', '15.1%'],
        ['Devstral Small 2 24B', 'vLLM', '1 GPU', '13.8%', '13.8%', '0.4 min', '13.8%', '13.8%', '13.8%']],
       [4.6, 1.15, 1.2, 1.05, 0.9, 1.05, 0.85, 0.85, 0.85], bold_rows=(3, 4, 7, 9),  # rows bold in README (team, team repeat, 4+4 baseline, 2+4 first run); matches README
       note="Bold marks rows highlighted in earlier versions; it is not a ranking. 4+4 / 2+4 = fast tries + thinking tries; fresh = new conversation at the switch.\nRetry run = up to 10 tries with test feedback (separate run). Times are per-exercise wall clock, 4 exercises in parallel. Fast models that retry beat slow 'thinking' models on time to working code.")

render("t6_vs_7960.png",
       "Dell Pro Precision 9 T6 vs Precision 7960 for local LLM inference",
       "T6 values from StorageReview's spec table (Mar 2026); 7960 values approximate — confirm against your unit",
       ["", "Pro Precision 9 T6", "Precision 7960"],
       [["CPU", "Xeon 6 (Granite Rapids), up to 86 cores", "Xeon W-3400/3500, up to ~56–60 cores"],
        ["Memory", "16 slots, DDR5-6400, up to 4 TB", "DDR5-4800, 8 channels"],
        ["GPUs (Dell spec)", "2× 600 W, or 5× 300 W", "up to 4 double-width"],
        ["Full Gen5 x16 GPU slots", "2 (others x8 / x4)", "check slot map"],
        ["RTX PRO 6000 Max-Q, practical", "3", "4"],
        ["Power supply", "2400 W (1200 W at 120 V)", "2200 W (likely derated at 120 V)"],
        ["Storage", "up to 12 NVMe, up to 316 TB", "—"],
        ["Best for", "2 full-power GPUs or fastest RAM", "4× RTX PRO 6000 Max-Q (384 GB VRAM)"]],
       [2.2, 3.1, 3.1])
print("ok")
