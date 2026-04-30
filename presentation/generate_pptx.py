"""
Generate Clear City presentations as native, editable PowerPoint files.

Two outputs, mirroring the HTML decks:
  - clear-city-short.pptx  (4 main + 3 appendix slides; ~3 minutes)
  - clear-city-final.pptx  (9 slides; ~7 minutes)

Each slide is built from text boxes and image placements - no master-slide
templates - so opening either file in PowerPoint, Keynote, or Google Slides
gives you fully editable text, fully replaceable images.

Run:
    python3 presentation/generate_pptx.py
"""

from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Inches, Pt

ROOT = Path(__file__).parent
CHARTS = ROOT.parent / "charts" / "alternatives"

# ---------- Brand palette (same hex values as the HTML decks) ----------
DUNES      = RGBColor(0x8B, 0x6F, 0x47)
PALM       = RGBColor(0x2C, 0x7A, 0x7B)
ACCENT     = RGBColor(0xA8, 0x43, 0x1E)
GRAY_DARK  = RGBColor(0x59, 0x59, 0x59)
GRAY       = RGBColor(0xA6, 0xA6, 0xA6)
GRAY_LIGHT = RGBColor(0xD9, 0xD9, 0xD9)
TEXT       = RGBColor(0x26, 0x26, 0x26)
WHITE      = RGBColor(0xFF, 0xFF, 0xFF)
ACCENT_BG  = RGBColor(0xFA, 0xF3, 0xEE)

# ---------- Slide geometry ----------
SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)


def new_presentation():
    prs = Presentation()
    prs.slide_width = SLIDE_W
    prs.slide_height = SLIDE_H
    return prs


def blank_slide(prs):
    return prs.slides.add_slide(prs.slide_layouts[6])  # 6 = Blank


def add_text(slide, x, y, w, h, text, *,
             size=18, bold=False, color=TEXT,
             align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP,
             font="Calibri", letter_spacing=None):
    """Add a single-run text box. Convenience wrapper."""
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0)
    tf.margin_top = tf.margin_bottom = Inches(0.05)
    tf.vertical_anchor = anchor
    p = tf.paragraphs[0]
    p.alignment = align
    r = p.add_run()
    r.text = text
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.color.rgb = color
    r.font.name = font
    return tb


def add_runs(slide, x, y, w, h, runs, *,
             align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP,
             font="Calibri"):
    """Add a text box composed of multiple coloured runs in one paragraph.

    `runs` is a list of (text, size, bold, color) tuples.
    """
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0)
    tf.margin_top = tf.margin_bottom = Inches(0.05)
    tf.vertical_anchor = anchor
    p = tf.paragraphs[0]
    p.alignment = align
    for text, size, bold, color in runs:
        r = p.add_run()
        r.text = text
        r.font.size = Pt(size)
        r.font.bold = bold
        r.font.color.rgb = color
        r.font.name = font
    return tb


def add_kicker(slide, text, *, x=Inches(0.6), y=Inches(0.45)):
    """Uppercase, letter-spaced kicker text - top of slide."""
    add_text(slide, x, y, Inches(12), Inches(0.4),
             text.upper(), size=11, bold=True, color=GRAY,
             font="Calibri")


def add_values_bar(slide, items=("Clarity", "Equity", "Access for every resident")):
    """Footer values bar centered at bottom."""
    text = "  ·  ".join(items).upper()
    add_text(slide, Inches(0), Inches(7.05), Inches(13.333), Inches(0.3),
             text, size=9, color=GRAY, align=PP_ALIGN.CENTER)


def add_image_centered(slide, image_path, top, max_height=Inches(4.2),
                       max_width=Inches(11.5)):
    """Add image centered horizontally; preserve aspect ratio."""
    from PIL import Image
    with Image.open(image_path) as im:
        iw, ih = im.size
    aspect = iw / ih
    h = max_height
    w = Inches(max_height.inches * aspect)
    if w > max_width:
        w = max_width
        h = Inches(max_width.inches / aspect)
    left = Inches((SLIDE_W.inches - w.inches) / 2)
    slide.shapes.add_picture(str(image_path), left, top, width=w, height=h)


