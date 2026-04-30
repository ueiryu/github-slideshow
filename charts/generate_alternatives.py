"""
Alternative chart styles for The Dunes vs. Palm Haven comparison.

Each style answers a slightly different question and emphasizes the data
differently. Pick the one that best matches the story you want to tell.

  A. Dot plot (Cleveland)     - clean, modern; shows magnitude + gap.
  B. Lollipop chart           - dot plot with a stem; a touch more visual weight.
  C. Slope chart              - one image, all five metrics, gap as slope.
  D. Diverging / butterfly    - back-to-back bars; symmetric "tug of war" feel.
  E. Grouped vertical bars    - classic; familiar to any audience.
  F. Small multiples          - one tiny chart per metric; great for repetition.
"""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.patches import FancyArrowPatch

OUTPUT_DIR = Path(__file__).parent / "alternatives"

DUNES = "#8B6F47"
PALM_HAVEN = "#2C7A7B"
GRAY_DARK = "#595959"
GRAY = "#A6A6A6"
GRAY_LIGHT = "#D9D9D9"
TEXT = "#262626"
ACCENT = "#A8431E"

rcParams["font.family"] = "DejaVu Sans"
rcParams["font.size"] = 11
rcParams["text.parse_math"] = False
rcParams["axes.edgecolor"] = GRAY
rcParams["axes.labelcolor"] = TEXT
rcParams["xtick.color"] = GRAY_DARK
rcParams["ytick.color"] = TEXT


def declutter(ax, keep_left=True, keep_bottom=False):
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    if not keep_bottom:
        ax.spines["bottom"].set_visible(False)
        ax.tick_params(axis="x", length=0)
    if not keep_left:
        ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)


def save(fig, name):
    path = OUTPUT_DIR / name
    fig.savefig(path, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  wrote {path}")


# Shared dataset for all alternatives.
METRICS = [
    ("Elevated BMI",            59, 23),
    ("Children under 18",       31, 16),
    ("Spanish primary",         15,  6),
    ("Income under $25K",       69, 16),
    ("Income over $40K",         4, 45),
]


# ---------------------------------------------------------------------------
# A. Dot plot (Cleveland) - BMI focus.
# ---------------------------------------------------------------------------
def chart_dot_plot():
    fig, ax = plt.subplots(figsize=(11, 4.2))
    fig.subplots_adjust(left=0.18, right=0.96, top=0.78, bottom=0.18)

    y = 0
    palm_v, dunes_v = 23, 59

    # Connector line representing the gap.
    ax.hlines(y, palm_v, dunes_v, color=GRAY_LIGHT, lw=4, zorder=1)
    ax.scatter([palm_v], [y], s=420, color=PALM_HAVEN, zorder=3,
               edgecolor="white", linewidth=2)
    ax.scatter([dunes_v], [y], s=420, color=ACCENT, zorder=3,
               edgecolor="white", linewidth=2)

    ax.text(palm_v, y - 0.35, f"Palm Haven\n{palm_v}%", ha="center", va="top",
            fontsize=11, color=PALM_HAVEN, fontweight="bold")
    ax.text(dunes_v, y - 0.35, f"The Dunes\n{dunes_v}%", ha="center", va="top",
            fontsize=11, color=ACCENT, fontweight="bold")
    ax.text((palm_v + dunes_v) / 2, y + 0.25, "36-point gap",
            ha="center", va="bottom", fontsize=12, fontweight="bold",
            color=GRAY_DARK)

    ax.set_xlim(0, 75)
    ax.set_ylim(-1.2, 0.9)
    ax.set_yticks([])
    ax.set_xticks([])
    declutter(ax, keep_left=False)

    fig.text(0.04, 0.92,
             "A. Dot plot — emphasizes the distance between two points",
             fontsize=15, fontweight="bold", color=TEXT)
    fig.text(0.04, 0.86,
             "Share of residents with elevated BMI",
             fontsize=10.5, color=GRAY_DARK)

    save(fig, "A_dot_plot.png")


# ---------------------------------------------------------------------------
# B. Lollipop chart - same idea, vertical stems.
# ---------------------------------------------------------------------------
def chart_lollipop():
    fig, ax = plt.subplots(figsize=(11, 5.2))
    fig.subplots_adjust(left=0.10, right=0.96, top=0.82, bottom=0.14)

    labels = [m[0] for m in METRICS]
    dunes_vals = [m[1] for m in METRICS]
    palm_vals = [m[2] for m in METRICS]
    x = list(range(len(labels)))

    offset = 0.18
    for i, (d, p) in enumerate(zip(dunes_vals, palm_vals)):
        ax.vlines(i - offset, 0, d, color=DUNES, lw=2.5, alpha=0.9)
        ax.vlines(i + offset, 0, p, color=PALM_HAVEN, lw=2.5, alpha=0.9)
    ax.scatter([i - offset for i in x], dunes_vals, s=180, color=DUNES,
               zorder=3, edgecolor="white", linewidth=1.5,
               label="The Dunes")
    ax.scatter([i + offset for i in x], palm_vals, s=180, color=PALM_HAVEN,
               zorder=3, edgecolor="white", linewidth=1.5,
               label="Palm Haven")

    for i, v in enumerate(dunes_vals):
        ax.text(i - offset, v + 3, f"{v}%", ha="center", va="bottom",
                fontsize=10, fontweight="bold", color=DUNES)
    for i, v in enumerate(palm_vals):
        ax.text(i + offset, v + 3, f"{v}%", ha="center", va="bottom",
                fontsize=10, fontweight="bold", color=PALM_HAVEN)

    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=10.5)
    ax.set_yticks([])
    ax.set_ylim(0, 85)
    declutter(ax, keep_left=False, keep_bottom=False)
    ax.legend(loc="upper right", frameon=False, fontsize=10.5)

    fig.text(0.04, 0.93,
             "B. Lollipop chart — five metrics, side by side",
             fontsize=15, fontweight="bold", color=TEXT)
    fig.text(0.04, 0.88,
             "Percent of residents in each category",
             fontsize=10.5, color=GRAY_DARK)

    save(fig, "B_lollipop.png")


