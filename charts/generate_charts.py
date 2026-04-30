"""
Neighborhood comparison charts: The Dunes vs. Palm Haven.

Design principles (Cole Nussbaumer Knaflic, "Storytelling with Data"):
  - Strategic use of color: brown/tan for The Dunes, teal for Palm Haven, gray
    for context.
  - Declutter: no gridlines, minimal spines, no top/right borders, no legends
    when direct labels work.
  - Focal point: BMI gap is the headline insight, the title carries the
    takeaway.
  - White space: generous margins and figure padding.
  - Direct data labeling instead of axis tick precision.
"""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import rcParams

OUTPUT_DIR = Path(__file__).parent

DUNES = "#8B6F47"          # Brown / tan
DUNES_LIGHT = "#C4A57B"
PALM_HAVEN = "#2C7A7B"     # Teal
PALM_HAVEN_LIGHT = "#81B5B0"
GRAY_DARK = "#595959"
GRAY = "#A6A6A6"
GRAY_LIGHT = "#D9D9D9"
TEXT = "#262626"
ACCENT = "#A8431E"         # Used sparingly to emphasize the key insight

rcParams["font.family"] = "DejaVu Sans"
rcParams["font.size"] = 11
rcParams["text.parse_math"] = False  # treat $ as a literal character
rcParams["axes.edgecolor"] = GRAY
rcParams["axes.labelcolor"] = TEXT
rcParams["xtick.color"] = GRAY_DARK
rcParams["ytick.color"] = TEXT
rcParams["axes.titlecolor"] = TEXT


def declutter(ax, keep_left=True, keep_bottom=False):
    """Remove chartjunk: top/right spines, ticks, gridlines."""
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    if not keep_bottom:
        ax.spines["bottom"].set_visible(False)
        ax.tick_params(axis="x", length=0)
    if not keep_left:
        ax.spines["left"].set_visible(False)
        ax.tick_params(axis="y", length=0)
    ax.tick_params(axis="y", length=0)