def add_takeaway_box(slide, text, top, *, accent_color=ACCENT):
    """Highlighted takeaway with accent left border."""
    box_x = Inches(1.2)
    box_w = Inches(10.9)
    box_h = Inches(0.9)
    # Background
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, box_x, top, box_w, box_h)
    bg.fill.solid()
    bg.fill.fore_color.rgb = ACCENT_BG
    bg.line.fill.background()
    bg.shadow.inherit = False
    # Accent stripe on left
    stripe = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,
                                    box_x, top, Inches(0.08), box_h)
    stripe.fill.solid()
    stripe.fill.fore_color.rgb = accent_color
    stripe.line.fill.background()
    # Text
    tb = slide.shapes.add_textbox(box_x + Inches(0.3), top + Inches(0.1),
                                  box_w - Inches(0.5), box_h - Inches(0.2))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    r = p.add_run()
    r.text = text
    r.font.size = Pt(15)
    r.font.color.rgb = TEXT
    r.font.name = "Calibri"


def add_two_card(slide, left_title, left_items, right_title, right_items,
                 top=Inches(2.6)):
    """Two-card layout (Dunes / Palm Haven style)."""
    card_w = Inches(5.85)
    card_h = Inches(3.6)
    gutter = Inches(0.4)

    cards = [
        (Inches(0.8),                          left_title,  DUNES, left_items),
        (Inches(0.8) + card_w + gutter,        right_title, PALM,  right_items),
    ]

    for x, title, color, items in cards:
        # Top accent bar
        bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, top,
                                     card_w, Inches(0.06))
        bar.fill.solid()
        bar.fill.fore_color.rgb = color
        bar.line.fill.background()

        # Card title
        add_text(slide, x, top + Inches(0.18),
                 card_w, Inches(0.5),
                 title, size=22, bold=True, color=color)

        # Items
        body_top = top + Inches(0.85)
        for i, item in enumerate(items):
            tb = slide.shapes.add_textbox(x, body_top + Inches(0.55 * i),
                                          card_w, Inches(0.55))
            tf = tb.text_frame
            tf.word_wrap = True
            tf.margin_left = tf.margin_right = Inches(0)
            p = tf.paragraphs[0]
            p.alignment = PP_ALIGN.LEFT

            # Each item is (bold_part, normal_part) tuple
            bold_part, normal_part = item
            r1 = p.add_run()
            r1.text = "• " + bold_part
            r1.font.size = Pt(14)
            r1.font.bold = True
            r1.font.color.rgb = TEXT
            r1.font.name = "Calibri"

            r2 = p.add_run()
            r2.text = " — " + normal_part
            r2.font.size = Pt(14)
            r2.font.color.rgb = GRAY_DARK
            r2.font.name = "Calibri"


def set_notes(slide, notes_text):
    """Attach speaker notes."""
    notes_slide = slide.notes_slide
    tf = notes_slide.notes_text_frame
    tf.text = notes_text