# ---------------------------------------------------------------------------
# C. Slope chart - all metrics on one chart, gap shown as slope.
# ---------------------------------------------------------------------------
def chart_slope():
    fig, ax = plt.subplots(figsize=(10.5, 6.5))
    fig.subplots_adjust(left=0.05, right=0.78, top=0.82, bottom=0.10)

    metrics = [
        ("Elevated BMI",      59, 23),
        ("Income under $25K", 69, 16),
        ("Children under 18", 31, 16),
        ("Spanish primary",   15,  6),
        ("Income over $40K",   4, 45),
    ]

    # Draw all slope lines and points first.
    for label, d_val, p_val in metrics:
        gap = abs(d_val - p_val)
        if gap < 10:
            line_color = GRAY
        elif d_val > p_val:
            line_color = DUNES
        else:
            line_color = PALM_HAVEN

        ax.plot([0, 1], [d_val, p_val], color=line_color, lw=2.5, alpha=0.9,
                zorder=2)
        ax.scatter([0], [d_val], s=110, color=DUNES, zorder=3,
                   edgecolor="white", linewidth=1.5)
        ax.scatter([1], [p_val], s=110, color=PALM_HAVEN, zorder=3,
                   edgecolor="white", linewidth=1.5)

    # Group right-side labels by Palm Haven value so coincident points share
    # one combined label (avoids overlapping text).
    right_groups = {}
    for label, _, p_val in metrics:
        right_groups.setdefault(p_val, []).append(label)
    for p_val, labels in right_groups.items():
        ax.text(1.04, p_val,
                f"{p_val}%   " + " / ".join(labels),
                ha="left", va="center", fontsize=10.5, color=TEXT)

    # Same grouping for the left (Dunes) side - just the value labels.
    left_groups = {}
    for _, d_val, _ in metrics:
        left_groups.setdefault(d_val, True)
    for d_val in left_groups:
        ax.text(-0.04, d_val, f"{d_val}%", ha="right", va="center",
                fontsize=10.5, fontweight="bold", color=TEXT)

    ax.text(0, 105, "The Dunes", ha="center", va="bottom",
            fontsize=12, fontweight="bold", color=DUNES)
    ax.text(1, 105, "Palm Haven", ha="center", va="bottom",
            fontsize=12, fontweight="bold", color=PALM_HAVEN)

    ax.set_xlim(-0.2, 1.2)
    ax.set_ylim(-5, 110)
    ax.set_xticks([])
    ax.set_yticks([])
    for side in ("top", "right", "bottom", "left"):
        ax.spines[side].set_visible(False)

    fig.text(0.04, 0.93,
             "C. Slope chart — every gap on one canvas",
             fontsize=15, fontweight="bold", color=TEXT)
    fig.text(0.04, 0.88,
             "Steeper line = larger gap between neighborhoods",
             fontsize=10.5, color=GRAY_DARK)

    save(fig, "C_slope_chart.png")