def save(fig, name):
    path = OUTPUT_DIR / name
    fig.savefig(path, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  wrote {path}")


# ---------------------------------------------------------------------------
# Chart 1: BMI status comparison — the headline insight (36-point gap).
# ---------------------------------------------------------------------------
def chart_bmi():
    fig, ax = plt.subplots(figsize=(11, 5.5))
    fig.subplots_adjust(left=0.18, right=0.96, top=0.82, bottom=0.12)

    neighborhoods = ["Palm Haven", "The Dunes"]
    elevated = [23, 59]
    colors = [GRAY_LIGHT, ACCENT]

    bars = ax.barh(neighborhoods, elevated, color=colors, height=0.55,
                   edgecolor="white", linewidth=2)

    # Direct labels at the end of each bar.
    for bar, value, color in zip(bars, elevated, [GRAY_DARK, ACCENT]):
        ax.text(value + 1.5, bar.get_y() + bar.get_height() / 2,
                f"{value}%", va="center", ha="left",
                fontsize=22, fontweight="bold", color=color)

    # Highlight the 36-point gap with an annotation between the two bars.
    ax.annotate("", xy=(59, 1), xytext=(23, 1),
                arrowprops=dict(arrowstyle="<->", color=GRAY_DARK, lw=1.2))
    ax.text(41, 1.32, "36-point gap", ha="center", va="bottom",
            fontsize=12, fontweight="bold", color=GRAY_DARK)

    ax.set_xlim(0, 75)
    ax.set_ylim(-0.6, 1.7)
    ax.set_yticks(range(len(neighborhoods)))
    ax.set_yticklabels(neighborhoods, fontsize=14, fontweight="bold")
    ax.set_xticks([])
    declutter(ax, keep_left=False)

    fig.text(0.04, 0.94,
             "The Dunes carries 2.5x the rate of elevated BMI of Palm Haven",
             fontsize=17, fontweight="bold", color=TEXT)
    fig.text(0.04, 0.885,
             "Share of residents with elevated BMI (overweight, obese, or severely obese)",
             fontsize=11, color=GRAY_DARK)
    fig.text(0.04, 0.02,
             "Source: Neighborhood health survey  |  The Dunes n=1,200  |  Palm Haven n=800",
             fontsize=9, color=GRAY)

    save(fig, "01_bmi_comparison.png")


# ---------------------------------------------------------------------------
# Chart 2: Income distribution comparison — paired horizontal bars.
# ---------------------------------------------------------------------------
def chart_income():
    fig, axes = plt.subplots(1, 2, figsize=(12, 5.5), sharey=True)
    fig.subplots_adjust(left=0.16, right=0.96, top=0.78, bottom=0.14,
                        wspace=0.08)

    brackets = ["Over $40K", "$25K–$40K", "Under $25K"]
    dunes_vals = [4, 27, 69]
    palm_vals = [45, 38, 16]

    # The Dunes panel.
    ax = axes[0]
    bars = ax.barh(brackets, dunes_vals, color=DUNES, height=0.6,
                   edgecolor="white", linewidth=2)
    for bar, value in zip(bars, dunes_vals):
        ax.text(value + 1.5, bar.get_y() + bar.get_height() / 2,
                f"{value}%", va="center", ha="left",
                fontsize=14, fontweight="bold", color=DUNES)
    ax.set_xlim(0, 80)
    ax.set_title("The Dunes", fontsize=15, fontweight="bold", color=DUNES,
                 loc="left", pad=14)
    ax.text(0, 1.02, "Median income  $29,300", transform=ax.transAxes,
            fontsize=10, color=GRAY_DARK)
    ax.set_xticks([])
    declutter(ax, keep_left=False)
    ax.tick_params(axis="y", labelsize=12, colors=TEXT)

    # Palm Haven panel.
    ax = axes[1]
    bars = ax.barh(brackets, palm_vals, color=PALM_HAVEN, height=0.6,
                   edgecolor="white", linewidth=2)
    for bar, value in zip(bars, palm_vals):
        ax.text(value + 1.5, bar.get_y() + bar.get_height() / 2,
                f"{value}%", va="center", ha="left",
                fontsize=14, fontweight="bold", color=PALM_HAVEN)
    ax.set_xlim(0, 80)
    ax.set_title("Palm Haven", fontsize=15, fontweight="bold", color=PALM_HAVEN,
                 loc="left", pad=14)
    ax.text(0, 1.02, "Median income  $70,600", transform=ax.transAxes,
            fontsize=10, color=GRAY_DARK)
    ax.set_xticks([])
    declutter(ax, keep_left=False)

    fig.text(0.04, 0.93,
             "Income concentrates at opposite ends of the spectrum",
             fontsize=17, fontweight="bold", color=TEXT)
    fig.text(0.04, 0.875,
             "69% of Dunes residents earn under $25K; 45% of Palm Haven residents earn over $40K",
             fontsize=11, color=GRAY_DARK)
    fig.text(0.04, 0.03,
             "Source: Household income survey  |  Median income shown for reference",
             fontsize=9, color=GRAY)

    save(fig, "02_income_distribution.png")


# ---------------------------------------------------------------------------
# Chart 3: Demographics — children under 18, Spanish-primary speakers.
# ---------------------------------------------------------------------------
def chart_demographics():
    fig, axes = plt.subplots(2, 1, figsize=(11, 6.2))
    fig.subplots_adjust(left=0.18, right=0.96, top=0.82, bottom=0.10,
                        hspace=0.55)

    metrics = [
        ("Children under 18", 31, 16, "% of residents"),
        ("Spanish as primary language", 15, 6, "% of residents"),
    ]

    for ax, (label, dunes_val, palm_val, _) in zip(axes, metrics):
        ax.barh(["Palm Haven", "The Dunes"], [palm_val, dunes_val],
                color=[PALM_HAVEN, DUNES], height=0.55,
                edgecolor="white", linewidth=2)

        for i, value in enumerate([palm_val, dunes_val]):
            color = PALM_HAVEN if i == 0 else DUNES
            ax.text(value + 0.6, i, f"{value}%", va="center", ha="left",
                    fontsize=15, fontweight="bold", color=color)

        ax.set_xlim(0, 40)
        ax.set_xticks([])
        ax.set_title(label, fontsize=13, fontweight="bold", color=TEXT,
                     loc="left", pad=8)
        declutter(ax, keep_left=False)
        ax.tick_params(axis="y", labelsize=12, colors=TEXT)

    fig.text(0.04, 0.94,
             "The Dunes serves a younger, more linguistically diverse population",
             fontsize=16, fontweight="bold", color=TEXT)
    fig.text(0.04, 0.895,
             "Nearly 1 in 3 Dunes residents is a child; Spanish-primary speakers are 2.5x more common",
             fontsize=10.5, color=GRAY_DARK)
    fig.text(0.04, 0.02,
             "Source: Neighborhood demographic survey",
             fontsize=9, color=GRAY)

    save(fig, "03_demographics.png")


# ---------------------------------------------------------------------------
# Chart 4: Combined infographic — single page summary.
# ---------------------------------------------------------------------------
def chart_combined():
    fig = plt.figure(figsize=(13, 10.5))
    gs = fig.add_gridspec(3, 2,
                          left=0.07, right=0.97, top=0.80, bottom=0.06,
                          hspace=1.00, wspace=0.20,
                          height_ratios=[1.1, 1.0, 1.0])

    # Header.
    fig.text(0.07, 0.95,
             "Two neighborhoods, two very different starting points",
             fontsize=20, fontweight="bold", color=TEXT)
    fig.text(0.07, 0.915,
             "The Dunes (1,200 residents) compared with Palm Haven (800 residents)",
             fontsize=12, color=GRAY_DARK)

    # Color key (replaces a legend).
    fig.text(0.07, 0.875, "■  The Dunes",
             fontsize=12, color=DUNES, fontweight="bold")
    fig.text(0.20, 0.875, "■  Palm Haven",
             fontsize=12, color=PALM_HAVEN, fontweight="bold")

    # --- Top row: BMI focal point spans both columns. -----------------------
    ax_bmi = fig.add_subplot(gs[0, :])
    bars = ax_bmi.barh(["Palm Haven", "The Dunes"], [23, 59],
                       color=[GRAY_LIGHT, ACCENT], height=0.55,
                       edgecolor="white", linewidth=2)
    for bar, value, color in zip(bars, [23, 59], [GRAY_DARK, ACCENT]):
        ax_bmi.text(value + 1.2, bar.get_y() + bar.get_height() / 2,
                    f"{value}%", va="center", ha="left",
                    fontsize=20, fontweight="bold", color=color)
    ax_bmi.annotate("", xy=(59, 1), xytext=(23, 1),
                    arrowprops=dict(arrowstyle="<->", color=GRAY_DARK,
                                    lw=1.1))
    ax_bmi.text(41, 1.3, "36-point gap", ha="center", va="bottom",
                fontsize=11, fontweight="bold", color=GRAY_DARK)
    ax_bmi.set_xlim(0, 75)
    ax_bmi.set_ylim(-0.6, 1.7)
    ax_bmi.set_xticks([])
    ax_bmi.tick_params(axis="y", labelsize=12, colors=TEXT)
    ax_bmi.set_title("Elevated BMI rate", fontsize=13, fontweight="bold",
                     color=TEXT, loc="left", pad=8)
    declutter(ax_bmi, keep_left=False)

    # --- Middle row: income (Dunes left, Palm Haven right). -----------------
    brackets = ["Over $40K", "$25K–$40K", "Under $25K"]
    income_panels = [
        (gs[1, 0], "Income — The Dunes", [4, 27, 69], DUNES, "Median $29,300"),
        (gs[1, 1], "Income — Palm Haven", [45, 38, 16], PALM_HAVEN,
         "Median $70,600"),
    ]
    for slot, title, vals, color, sub in income_panels:
        ax = fig.add_subplot(slot)
        ax.barh(brackets, vals, color=color, height=0.6,
                edgecolor="white", linewidth=2)
        for i, value in enumerate(vals):
            ax.text(value + 1.2, i, f"{value}%", va="center", ha="left",
                    fontsize=12, fontweight="bold", color=color)
        ax.set_xlim(0, 80)
        ax.set_xticks([])
        ax.set_title(title, fontsize=12, fontweight="bold", color=TEXT,
                     loc="left", pad=22)
        ax.text(0, 1.04, sub, transform=ax.transAxes,
                fontsize=10, color=GRAY_DARK)
        ax.tick_params(axis="y", labelsize=10.5, colors=TEXT)
        declutter(ax, keep_left=False)

    # --- Bottom row: demographics. ------------------------------------------
    demo_panels = [
        (gs[2, 0], "Children under 18", 31, 16),
        (gs[2, 1], "Spanish as primary language", 15, 6),
    ]
    for slot, title, dunes_val, palm_val in demo_panels:
        ax = fig.add_subplot(slot)
        ax.barh(["Palm Haven", "The Dunes"], [palm_val, dunes_val],
                color=[PALM_HAVEN, DUNES], height=0.55,
                edgecolor="white", linewidth=2)
        for i, value in enumerate([palm_val, dunes_val]):
            color = PALM_HAVEN if i == 0 else DUNES
            ax.text(value + 0.6, i, f"{value}%", va="center", ha="left",
                    fontsize=12, fontweight="bold", color=color)
        ax.set_xlim(0, 40)
        ax.set_xticks([])
        ax.set_title(title, fontsize=12, fontweight="bold", color=TEXT,
                     loc="left", pad=8)
        ax.tick_params(axis="y", labelsize=10.5, colors=TEXT)
        declutter(ax, keep_left=False)

    fig.text(0.07, 0.025,
             "Source: Neighborhood health, income, and demographic surveys  |  "
             "Percentages may not sum to 100 due to rounding",
             fontsize=9, color=GRAY)

    save(fig, "04_combined_infographic.png")


def main():
    print("Generating charts...")
    chart_bmi()
    chart_income()
    chart_demographics()
    chart_combined()
    print("Done.")


if __name__ == "__main__":
    main()