# ────────────────────────────────────────────────────────────────────
# Slide builders shared between decks
# ────────────────────────────────────────────────────────────────────
def build_title_slide(prs, *, kicker_text, big_title_runs, subtitle, tagline,
                      notes):
    s = blank_slide(prs)
    # Kicker top-centered
    add_text(s, Inches(0), Inches(0.7), Inches(13.333), Inches(0.4),
             kicker_text.upper(), size=11, bold=True, color=GRAY,
             align=PP_ALIGN.CENTER)
    # Big title - multi-run for color emphasis
    add_runs(s, Inches(0), Inches(2.4), Inches(13.333), Inches(2.0),
             big_title_runs, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    # Subtitle
    add_text(s, Inches(0), Inches(4.6), Inches(13.333), Inches(0.5),
             subtitle, size=18, color=GRAY_DARK, align=PP_ALIGN.CENTER)
    # Tagline
    add_text(s, Inches(0), Inches(5.2), Inches(13.333), Inches(0.5),
             tagline, size=14, color=GRAY_DARK, align=PP_ALIGN.CENTER)
    add_values_bar(s)
    set_notes(s, notes)
    return s


def build_chart_slide(prs, *, kicker, title, image_path, takeaway, notes,
                      values_bar_items=None):
    s = blank_slide(prs)
    add_kicker(s, kicker)
    add_text(s, Inches(0.6), Inches(0.95), Inches(12), Inches(0.7),
             title, size=30, bold=True, color=TEXT)
    # If there's a takeaway, leave room for it; otherwise let image breathe.
    if takeaway:
        add_image_centered(s, image_path, Inches(1.85),
                           max_height=Inches(3.7))
        add_takeaway_box(s, takeaway, Inches(5.85))
    else:
        add_image_centered(s, image_path, Inches(1.85),
                           max_height=Inches(4.6))
    if values_bar_items:
        add_values_bar(s, values_bar_items)
    set_notes(s, notes)
    return s


def build_two_card_slide(prs, *, kicker, title, left_title, left_items,
                         right_title, right_items, takeaway, notes):
    s = blank_slide(prs)
    add_kicker(s, kicker)
    add_text(s, Inches(0.6), Inches(0.95), Inches(12), Inches(0.7),
             title, size=30, bold=True, color=TEXT)
    add_two_card(s, left_title, left_items, right_title, right_items)
    if takeaway:
        add_takeaway_box(s, takeaway, Inches(6.4))
    set_notes(s, notes)
    return s


def build_close_slide(prs, *, title, subtitle, notes):
    s = blank_slide(prs)
    add_text(s, Inches(0), Inches(1.0), Inches(13.333), Inches(0.4),
             "THANK YOU", size=11, bold=True, color=GRAY,
             align=PP_ALIGN.CENTER)
    add_text(s, Inches(0), Inches(2.4), Inches(13.333), Inches(2.5),
             title, size=44, bold=True, color=TEXT,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, Inches(0), Inches(5.0), Inches(13.333), Inches(0.5),
             subtitle, size=16, color=GRAY_DARK, align=PP_ALIGN.CENTER)
    set_notes(s, notes)
    return s


# ────────────────────────────────────────────────────────────────────
# Title-slide runs (the only multi-color heading we need)
# ────────────────────────────────────────────────────────────────────
TITLE_RUNS = [
    ("Two Neighborhoods, ",   54, True, TEXT),
    ("Two ",                  54, True, DUNES),
    ("Communications Strategies", 54, True, PALM),
]


# ════════════════════════════════════════════════════════════════════
# SHORT DECK (Apr 30 draft, 3 minutes)
# ════════════════════════════════════════════════════════════════════
def build_short_deck():
    prs = new_presentation()

    # 1. Title
    build_title_slide(
        prs,
        kicker_text="Clear City · Communications Director · 3-minute pitch",
        big_title_runs=TITLE_RUNS,
        subtitle="The Dunes · 1,200 residents    |    Palm Haven · 800 residents",
        tagline="Same city. Same services. Profoundly different starting points.",
        notes=(
            "Good [morning / afternoon]. I'm [your name], and I'm here to apply for "
            "Communications Director. In the next three minutes I'll do three things — "
            "show you a story I found in our city's data, tell you what I'd do about it, "
            "and let the work itself show you how I'd communicate for Clear City."
        ),
    )

    # 2. Slope chart (the data)
    build_chart_slide(
        prs,
        kicker="What the data shows",
        title="Two neighborhoods. One picture.",
        image_path=CHARTS / "C_slope_chart.png",
        takeaway=(
            "On every measure that matters, these two neighborhoods are starting in "
            "different places. The widest gap — a 36-point difference in residents "
            "with elevated BMI — is the one we cannot ignore."
        ),
        values_bar_items=("One chart, five facts", "Plain numbers",
                          "Readable for everyone"),
        notes=(
            "One chart, two neighborhoods, five facts. The steeper the line, the bigger the gap.\n\n"
            "The headline: fifty-nine percent of Dunes residents are at elevated weight risk — "
            "versus twenty-three percent in Palm Haven. A thirty-six-point gap.\n\n"
            "Sixty-nine percent of Dunes households earn under twenty-five thousand a year. "
            "Forty-five percent of Palm Haven households earn over forty thousand. Incomes at opposite ends.\n\n"
            "The Dunes also has more children — about one in three residents is under eighteen — "
            "and is two-and-a-half times more likely to use Spanish at home.\n\n"
            "Same city. Same services on offer. Profoundly different starting points."
        ),
    )

    # 3. Two strategies
    build_two_card_slide(
        prs,
        kicker="What I'd do about it",
        title="Two neighborhoods. Two strategies.",
        left_title="The Dunes",
        left_items=[
            ("Spanish first", "written natively, plain language"),
            ("Lead with health", "clinics, food access, family programs"),
            ("Trusted messengers", "schools, faith leaders, community health workers"),
            ("Print, text, in-person", "meet people on the channels they use"),
        ],
        right_title="Palm Haven",
        right_items=[
            ("Digital-first", "screen-reader friendly, captioned video"),
            ("Lead with civic engagement", "volunteering, advocacy, town halls"),
            ("Self-serve resources", "clear portals, on-demand video"),
            ("Monthly newsletter", "opt-in, data-rich, transparent"),
        ],
        takeaway=(
            "The goal — every Clear City resident reached on a channel they use, "
            "in a language they speak, at a reading level they understand."
        ),
        notes=(
            "So what does this mean for Clear City? Two strategies, not one.\n\n"
            "For The Dunes — Spanish first. Written in Spanish from day one, not translated at the end. "
            "Plain language — short sentences, everyday words. Health is the through-line. "
            "The schools, the faith communities, and community health workers carry the message. "
            "Print, text message, and in-person. Not email-first.\n\n"
            "For Palm Haven — digital-first works. Captioned video, screen-reader friendly, "
            "keyboard-accessible. Lead with civic engagement. Self-serve, transparent, data-rich.\n\n"
            "In my first ninety days I'd audit what we already publish, build the Spanish-language "
            "and accessibility workflow, and re-mix the channels."
        ),
    )

    # 4. Close
    build_close_slide(
        prs,
        title="I'd be honored to do this work for Clear City.",
        subtitle="Two neighborhoods. Two strategies. One goal — every resident reached.",
        notes="Thank you. I'd be honored to do this work for Clear City. I'm happy to take questions.",
    )

    # ───────── Appendix slides (Q&A backup) ─────────
    # A. Dot plot
    build_chart_slide(
        prs,
        kicker="Appendix · zooming in on the headline",
        title="The 36-point gap, on its own.",
        image_path=CHARTS / "A_dot_plot.png",
        takeaway=None,
        notes=(
            "Use this slide if a panelist asks: 'Can you show just the BMI number on its own?' "
            "The dot plot is the simplest possible chart — two values, the distance between them."
        ),
    )

    # B. Lollipop
    build_chart_slide(
        prs,
        kicker="Appendix · all metrics, side by side",
        title="Every metric, paired and labeled.",
        image_path=CHARTS / "B_lollipop.png",
        takeaway=None,
        notes=(
            "Use this slide if a panelist asks: 'Can you break out each metric separately?' "
            "Trades the slope chart's at-a-glance view for clearer per-metric reading."
        ),
    )

    # D. Diverging bars
    build_chart_slide(
        prs,
        kicker="Appendix · income, in detail",
        title="Incomes pulling in opposite directions.",
        image_path=CHARTS / "D_diverging_bars.png",
        takeaway=None,
        notes=(
            "Use this slide if a panelist asks: 'Tell me more about the income story.' "
            "The asymmetry makes the case for different channels in each neighborhood."
        ),
    )

    out = ROOT / "clear-city-short.pptx"
    prs.save(str(out))
    print(f"  wrote {out}")
    return out


# ════════════════════════════════════════════════════════════════════
# FINAL DECK (May 14, ~7 minutes)
# ════════════════════════════════════════════════════════════════════
def build_final_deck():
    prs = new_presentation()

    # 1. Title
    build_title_slide(
        prs,
        kicker_text="Clear City · Communications Director · Final Presentation",
        big_title_runs=TITLE_RUNS,
        subtitle="A data-informed, equity-first approach for Clear City",
        tagline="",
        notes=(
            "Good [morning / afternoon]. I'm [your name], applying for Communications Director.\n\n"
            "Two weeks ago I gave you a three-minute draft of this talk. You gave me thoughtful feedback. "
            "Today's seven-minute version is what I built from it — a fuller view of the data, "
            "a more concrete strategy, and a clearer plan for how I'd measure whether it's working."
        ),
    )

    # 2. Setup
    build_two_card_slide(
        prs,
        kicker="The brief, in one slide",
        title="Two neighborhoods inside one city.",
        left_title="The Dunes",
        left_items=[
            ("1,200 residents", ""),
            ("Working-class", "younger, multilingual"),
            ("Significant health needs",
             "elevated BMI affects 59% of residents"),
        ],
        right_title="Palm Haven",
        right_items=[
            ("800 residents", ""),
            ("Mid-to-upper income", "strong digital access"),
            ("High civic engagement", "engaged with city services"),
        ],
        takeaway=(
            "Same city. Same services on offer. Profoundly different starting points — "
            "and that means our communications cannot be one-size-fits-all."
        ),
        notes=(
            "Two neighborhoods, both in Clear City. The Dunes — twelve hundred residents, "
            "working-class, younger, more multilingual, with serious health needs. "
            "Palm Haven — eight hundred residents, mid-to-upper income, digitally connected, "
            "civically engaged. Same city, same services on offer. The data tells me they need "
            "profoundly different communications. Let me show you why."
        ),
    )

    # 3. Lollipop B
    build_chart_slide(
        prs,
        kicker="Five things I looked at",
        title="The metrics that matter for outreach.",
        image_path=CHARTS / "B_lollipop.png",
        takeaway=None,
        notes=(
            "Five things I looked at — health, age, language, and the two ends of the income spectrum. "
            "I picked these because each one changes how we should communicate. "
            "Health drives what we lead with. Age affects how we talk to families. "
            "Language affects whether we get through at all. And income shapes which channels reach people."
        ),
    )

    # 4. Slope C
    build_chart_slide(
        prs,
        kicker="The gaps tell a story",
        title="Same data. Tilted view. Different revelation.",
        image_path=CHARTS / "C_slope_chart.png",
        takeaway=(
            "Every metric diverges. The steepest line — the 36-point health gap — "
            "is the one I cannot ignore."
        ),
        notes=(
            "Now look at the same data tilted ninety degrees. Each line connects the same metric "
            "across the two neighborhoods. The steeper the line, the bigger the gap. "
            "Four of the five lines slope downward — The Dunes higher than Palm Haven on health risk, "
            "children, Spanish at home, and lower income. One line goes the other way — higher income, "
            "where Palm Haven is far ahead. The steepest line — and the most consequential one — is the health gap."
        ),
    )

    # 5. Dot plot A
    build_chart_slide(
        prs,
        kicker="The headline",
        title="A 36-point health gap.",
        image_path=CHARTS / "A_dot_plot.png",
        takeaway=(
            "In Palm Haven, this is one campaign a year. In The Dunes, it's the through-line "
            "of everything we publish."
        ),
        notes=(
            "Fifty-nine percent of Dunes residents are at elevated weight risk. Twenty-three percent "
            "in Palm Haven. A thirty-six-point gap. For context: a thirty-six-point gap is the "
            "difference between a public-health emergency and a healthy community.\n\n"
            "In Palm Haven, health is one campaign a year. In The Dunes, it's the through-line of "
            "everything we publish — every newsletter, every event, every billboard touches it somehow."
        ),
    )

    # 6. Diverging bars D
    build_chart_slide(
        prs,
        kicker="The channel question",
        title="Why income demands different channels.",
        image_path=CHARTS / "D_diverging_bars.png",
        takeaway=(
            "69% of Dunes households earn under $25K. 45% of Palm Haven earns over $40K. "
            "The right channel mix is different in each neighborhood."
        ),
        notes=(
            "Income flips the script. Sixty-nine percent of Dunes households earn under twenty-five "
            "thousand a year. Forty-five percent of Palm Haven households earn over forty thousand. "
            "That gap matters because it shapes which channels actually reach people. "
            "Households in The Dunes are less likely to have unlimited data — so print, text, "
            "and in-person aren't fallbacks, they're the front door. Households in Palm Haven "
            "have all of those things. Email and self-serve portals aren't shortcuts — they're "
            "respectful of how this community wants to engage."
        ),
    )

    # 7. Two strategies
    build_two_card_slide(
        prs,
        kicker="What I'd do about it",
        title="Two neighborhoods. Two strategies.",
        left_title="The Dunes",
        left_items=[
            ("Spanish first", "written natively, plain language"),
            ("Lead with health", "clinics, food access, family programs"),
            ("Trusted messengers", "schools, faith leaders, community health workers"),
            ("Print, text, in-person", "channels people actually use"),
            ("Multimodal", "same message, three formats"),
        ],
        right_title="Palm Haven",
        right_items=[
            ("Digital-first", "captioned video, screen-reader friendly"),
            ("Lead with civic engagement", "volunteering, advocacy, town halls"),
            ("Self-serve resources", "clear portals, on-demand video"),
            ("Monthly newsletter", "opt-in, data-rich, transparent"),
            ("Two-way", "comment forms, surveys, public meetings"),
        ],
        takeaway=None,
        notes=(
            "Two strategies, not one. The Dunes — Spanish first, written natively. Plain language. "
            "Health as the through-line. Trusted messengers — schools, faith leaders, community health "
            "workers — carry the message. Print, text, in-person. Same message, three formats.\n\n"
            "Palm Haven — digital-first works. Captioned video, screen-reader friendly. Lead with "
            "civic engagement. Self-serve, transparent, data-rich. Two-way — comment forms, surveys, "
            "public meetings. They want to engage with us, not just receive us."
        ),
    )

    # 8. 90-day plan + measurement
    build_two_card_slide(
        prs,
        kicker="First 90 days & how I'll measure",
        title="Sequenced. Measurable. Honest.",
        left_title="First 90 days",
        left_items=[
            ("Days 1–30 — Audit", "inventory every channel; translate nothing yet"),
            ("Days 31–60 — Build", "Spanish-language editor; accessibility workflow"),
            ("Days 61–90 — Re-mix", "SMS pilot, email cleanup, sunset what isn't working"),
        ],
        right_title="How I'll know it's working",
        right_items=[
            ("Reach by neighborhood", "never aggregate"),
            ("Outcome metrics", "clinic visits, town halls, enrollments"),
            ("Accessibility scan", "every published asset"),
            ("Trust surveys", "before-and-after every event"),
        ],
        takeaway=None,
        notes=(
            "Sequenced. Measurable. Honest.\n\n"
            "First thirty days — audit. I don't translate anything until I understand what's already "
            "in market. Next thirty — build. A Spanish-language editor. An accessibility checklist on "
            "every asset. Final thirty — re-mix. SMS for The Dunes. A clean email program for Palm Haven. "
            "Sunset what isn't working.\n\n"
            "And here's how I'll know it's working — reach by neighborhood, never aggregate, because "
            "aggregate dashboards hide the gap. Outcome metrics tied to program goals. Accessibility "
            "scans. And short trust surveys, before and after every event."
        ),
    )

    # 9. Close
    build_close_slide(
        prs,
        title="I'd be honored to do this work for Clear City.",
        subtitle="Two neighborhoods. Two strategies. One goal — every resident reached.",
        notes="Thank you. I'd be honored to do this work for Clear City. I'm happy to take questions.",
    )

    # Color the second card on slides 8 differently (overrides default DUNES/PALM)
    # Simpler: leave defaults; visual works fine.

    out = ROOT / "clear-city-final.pptx"
    prs.save(str(out))
    print(f"  wrote {out}")
    return out


def main():
    print("Generating PowerPoint files...")
    build_short_deck()
    build_final_deck()
    print("Done.")


if __name__ == "__main__":
    main()