# ---------------------------------------------------------------------------
# D. Diverging / butterfly chart - back-to-back bars for income.
# ---------------------------------------------------------------------------
def chart_diverging():
    fig, ax = plt.subplots(figsize=(11, 5.4))
    fig.subplots_adjust(left=0.06, right=0.94, top=0.80, bottom=0.10)

    brackets = ["Over $40K", "$25K–$40K", "Under $25K"]
    dunes_vals = [4, 27, 69]
    palm_vals = [45, 38, 16]

    y = list(range(len(brackets)))
    bar_height = 0.5

    ax.barh(y, [-v for v in dunes_vals], color=DUNES, height=bar_height,
            edgecolor="white", linewidth=2)
    ax.barh(y, palm_vals, color=PALM_HAVEN, height=bar_height,
            edgecolor="white", linewidth=2)

    for i, v in enumerate(dunes_vals):
        ax.text(-v - 2, i, f"{v}%", ha="right", va="center",
                fontsize=12, fontweight="bold", color=DUNES)
    for i, v in enumerate(palm_vals):
        ax.text(v + 2, i, f"{v}%", ha="left", va="center",
                fontsize=12, fontweight="bold", color=PALM_HAVEN)

    # Place the bracket label above each bar pair so it never overlaps a bar.
    for i, label in enumerate(brackets):
        ax.text(0, i + bar_height / 2 + 0.08, label,
                ha="center", va="bottom", fontsize=11,
                color=TEXT, fontweight="bold")

    # Anchor labels for each side, placed once at the top.
    ax.text(-85, len(brackets) - 0.2, "The Dunes", ha="left", va="bottom",
            fontsize=12, fontweight="bold", color=DUNES)
    ax.text(85, len(brackets) - 0.2, "Palm Haven", ha="right", va="bottom",
            fontsize=12, fontweight="bold", color=PALM_HAVEN)

    ax.axvline(0, color=GRAY, lw=0.8, ymin=0.05, ymax=0.95)
    ax.set_xlim(-85, 85)
    ax.set_ylim(-0.6, len(brackets) - 0.1)
    ax.set_xticks([])
    ax.set_yticks([])
    for side in ("top", "right", "bottom", "left"):
        ax.spines[side].set_visible(False)

    fig.text(0.04, 0.92,
             "D. Diverging bars — opposite-pulling distributions",
             fontsize=15, fontweight="bold", color=TEXT)
    fig.text(0.04, 0.87,
             "Income bracket: The Dunes (left) vs. Palm Haven (right)",
             fontsize=10.5, color=GRAY_DARK)

    save(fig, "D_diverging_bars.png")


# ---------------------------------------------------------------------------
# E. Grouped vertical bars - classic, audience-friendly.
# ---------------------------------------------------------------------------
def chart_grouped_vertical():
    fig, ax = plt.subplots(figsize=(11, 5.2))
    fig.subplots_adjust(left=0.08, right=0.96, top=0.82, bottom=0.16)

    labels = [m[0] for m in METRICS]
    dunes_vals = [m[1] for m in METRICS]
    palm_vals = [m[2] for m in METRICS]
    x = list(range(len(labels)))
    width = 0.36

    bars1 = ax.bar([i - width / 2 for i in x], dunes_vals, width,
                   color=DUNES, label="The Dunes",
                   edgecolor="white", linewidth=1.5)
    bars2 = ax.bar([i + width / 2 for i in x], palm_vals, width,
                   color=PALM_HAVEN, label="Palm Haven",
                   edgecolor="white", linewidth=1.5)

    for bar in bars1:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1.5,
                f"{int(bar.get_height())}%", ha="center", va="bottom",
                fontsize=10, fontweight="bold", color=DUNES)
    for bar in bars2:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1.5,
                f"{int(bar.get_height())}%", ha="center", va="bottom",
                fontsize=10, fontweight="bold", color=PALM_HAVEN)

    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=10.5)
    ax.set_yticks([])
    ax.set_ylim(0, 85)
    declutter(ax, keep_left=False)
    ax.legend(loc="upper right", frameon=False, fontsize=10.5)

    fig.text(0.04, 0.93,
             "E. Grouped vertical bars — the most familiar comparison",
             fontsize=15, fontweight="bold", color=TEXT)
    fig.text(0.04, 0.88,
             "Each pair: The Dunes vs. Palm Haven",
             fontsize=10.5, color=GRAY_DARK)

    save(fig, "E_grouped_vertical.png")


# ---------------------------------------------------------------------------
# F. Small multiples - one tiny chart per metric.
# ---------------------------------------------------------------------------
def chart_small_multiples():
    fig, axes = plt.subplots(1, 5, figsize=(13.5, 4.2), sharey=True)
    fig.subplots_adjust(left=0.05, right=0.97, top=0.72, bottom=0.18,
                        wspace=0.25)

    for ax, (label, d_val, p_val) in zip(axes, METRICS):
        bars = ax.bar(["Dunes", "Palm\nHaven"], [d_val, p_val],
                      color=[DUNES, PALM_HAVEN], width=0.55,
                      edgecolor="white", linewidth=1.5)
        for bar, val, color in zip(bars, [d_val, p_val],
                                   [DUNES, PALM_HAVEN]):
            ax.text(bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + 1.5, f"{val}%",
                    ha="center", va="bottom",
                    fontsize=11, fontweight="bold", color=color)
        ax.set_ylim(0, 85)
        ax.set_yticks([])
        ax.set_title(label, fontsize=11, fontweight="bold", color=TEXT,
                     pad=8)
        declutter(ax, keep_left=False)
        ax.tick_params(axis="x", labelsize=9.5, colors=GRAY_DARK)

    fig.text(0.04, 0.92,
             "F. Small multiples — repeat the same shape for every metric",
             fontsize=15, fontweight="bold", color=TEXT)
    fig.text(0.04, 0.85,
             "Once the audience reads one, they can read them all",
             fontsize=10.5, color=GRAY_DARK)

    save(fig, "F_small_multiples.png")


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print("Generating alternative chart styles...")
    chart_dot_plot()
    chart_lollipop()
    chart_slope()
    chart_diverging()
    chart_grouped_vertical()
    chart_small_multiples()
    print("Done.")


if __name__ == "__main__":
    main()
