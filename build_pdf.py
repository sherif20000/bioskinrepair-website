#!/usr/bin/env python3
"""
BioSkinRepair — 7-Day Skin Barrier Reset Guide
Full rebuild with exact brand identity + rich visuals/infographics.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white, black, Color
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate, SimpleDocTemplate,
    Paragraph, Spacer, Table, TableStyle, PageBreak,
    HRFlowable, KeepTogether, NextPageTemplate, Image
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus.flowables import Flowable
from reportlab.graphics.shapes import (
    Drawing, Rect, Circle, Line, Polygon, String,
    Path, Group, PolyLine
)
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics import renderPDF
from reportlab.graphics.charts.legends import Legend
import math

# ── Exact brand colors from styles.css ───────────────────────────────────────
ACCENT        = HexColor("#2D5A3D")   # --accent: forest green
ACCENT_LIGHT  = HexColor("#EEF4F1")   # --accent-light
GOLD          = HexColor("#C9A96E")   # --gold
GOLD_HOVER    = HexColor("#B8935A")   # --gold-hover
FOOTER_BG     = HexColor("#0F1F16")   # --footer-bg: very dark green
SAGE          = HexColor("#7A9E85")   # --sage
SAGE_LIGHT    = HexColor("#A8C4B0")   # --sage-light
BG            = HexColor("#FAFAF7")   # --bg: warm off-white
SURFACE       = HexColor("#FFFFFF")
TEXT_PRIMARY  = HexColor("#1A1A18")   # --text-primary
TEXT_SECONDARY= HexColor("#6B7280")   # --text-secondary
BORDER        = HexColor("#E4EDE6")   # --border
GREEN_OK      = HexColor("#1A5C38")   # dark green for "use" list
RED_NO        = HexColor("#9B2335")   # red for "avoid" list
RED_LIGHT     = HexColor("#FBE8E8")
GREEN_LIGHT   = HexColor("#E8F5EE")

PAGE_W, PAGE_H = A4   # 595 x 842 pts


# ── Styles ────────────────────────────────────────────────────────────────────
def S(name, **kw):
    defaults = dict(fontName="Helvetica", fontSize=10, leading=16,
                    textColor=TEXT_PRIMARY, alignment=TA_LEFT)
    defaults.update(kw)
    return ParagraphStyle(name, **defaults)

def styles():
    return {
    "eyebrow":   S("eyebrow", fontName="Helvetica-Bold", fontSize=8,
                   textColor=ACCENT, leading=13, spaceAfter=4,
                   letterSpacing=1.8),
    "h1":        S("h1", fontName="Times-Bold", fontSize=26, leading=32,
                   textColor=TEXT_PRIMARY, spaceAfter=8),
    "h1w":       S("h1w", fontName="Times-Bold", fontSize=26, leading=32,
                   textColor=white, spaceAfter=8),
    "h2":        S("h2", fontName="Times-Bold", fontSize=17, leading=22,
                   textColor=ACCENT, spaceAfter=6, spaceBefore=14),
    "h3":        S("h3", fontName="Times-Bold", fontSize=13, leading=18,
                   textColor=TEXT_PRIMARY, spaceAfter=4, spaceBefore=10),
    "day_n":     S("day_n", fontName="Helvetica-Bold", fontSize=9,
                   textColor=GOLD, leading=13, spaceAfter=2, letterSpacing=1.5),
    "day_title": S("day_title", fontName="Times-Bold", fontSize=22, leading=28,
                   textColor=ACCENT, spaceAfter=3),
    "day_sub":   S("day_sub", fontName="Times-BoldItalic", fontSize=11, leading=16,
                   textColor=TEXT_SECONDARY, spaceAfter=10),
    "body":      S("body", fontName="Helvetica", fontSize=10, leading=17,
                   textColor=TEXT_PRIMARY, spaceAfter=8),
    "body_sm":   S("body_sm", fontName="Helvetica", fontSize=9, leading=14,
                   textColor=TEXT_SECONDARY, spaceAfter=6),
    "bullet":    S("bullet", fontName="Helvetica", fontSize=10, leading=16,
                   textColor=TEXT_PRIMARY, leftIndent=14, spaceAfter=5),
    "step_lbl":  S("step_lbl", fontName="Helvetica-Bold", fontSize=10, leading=15,
                   textColor=ACCENT, leftIndent=0, spaceAfter=2),
    "step_body": S("step_body", fontName="Helvetica", fontSize=9.5, leading=15,
                   textColor=TEXT_PRIMARY, leftIndent=0, spaceAfter=8),
    "why_lbl":   S("why_lbl", fontName="Helvetica-Bold", fontSize=8.5, leading=13,
                   textColor=GOLD),
    "why_body":  S("why_body", fontName="Helvetica-Oblique", fontSize=9.5, leading=14,
                   textColor=TEXT_SECONDARY, leftIndent=8, spaceAfter=8),
    "callout":   S("callout", fontName="Helvetica-Bold", fontSize=9.5, leading=15,
                   textColor=ACCENT),
    "cover_tag": S("cover_tag", fontName="Helvetica-Bold", fontSize=8,
                   textColor=GOLD, leading=12, letterSpacing=2),
    "cover_h1":  S("cover_h1", fontName="Times-Bold", fontSize=40, leading=48,
                   textColor=white, spaceAfter=8),
    "cover_gold":S("cover_gold", fontName="Times-Bold", fontSize=40, leading=48,
                   textColor=GOLD, spaceAfter=12),
    "cover_sub": S("cover_sub", fontName="Helvetica", fontSize=12, leading=20,
                   textColor=HexColor("#A8C4B0"), spaceAfter=0),
    "back_big":  S("back_big", fontName="Times-Bold", fontSize=22, leading=28,
                   textColor=white, alignment=TA_CENTER),
    "back_sub":  S("back_sub", fontName="Helvetica", fontSize=11, leading=17,
                   textColor=HexColor("#A8C4B0"), alignment=TA_CENTER),
    "back_gold": S("back_gold", fontName="Times-BoldItalic", fontSize=12, leading=18,
                   textColor=GOLD, alignment=TA_CENTER),
    "back_url":  S("back_url", fontName="Helvetica", fontSize=9, leading=14,
                   textColor=SAGE, alignment=TA_CENTER),
    "caption":   S("caption", fontName="Helvetica-Oblique", fontSize=8, leading=12,
                   textColor=TEXT_SECONDARY, alignment=TA_CENTER),
    "tbl_head":  S("tbl_head", fontName="Helvetica-Bold", fontSize=9.5, leading=14,
                   textColor=white, alignment=TA_CENTER),
    "tbl_cell":  S("tbl_cell", fontName="Helvetica", fontSize=9, leading=14,
                   textColor=TEXT_PRIMARY),
    "ingr_ok":   S("ingr_ok", fontName="Helvetica", fontSize=9.5, leading=15,
                   textColor=TEXT_PRIMARY, leftIndent=10, spaceAfter=3),
    "ingr_no":   S("ingr_no", fontName="Helvetica", fontSize=9.5, leading=15,
                   textColor=TEXT_PRIMARY, leftIndent=10, spaceAfter=3),
    "note":      S("note", fontName="Helvetica-Oblique", fontSize=8.5, leading=13,
                   textColor=TEXT_SECONDARY),
    }

ST = styles()
IW = PAGE_W - 48 * mm   # inner width (content area)


# ── Page callbacks ────────────────────────────────────────────────────────────

def cb_cover(canvas, doc):
    canvas.saveState()
    w, h = A4
    # Dark green background
    canvas.setFillColor(FOOTER_BG)
    canvas.rect(0, 0, w, h, fill=1, stroke=0)
    # Subtle grid texture
    canvas.setStrokeColor(HexColor("#162A1E"))
    canvas.setLineWidth(0.4)
    for y in range(0, int(h)+1, 24): canvas.line(0, y, w, y)
    # Left accent bar
    canvas.setFillColor(ACCENT)
    canvas.rect(0, 0, 5, h, fill=1, stroke=0)
    # Gold top rule
    canvas.setFillColor(GOLD)
    canvas.rect(0, h-5, w, 5, fill=1, stroke=0)
    # Large "7" watermark
    canvas.setFillColor(HexColor("#182C20"))
    canvas.setFont("Times-Bold", 400)
    canvas.drawCentredString(w/2+50, -30, "7")
    # Right abstract circle ornament
    canvas.setFillColor(HexColor("#1E3A28"))
    canvas.circle(w-30, h*0.55, 110, fill=1, stroke=0)
    canvas.setFillColor(HexColor("#243E2C"))
    canvas.circle(w-30, h*0.55, 80, fill=1, stroke=0)
    canvas.setFillColor(HexColor("#2D5A3D"))
    canvas.circle(w-30, h*0.55, 50, fill=1, stroke=0)
    # Eyebrow
    canvas.setFillColor(GOLD)
    canvas.setFont("Helvetica-Bold", 8)
    canvas.drawString(38, h-48, "B I O S K I N R E P A I R  —  F R E E  G U I D E")
    canvas.setStrokeColor(HexColor("#2D5A3D"))
    canvas.setLineWidth(0.7)
    canvas.line(38, h-58, w-38, h-58)
    # Title
    canvas.setFillColor(white)
    canvas.setFont("Times-Bold", 44)
    canvas.drawString(38, h-128, "The 7-Day")
    canvas.drawString(38, h-178, "Skin Barrier")
    canvas.setFillColor(GOLD)
    canvas.drawString(38, h-228, "Reset Guide")
    # Subtitle
    canvas.setFillColor(HexColor("#A8C4B0"))
    canvas.setFont("Helvetica", 12)
    canvas.drawString(38, h-268, "A clinically-grounded protocol to stop irritation,")
    canvas.drawString(38, h-284, "restore your barrier, and rebuild from scratch.")
    # Divider rule
    canvas.setStrokeColor(HexColor("#2D5A3D"))
    canvas.setLineWidth(1)
    canvas.line(38, h-304, w-38, h-304)
    # Three phases
    phases = [("PHASE 1","Stop the Damage"),("PHASE 2","Support Repair"),("PHASE 3","Maintain & Protect")]
    x = 38
    for lbl, txt in phases:
        canvas.setFillColor(GOLD)
        canvas.setFont("Helvetica-Bold", 7.5)
        canvas.drawString(x, h-322, lbl)
        canvas.setFillColor(HexColor("#A8C4B0"))
        canvas.setFont("Helvetica", 9.5)
        canvas.drawString(x, h-336, txt)
        # Arrow
        if lbl != "PHASE 3":
            ax = x + 150
            canvas.setStrokeColor(GOLD)
            canvas.setLineWidth(0.7)
            canvas.line(ax-4, h-329, ax+10, h-329)
            canvas.line(ax+6, h-333, ax+10, h-329)
            canvas.line(ax+6, h-325, ax+10, h-329)
        x += 170
    # Bottom bar
    canvas.setFillColor(HexColor("#0A1610"))
    canvas.rect(0, 0, w, 60, fill=1, stroke=0)
    canvas.setFillColor(GOLD)
    canvas.setFont("Times-Bold", 14)
    canvas.drawString(38, 34, "BioSkinRepair")
    canvas.setFillColor(SAGE)
    canvas.setFont("Helvetica", 8.5)
    canvas.drawString(38, 20, "bioskinrepair.com")
    canvas.setFillColor(HexColor("#4A7A5A"))
    canvas.setFont("Helvetica-Oblique", 8)
    canvas.drawRightString(w-38, 20, "The science of skin recovery.")
    canvas.restoreState()


def cb_inner(canvas, doc):
    canvas.saveState()
    w, h = A4
    # Top header bar
    canvas.setFillColor(ACCENT)
    canvas.rect(0, h-34, w, 34, fill=1, stroke=0)
    # Gold micro-strip under header
    canvas.setFillColor(GOLD)
    canvas.rect(0, h-36, w, 2, fill=1, stroke=0)
    # Header text
    canvas.setFillColor(GOLD)
    canvas.setFont("Times-Bold", 9)
    canvas.drawString(22, h-22, "BioSkinRepair")
    canvas.setFillColor(HexColor("#A8C4B0"))
    canvas.setFont("Helvetica", 8)
    canvas.drawRightString(w-22, h-22, "The 7-Day Skin Barrier Reset Guide")
    # Left accent bar (thin)
    canvas.setFillColor(ACCENT)
    canvas.rect(0, 0, 3, h-36, fill=1, stroke=0)
    # Footer rule
    canvas.setStrokeColor(BORDER)
    canvas.setLineWidth(0.6)
    canvas.line(22, 28, w-22, 28)
    # Footer text
    canvas.setFillColor(TEXT_SECONDARY)
    canvas.setFont("Helvetica", 7.5)
    canvas.drawString(22, 16, "bioskinrepair.com  |  For educational purposes only. Not a substitute for medical advice.")
    canvas.drawRightString(w-22, 16, f"{doc.page}")
    canvas.restoreState()


def cb_back(canvas, doc):
    canvas.saveState()
    w, h = A4
    canvas.setFillColor(FOOTER_BG)
    canvas.rect(0, 0, w, h, fill=1, stroke=0)
    # Grid texture
    canvas.setStrokeColor(HexColor("#162A1E"))
    canvas.setLineWidth(0.3)
    for y in range(0, int(h)+1, 24): canvas.line(0, y, w, y)
    # Gold top/bottom rules
    canvas.setFillColor(GOLD)
    canvas.rect(0, h-5, w, 5, fill=1, stroke=0)
    canvas.rect(0, 0, w, 5, fill=1, stroke=0)
    # Left accent
    canvas.setFillColor(ACCENT)
    canvas.rect(0, 5, 5, h-10, fill=1, stroke=0)
    # Circle badge
    cx, cy = w/2, h/2+60
    canvas.setFillColor(HexColor("#1A3020"))
    canvas.circle(cx, cy, 68, fill=1, stroke=0)
    canvas.setStrokeColor(GOLD)
    canvas.setLineWidth(1.5)
    canvas.circle(cx, cy, 66, fill=0, stroke=1)
    canvas.setFillColor(GOLD)
    canvas.setFont("Times-Bold", 22)
    canvas.drawCentredString(cx, cy+2, "BSR")
    canvas.setFillColor(SAGE)
    canvas.setFont("Helvetica", 8)
    canvas.drawCentredString(cx, cy-16, "BioSkinRepair")
    # Headline
    canvas.setFillColor(white)
    canvas.setFont("Times-Bold", 20)
    canvas.drawCentredString(cx, h/2-30, "More at bioskinrepair.com")
    canvas.setFillColor(HexColor("#A8C4B0"))
    canvas.setFont("Helvetica", 10.5)
    canvas.drawCentredString(cx, h/2-52, "The complete guide to skin barrier repair.")
    # Links
    links = [
        "bioskinrepair.com/skin-barrier-101",
        "bioskinrepair.com/ingredients",
        "bioskinrepair.com/routines",
        "bioskinrepair.com/skin-conditions",
    ]
    y = h/2-80
    for link in links:
        canvas.setFillColor(SAGE)
        canvas.setFont("Helvetica", 9)
        canvas.drawCentredString(cx, y, link)
        y -= 17
    # Tagline
    canvas.setFillColor(GOLD)
    canvas.setFont("Times-BoldItalic", 13)
    canvas.drawCentredString(cx, 80, '"The science of skin recovery."')
    canvas.setFillColor(HexColor("#3A6A4A"))
    canvas.setFont("Helvetica", 7.5)
    canvas.drawCentredString(cx, 50, "© 2026 BioSkinRepair. All rights reserved.")
    canvas.restoreState()


# ── Visual Flowables ──────────────────────────────────────────────────────────

def skin_barrier_diagram():
    """Cross-section diagram of the skin barrier — layers, lipids, water loss arrows."""
    d = Drawing(IW, 140)
    bw = IW
    bh = 140
    labels = [
        ("STRATUM CORNEUM",  22,  HexColor("#2D5A3D"), HexColor("#EEF4F1"), "Outermost protective layer"),
        ("GRANULAR LAYER",   18,  HexColor("#3E6B4E"), HexColor("#F0F6F2"), "Lipid synthesis begins here"),
        ("SPINOUS LAYER",    18,  HexColor("#4A7A5A"), HexColor("#F2F7F4"), "Keratinocyte differentiation"),
        ("BASAL LAYER",      18,  HexColor("#5A8A6A"), HexColor("#F4F8F5"), "New cell generation"),
        ("DERMIS",           24,  HexColor("#7A9E85"), HexColor("#F7FAF8"), "Support matrix & blood supply"),
    ]
    y_pos = bh
    for lbl, ht, border_col, fill_col, sub in labels:
        y_pos -= ht
        r = Rect(0, y_pos, bw * 0.72, ht, fillColor=fill_col, strokeColor=border_col, strokeWidth=0.5)
        d.add(r)
        # Brick pattern on stratum corneum
        if lbl == "STRATUM CORNEUM":
            brick_w, brick_h = 28, 8
            col_limit = bw * 0.72  # hard right boundary — no bleed into annotation column
            for row in range(3):
                offset = (row % 2) * (brick_w // 2)
                for col in range(int(col_limit / brick_w) + 2):
                    bx = col * brick_w - offset
                    if bx >= col_limit:
                        continue  # completely outside left panel
                    bw_brick = min(brick_w - 1, col_limit - bx)
                    if bw_brick <= 0:
                        continue
                    by = y_pos + row * (brick_h // 2) + 2
                    br = Rect(bx, by, bw_brick, brick_h // 2 - 1,
                              fillColor=HexColor("#C8DDD0"), strokeColor=border_col, strokeWidth=0.3)
                    d.add(br)
        # Layer label
        d.add(String(8, y_pos + ht/2 - 4, lbl,
                     fontName="Helvetica-Bold", fontSize=6.5,
                     fillColor=TEXT_PRIMARY))
        d.add(String(8, y_pos + ht/2 - 12, sub,
                     fontName="Helvetica", fontSize=5.5,
                     fillColor=TEXT_SECONDARY))

    # Right panel: annotations
    rx = bw * 0.74
    # TEWL arrow (water escaping upward from damaged barrier)
    for i in range(3):
        ax = rx + 12 + i * 22
        d.add(Line(ax, 30, ax, 95, strokeColor=HexColor("#90C0E8"), strokeWidth=1.5,
                   strokeDashArray=[3, 2]))
        d.add(Polygon([ax, 98, ax-4, 90, ax+4, 90],
                      fillColor=HexColor("#90C0E8"), strokeColor=None))

    d.add(String(rx+2, 26, "TEWL", fontName="Helvetica-Bold", fontSize=7, fillColor=HexColor("#5090C0")))
    d.add(String(rx+2, 16, "water loss", fontName="Helvetica", fontSize=6, fillColor=TEXT_SECONDARY))

    # Ceramide icons (small rectangles in the lipid bilayer area)
    for i in range(5):
        cx2 = rx + 50 + i * 10
        d.add(Rect(cx2, 108, 8, 14, fillColor=GOLD, strokeColor=None, rx=2))

    d.add(String(rx+42, 126, "Ceramide", fontName="Helvetica-Bold", fontSize=6.5, fillColor=GOLD))
    d.add(String(rx+42, 117, "lipid matrix", fontName="Helvetica", fontSize=6, fillColor=TEXT_SECONDARY))

    # Border around whole diagram
    d.add(Rect(0, 0, bw, bh, fillColor=None, strokeColor=BORDER, strokeWidth=0.7))

    return d


def three_phase_flow():
    """Horizontal 3-phase infographic: Stop → Support → Maintain."""
    w, h = IW, 72
    d = Drawing(w, h)
    phases = [
        ("01", "STOP", "Remove all actives,\nirritants & damage\ntriggers", ACCENT, HexColor("#EEF4F1")),
        ("02", "SUPPORT", "Feed barrier with\nceramides, humectants\n& occlusives",   HexColor("#1E4A2E"), HexColor("#E6F2EA")),
        ("03", "MAINTAIN", "Lock in progress\nwith a minimal,\nconsistent routine", HexColor("#0F3020"), ACCENT_LIGHT),
    ]
    bw = (w - 30) / 3
    for i, (num, title, body, bg, fg) in enumerate(phases):
        x = i * (bw + 15)
        # Box
        d.add(Rect(x, 0, bw, h, fillColor=bg, strokeColor=BORDER, strokeWidth=0.6, rx=6))
        # Number badge
        d.add(Circle(x + 18, h - 16, 10, fillColor=GOLD, strokeColor=None))
        d.add(String(x + 14, h - 20, num, fontName="Helvetica-Bold", fontSize=7.5, fillColor=FOOTER_BG))
        # Title
        d.add(String(x + 32, h - 20, title, fontName="Helvetica-Bold", fontSize=9, fillColor=white if bg == ACCENT else ACCENT))
        # Body lines
        for j, line in enumerate(body.split("\n")):
            d.add(String(x + 8, h - 34 - j * 11, line, fontName="Helvetica", fontSize=7.5, fillColor=TEXT_SECONDARY))
        # Arrow (not on last)
        if i < 2:
            ax = x + bw + 3
            ay = h / 2
            d.add(Line(ax, ay, ax + 10, ay, strokeColor=GOLD, strokeWidth=1.5))
            d.add(Polygon([ax+10, ay, ax+5, ay+4, ax+5, ay-4], fillColor=GOLD, strokeColor=None))
    return d


def ceramide_pie():
    """Pie chart: 50% ceramides, 25% cholesterol, 15% fatty acids, 10% other."""
    w, h = 220, 145
    d = Drawing(w, h)
    pie = Pie()
    pie.x, pie.y = 20, 22
    pie.width = pie.height = 100
    pie.data = [50, 25, 15, 10]
    pie.labels = ["", "", "", ""]
    pie.slices[0].fillColor = ACCENT
    pie.slices[1].fillColor = GOLD
    pie.slices[2].fillColor = SAGE
    pie.slices[3].fillColor = BORDER
    pie.slices[0].strokeColor = white
    pie.slices[1].strokeColor = white
    pie.slices[2].strokeColor = white
    pie.slices[3].strokeColor = white
    pie.slices[0].strokeWidth = 1
    pie.slices[1].strokeWidth = 1
    pie.slices[2].strokeWidth = 1
    pie.slices[3].strokeWidth = 1
    d.add(pie)
    # Legend
    items = [
        (ACCENT, "Ceramides  50%"),
        (GOLD,   "Cholesterol  25%"),
        (SAGE,   "Fatty Acids  15%"),
        (BORDER, "Other  10%"),
    ]
    for i, (col, lbl) in enumerate(items):
        ly = 95 - i * 20
        d.add(Rect(130, ly, 10, 10, fillColor=col, strokeColor=None))
        d.add(String(145, ly + 1, lbl, fontName="Helvetica", fontSize=8, fillColor=TEXT_PRIMARY))
    # Title
    d.add(String(20, 133, "Skin Barrier Lipid Composition", fontName="Helvetica-Bold",
                 fontSize=8, fillColor=TEXT_PRIMARY))
    return d


def tewl_bar_chart():
    """Bar chart comparing TEWL: Healthy vs Damaged vs Restoring (Day 7)."""
    w, h = 200, 155
    d = Drawing(w, h)
    bc = VerticalBarChart()
    bc.x, bc.y = 40, 38
    bc.height, bc.width = 85, 145
    bc.data = [[8, 24, 14]]  # g/m²/h: healthy, damaged, restoring
    bc.bars[0].fillColor = SAGE
    bc.categoryAxis.categoryNames = ["Healthy", "Compromised", "Day 7"]
    bc.categoryAxis.labels.fontSize = 7
    bc.categoryAxis.labels.fontName = "Helvetica"
    bc.categoryAxis.labels.fillColor = TEXT_SECONDARY
    bc.valueAxis.valueMin = 0
    bc.valueAxis.valueMax = 30
    bc.valueAxis.valueStep = 10
    bc.valueAxis.labels.fontSize = 7
    bc.valueAxis.labels.fontName = "Helvetica"
    bc.valueAxis.labels.fillColor = TEXT_SECONDARY
    bc.bars[0].fillColor = SAGE
    # Color individual bars
    bc.bars[(0,0)].fillColor = ACCENT
    bc.bars[(0,1)].fillColor = RED_NO
    bc.bars[(0,2)].fillColor = GOLD
    bc.strokeColor = None
    bc.barSpacing = 4
    bc.groupSpacing = 16
    d.add(bc)
    d.add(String(40, 143, "TEWL (g/m²/h) — Water Loss Rate", fontName="Helvetica-Bold",
                 fontSize=7.5, fillColor=TEXT_PRIMARY))
    d.add(String(40, 20, "Lower = better barrier integrity", fontName="Helvetica-Oblique",
                 fontSize=6.5, fillColor=TEXT_SECONDARY))
    return d


def day_timeline(active_day):
    """7-dot horizontal timeline with current day highlighted."""
    w, h = IW, 44
    d = Drawing(w, h)
    step = (w - 40) / 6
    for i in range(7):
        x = 20 + i * step
        is_done  = i + 1 < active_day
        is_today = i + 1 == active_day
        fill = ACCENT if is_done else (GOLD if is_today else HexColor("#D0DDD4"))
        r = 10 if is_today else 8
        d.add(Circle(x, h/2, r, fillColor=fill, strokeColor=None))
        if is_today:
            d.add(Circle(x, h/2, r+3, fillColor=None, strokeColor=GOLD, strokeWidth=1.5))
        d.add(String(x - 4 if i < 9 else x - 7, h/2 - 5,
                     str(i+1), fontName="Helvetica-Bold", fontSize=7.5,
                     fillColor=white if (is_done or is_today) else TEXT_SECONDARY))
        d.add(String(x - 8, 6, f"Day {i+1}", fontName="Helvetica", fontSize=6,
                     fillColor=GOLD if is_today else TEXT_SECONDARY))
        if i < 6:
            lx = x + r + 1
            rx = x + step - r - 1
            d.add(Line(lx, h/2, rx, h/2,
                       strokeColor=ACCENT if is_done else BORDER, strokeWidth=1))
    return d


def reintroduction_timeline():
    """Gantt-style chart showing when actives can be reintroduced."""
    w, h = IW, 115
    d = Drawing(w, h)
    d.add(Rect(0, 0, w, h, fillColor=ACCENT_LIGHT, strokeColor=BORDER, strokeWidth=0.5, rx=4))

    # Title
    d.add(String(10, h-14, "Active Reintroduction Timeline (weeks after starting reset)",
                 fontName="Helvetica-Bold", fontSize=8, fillColor=ACCENT))

    # Layout zones:
    #   title:      y=101-115
    #   week labels: y=86-100  (W1..W10 header row)
    #   grid+bars:  y=10-85
    total_weeks = 10
    gw = (w - 120) / total_weeks

    # Week labels in their own header row, well above bars
    for wk in range(total_weeks + 1):
        gx = 120 + wk * gw
        d.add(Line(gx, 10, gx, 85, strokeColor=BORDER, strokeWidth=0.4))
        if wk > 0:
            d.add(String(gx - 5, 88, f"W{wk}", fontName="Helvetica", fontSize=6,
                         fillColor=TEXT_SECONDARY))

    # Highlight reset zone (weeks 1-2)
    d.add(Rect(120, 10, gw*2, 75, fillColor=HexColor("#E0EDE6"), strokeColor=None))
    d.add(String(125, 13, "RESET", fontName="Helvetica-Bold", fontSize=6, fillColor=ACCENT))

    # Bars: (label, start_week, duration, color, note)
    # Rows are placed from y=78 downward, below week labels (y=88)
    actives = [
        ("Minimal Routine",  1, 10, ACCENT, "Continue always"),
        ("Niacinamide",      4,  6, SAGE,   "Week 4+"),
        ("Vitamin C",        7,  3, GOLD,   "Week 6-8"),
        ("Exf. Acids",       8,  2, HexColor("#C08040"), "Week 7-9"),
        ("Retinoids",        9,  1, RED_NO, "Week 8+ last"),
    ]
    bar_h = 8
    for row, (lbl, start, dur, col, note) in enumerate(actives):
        bx = 120 + (start - 1) * gw
        by = 78 - row * (bar_h + 5)   # row 0→78, row 1→65, row 2→52, row 3→39, row 4→26
        bw2 = dur * gw - 2
        d.add(Rect(bx, by, bw2, bar_h, fillColor=col, strokeColor=None, rx=2))
        d.add(String(8, by + 1, lbl, fontName="Helvetica", fontSize=7, fillColor=TEXT_PRIMARY))
        d.add(String(bx + 3, by + 1, note, fontName="Helvetica-Oblique", fontSize=6, fillColor=white))
    return d


def routine_flow_am():
    """AM routine visual step-flow diagram."""
    w, h = IW, 54
    d = Drawing(w, h)
    steps = ["Gentle\nCleanser", "Humectant\nSerum*", "Ceramide\nMoisturizer", "SPF 30+"]
    colors = [ACCENT, SAGE, HexColor("#1E4A2E"), HexColor("#B8935A")]
    bw2 = (w - 36) / 4
    for i, (lbl, col) in enumerate(zip(steps, colors)):
        x = i * (bw2 + 12)
        d.add(Rect(x, 8, bw2, 38, fillColor=col, strokeColor=None, rx=6))
        d.add(String(x + bw2/2 - 22, 28, lbl.split("\n")[0],
                     fontName="Helvetica-Bold", fontSize=8, fillColor=white))
        if "\n" in lbl:
            d.add(String(x + bw2/2 - 20, 18, lbl.split("\n")[1],
                         fontName="Helvetica", fontSize=7.5, fillColor=HexColor("#C8E0D0")))
        if i < 3:
            ax = x + bw2 + 3
            d.add(Line(ax, 27, ax + 9, 27, strokeColor=GOLD, strokeWidth=1.5))
            d.add(Polygon([ax+9, 27, ax+4, 30, ax+4, 24], fillColor=GOLD, strokeColor=None))
    return d


def routine_flow_pm():
    """PM routine visual step-flow diagram."""
    w, h = IW/2 - 6, 54
    d = Drawing(w, h)
    steps = ["Gentle\nCleanser", "Rich Ceramide\nMoisturizer"]
    colors = [ACCENT, HexColor("#1E4A2E")]
    bw2 = (w - 20) / 2
    for i, (lbl, col) in enumerate(zip(steps, colors)):
        x = i * (bw2 + 20)
        d.add(Rect(x, 8, bw2, 38, fillColor=col, strokeColor=None, rx=6))
        d.add(String(x + 6, 30, lbl.split("\n")[0],
                     fontName="Helvetica-Bold", fontSize=8, fillColor=white))
        d.add(String(x + 6, 20, lbl.split("\n")[1],
                     fontName="Helvetica", fontSize=7, fillColor=HexColor("#C8E0D0")))
        if i < 1:
            ax = x + bw2 + 2
            d.add(Line(ax, 27, ax + 16, 27, strokeColor=GOLD, strokeWidth=1.5))
            d.add(Polygon([ax+16, 27, ax+11, 30, ax+11, 24], fillColor=GOLD, strokeColor=None))
    return d


def progress_gauge():
    """Simple horizontal gauge showing skin status."""
    w, h = IW, 52
    d = Drawing(w, h)
    # Background track
    d.add(Rect(10, 30, w-20, 10, fillColor=BORDER, strokeColor=None, rx=5))
    # Progress fill (Day 5 = ~40% through recovery)
    d.add(Rect(10, 30, (w-20)*0.40, 10, fillColor=ACCENT, strokeColor=None, rx=5))
    # Pointer
    px = 10 + (w-20)*0.40
    d.add(Polygon([px, 42, px-5, 48, px+5, 48], fillColor=GOLD, strokeColor=None))
    # Labels
    d.add(String(10, 19, "Compromised", fontName="Helvetica", fontSize=7, fillColor=RED_NO))
    d.add(String(w/2-20, 19, "Improving", fontName="Helvetica-Bold", fontSize=7, fillColor=GOLD))
    d.add(String(w-55, 19, "Fully Restored", fontName="Helvetica", fontSize=7, fillColor=ACCENT))
    d.add(String(px-12, 12, "YOU ARE HERE", fontName="Helvetica-Bold", fontSize=6, fillColor=GOLD))
    return d


def ingredient_grid(items, color, bg_color, header):
    """Colored ingredient checklist cell content."""
    header_p = Paragraph(header, ParagraphStyle("ih",
        fontName="Helvetica-Bold", fontSize=10, leading=14,
        textColor=white, alignment=TA_CENTER))
    content = [header_p, Spacer(1, 5)]
    symbol = "+" if color == GREEN_OK else "x"
    sym_color = HexColor("#1A5C38") if color == GREEN_OK else HexColor("#9B2335")
    for item in items:
        p = Paragraph(
            f"<font color='#{('1A5C38' if color == GREEN_OK else '9B2335')}'>&#9679;</font>  {item}",
            ParagraphStyle("ii", fontName="Helvetica", fontSize=9, leading=15,
                           textColor=TEXT_PRIMARY, leftIndent=8, spaceAfter=2))
        content.append(p)
    return content


class SVGFlowable(Flowable):
    """Wrap a reportlab Drawing as a Flowable."""
    def __init__(self, drawing):
        super().__init__()
        self.drawing = drawing
        self.width = drawing.width
        self.height = drawing.height

    def wrap(self, availWidth, availHeight):
        return (self.width, self.height)

    def draw(self):
        renderPDF.draw(self.drawing, self.canv, 0, 0)


def dflo(drawing):
    return SVGFlowable(drawing)


def rule(color=BORDER, t=0.6, sb=4, sa=10):
    return HRFlowable(width="100%", thickness=t, color=color, spaceAfter=sa, spaceBefore=sb)


def callout_box(text, bg=ACCENT_LIGHT, border=ACCENT):
    data = [[Paragraph(text, ST["callout"])]]
    t = Table(data, colWidths=[IW])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), bg),
        ("LEFTPADDING",   (0,0),(-1,-1), 14),
        ("RIGHTPADDING",  (0,0),(-1,-1), 14),
        ("TOPPADDING",    (0,0),(-1,-1), 10),
        ("BOTTOMPADDING", (0,0),(-1,-1), 10),
        ("LINEBEFORE",   (0,0),(0,-1), 3, border),
    ]))
    return t


def why_block(text):
    items = [
        [Paragraph("WHY THIS MATTERS", ST["why_lbl"])],
        [Paragraph(text, ST["why_body"])],
    ]
    t = Table(items, colWidths=[IW])
    t.setStyle(TableStyle([
        ("LEFTPADDING",   (0,0),(-1,-1), 12),
        ("RIGHTPADDING",  (0,0),(-1,-1), 12),
        ("TOPPADDING",    (0,0),(-1,-1), 5),
        ("BOTTOMPADDING", (0,0),(-1,-1), 5),
        ("BACKGROUND",    (0,0),(-1,-1), BG),
        ("LINEBEFORE",   (0,0),(0,-1), 2.5, GOLD),
    ]))
    return t


# ── Pages ─────────────────────────────────────────────────────────────────────

def page_intro():
    s = []
    s.append(Spacer(1, 6*mm))
    s.append(Paragraph("INTRODUCTION", ST["eyebrow"]))
    s.append(rule(ACCENT, t=1.5))
    s.append(Paragraph("Why Your Skin Barrier Matters", ST["h1"]))
    s.append(Paragraph(
        "The skin barrier — the stratum corneum — is your body's primary interface with the world. "
        "Its function is elegantly simple: keep water in, keep irritants out. When compromised, "
        "the cascade is immediate: stinging, redness, tightness, breakouts, and hypersensitivity "
        "to products that never previously caused issues.",
        ST["body"]))

    # Skin barrier diagram — AI-generated illustration
    s.append(Spacer(1, 3*mm))
    s.append(Image("assets/skin-diagram.png", width=IW, height=IW * 0.72))
    s.append(Paragraph("Cross-section of the skin barrier layers. The stratum corneum's 'brick and mortar' structure — corneocytes embedded in a lipid matrix — is what barrier repair targets.", ST["caption"]))
    s.append(Spacer(1, 4*mm))

    s.append(Paragraph("The 3-Phase Reset Logic", ST["h2"]))
    s.append(dflo(three_phase_flow()))
    s.append(Spacer(1, 4*mm))

    s.append(Paragraph("Who This Protocol Is For", ST["h2"]))
    bullets = [
        "Skin that stings on application of regular products",
        "Persistent redness, tightness, or flaking despite moisturising",
        "Barrier damage from over-exfoliation with AHAs, BHAs, or physical scrubs",
        "Reactive skin worsening without an identifiable cause",
        "Post-procedure, eczema-adjacent, or rosacea-related reactivity",
    ]
    for b in bullets:
        s.append(Paragraph(f"\u2022  {b}", ST["bullet"]))

    s.append(rule(sb=8))
    s.append(Paragraph(
        "This protocol is evidence-based. It is not a substitute for dermatological care. "
        "If you are under active clinical management, share this guide with your clinician first.",
        ST["body_sm"]))
    return s


def page_day(n, title, subtitle, blocks):
    s = []
    s.append(Spacer(1, 5*mm))
    s.append(dflo(day_timeline(n)))
    s.append(rule(GOLD, t=1, sb=4, sa=8))
    s.append(Paragraph(f"DAY {n}", ST["day_n"]))
    s.append(Paragraph(title, ST["day_title"]))
    s.append(Paragraph(subtitle, ST["day_sub"]))
    s.append(rule(BORDER, t=0.5, sb=0, sa=8))
    for b in blocks:
        t = b["type"]
        if t == "body":
            s.append(Paragraph(b["text"], ST["body"]))
        elif t == "why":
            s.append(why_block(b["text"]))
        elif t == "callout":
            s.append(callout_box(b["text"]))
            s.append(Spacer(1, 2*mm))
        elif t == "step":
            s.append(Paragraph(b["label"], ST["step_lbl"]))
            s.append(Paragraph(b["text"], ST["step_body"]))
        elif t == "bullets":
            for item in b["items"]:
                s.append(Paragraph(f"\u2022  {item}", ST["bullet"]))
            s.append(Spacer(1, 2*mm))
        elif t == "note":
            s.append(Paragraph(b["text"], ST["note"]))
        elif t == "drawing":
            s.append(dflo(b["drawing"]))
            if "caption" in b:
                s.append(Paragraph(b["caption"], ST["caption"]))
            s.append(Spacer(1, 2*mm))
    return s


def page_ingredients():
    s = []
    s.append(Spacer(1, 5*mm))
    s.append(Paragraph("REFERENCE", ST["eyebrow"]))
    s.append(rule(ACCENT, t=1.5))
    s.append(Paragraph("Ingredients Cheat Sheet", ST["h1"]))
    s.append(Paragraph(
        "Audit every product in your routine against this list. "
        "During the reset your formulas must be rich in the green list and completely free of the red list.",
        ST["body"]))
    s.append(Spacer(1, 3*mm))

    green = ["Ceramide NP / AP / EOP", "Cholesterol", "Fatty acids (linoleic, palmitic, stearic)",
             "Niacinamide (5–10%)", "Panthenol (Vitamin B5)", "Centella asiatica / Madecassoside",
             "Allantoin", "Glycerin", "Hyaluronic acid / Sodium hyaluronate",
             "Squalane", "Colloidal oat (Avena sativa)"]
    red   = ["Fragrance / Parfum", "Denatured Alcohol (Alcohol Denat.)",
             "Sodium Lauryl Sulfate (SLS / SLES)", "Essential oils (lavender, tea tree, eucalyptus)",
             "AHA / BHA exfoliants — during reset", "Retinoids (retinol, tretinoin)",
             "Vitamin C (L-ascorbic acid) — during reset"]

    green_content = ingredient_grid(green, GREEN_OK, GREEN_LIGHT, "USE — Barrier-Friendly")
    red_content   = ingredient_grid(red,   RED_NO,   RED_LIGHT,   "AVOID — During the Reset")

    cw = (IW - 8) / 2
    grid = Table([[green_content, red_content]], colWidths=[cw, cw], spaceBefore=4)
    grid.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(0,0), GREEN_LIGHT),
        ("BACKGROUND",    (1,0),(1,0), RED_LIGHT),
        ("LEFTPADDING",   (0,0),(-1,-1), 12),
        ("RIGHTPADDING",  (0,0),(-1,-1), 12),
        ("TOPPADDING",    (0,0),(-1,-1), 12),
        ("BOTTOMPADDING", (0,0),(-1,-1), 12),
        ("VALIGN",        (0,0),(-1,-1), "TOP"),
        ("BOX",           (0,0),(0,0), 1, HexColor("#B0D4BC")),
        ("BOX",           (1,0),(1,0), 1, HexColor("#F0B0B0")),
    ]))
    s.append(grid)
    s.append(Spacer(1, 5*mm))

    # Side-by-side charts: ceramide ratio + TEWL
    charts = [[dflo(ceramide_pie()), dflo(tewl_bar_chart())]]
    ct = Table(charts, colWidths=[IW/2-4, IW/2-4])
    ct.setStyle(TableStyle([
        ("LEFTPADDING",   (0,0),(-1,-1), 0),
        ("RIGHTPADDING",  (0,0),(-1,-1), 4),
        ("TOPPADDING",    (0,0),(-1,-1), 0),
        ("BOTTOMPADDING", (0,0),(-1,-1), 0),
        ("VALIGN",        (0,0),(-1,-1), "MIDDLE"),
    ]))
    s.append(ct)
    s.append(Paragraph(
        "Left: The skin barrier lipid composition that your moisturizer should mirror. "
        "Right: TEWL rates showing the measurable impact of barrier compromise and early restoration.",
        ST["caption"]))
    s.append(Spacer(1, 3*mm))
    s.append(Paragraph(
        "Note: AHAs, BHAs, retinoids, and vitamin C are removed only during the reset. "
        "They are reintroduced systematically after barrier function is restored.",
        ST["body_sm"]))
    return s


def page_routine():
    s = []
    s.append(Spacer(1, 5*mm))
    s.append(Paragraph("REFERENCE", ST["eyebrow"]))
    s.append(rule(ACCENT, t=1.5))
    s.append(Paragraph("Your Daily Routine Template", ST["h1"]))
    s.append(Paragraph(
        "Follow this minimal structure exactly during the 7-day reset. "
        "No substitutions. No additions. Simplicity is the protocol.",
        ST["body"]))
    s.append(Spacer(1, 4*mm))

    # AM label
    am_header = [[Paragraph("MORNING ROUTINE", ST["tbl_head"])]]
    amt = Table(am_header, colWidths=[IW])
    amt.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1),ACCENT),
        ("LEFTPADDING",(0,0),(-1,-1),14),
        ("TOPPADDING",(0,0),(-1,-1),8),
        ("BOTTOMPADDING",(0,0),(-1,-1),8),
    ]))
    s.append(amt)
    s.append(dflo(routine_flow_am()))
    s.append(Paragraph("* Humectant serum optional — skip if skin is acutely reactive.", ST["caption"]))
    s.append(Spacer(1, 4*mm))

    # AM step table
    am_steps = [
        ("1", "Cleanse", "Fragrance-free, low-pH gel or cream cleanser. Lukewarm water, 30–60 sec. Pat dry."),
        ("2", "Humectant (opt.)", "Hyaluronic acid or glycerin serum on damp skin. Apply immediately after washing."),
        ("3", "Moisturize", "Ceramide-based cream: look for ceramide NP + AP + EOP, cholesterol, fatty acids."),
        ("4", "SPF 30+", "Mineral (zinc oxide) or hybrid SPF. Non-negotiable — UV radiation extends barrier damage."),
    ]
    pm_steps = [
        ("1", "Cleanse", "Same gentle cleanser. No double-cleanse during the reset."),
        ("2", "Moisturize", "Richer ceramide formula, sleeping mask, or a thin occlusive layer over your regular cream."),
    ]

    def step_rows(steps, bg1, bg2):
        rows = []
        for num, name, detail in steps:
            rows.append([
                Paragraph(f"<b>{num}</b>", ParagraphStyle("n", fontName="Helvetica-Bold",
                    fontSize=12, leading=16, textColor=ACCENT, alignment=TA_CENTER)),
                [Paragraph(f"<b>{name}</b>", ParagraphStyle("sn", fontName="Helvetica-Bold",
                    fontSize=9.5, leading=14, textColor=TEXT_PRIMARY)),
                 Paragraph(detail, ParagraphStyle("sd", fontName="Helvetica",
                    fontSize=8.5, leading=13, textColor=TEXT_SECONDARY))]
            ])
        t = Table(rows, colWidths=[28, IW-28])
        t.setStyle(TableStyle([
            ("LEFTPADDING",   (0,0),(-1,-1), 8),
            ("RIGHTPADDING",  (0,0),(-1,-1), 8),
            ("TOPPADDING",    (0,0),(-1,-1), 7),
            ("BOTTOMPADDING", (0,0),(-1,-1), 7),
            ("VALIGN",        (0,0),(-1,-1), "MIDDLE"),
            ("ROWBACKGROUNDS",(0,0),(-1,-1), [bg1, bg2]),
            ("LINEBELOW",     (0,0),(-1,-2), 0.5, BORDER),
            ("BOX",           (0,0),(-1,-1), 0.5, BORDER),
        ]))
        return t

    s.append(step_rows(am_steps, BG, SURFACE))
    s.append(Spacer(1, 5*mm))

    pm_header = [[Paragraph("EVENING ROUTINE", ST["tbl_head"])]]
    pmt = Table(pm_header, colWidths=[IW])
    pmt.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1),HexColor("#1E4A2E")),
        ("LEFTPADDING",(0,0),(-1,-1),14),
        ("TOPPADDING",(0,0),(-1,-1),8),
        ("BOTTOMPADDING",(0,0),(-1,-1),8),
    ]))
    s.append(pmt)
    s.append(step_rows(pm_steps, BG, SURFACE))
    s.append(Spacer(1, 4*mm))
    s.append(callout_box(
        "The damp-skin rule: Apply your moisturizer within 60 seconds of washing. "
        "Water evaporates rapidly from a compromised barrier — humectants and occlusives "
        "must be applied before this happens."
    ))
    return s


def page_next():
    s = []
    s.append(Spacer(1, 5*mm))
    s.append(Paragraph("AFTER THE RESET", ST["eyebrow"]))
    s.append(rule(ACCENT, t=1.5))
    s.append(Paragraph("What Comes Next", ST["h1"]))
    s.append(Paragraph(
        "The 7-day reset is the starting point, not the endpoint. "
        "Barrier repair is a 4–8 week biological process. The roadmap below shows what to do next.",
        ST["body"]))
    s.append(Spacer(1, 3*mm))

    # Reintroduction gantt
    s.append(dflo(reintroduction_timeline()))
    s.append(Paragraph(
        "Active reintroduction timeline. Each bar represents the earliest safe window — not a mandate. "
        "Always patch-test and observe for 2 weeks before adding the next active.",
        ST["caption"]))
    s.append(Spacer(1, 4*mm))

    timeline = [
        ("Weeks 2–4",  ACCENT,  "Continue the minimal routine. No additions. Assess skin weekly — less stinging, tightness, and flaking are the metrics. The barrier lipids regenerate invisibly."),
        ("Weeks 4–6",  SAGE,    "Introduce niacinamide (5–10%, fragrance-free). It stimulates ceramide synthesis and reduces TEWL. Patch-test first. Allow 2 weeks of observation."),
        ("Weeks 6–8",  GOLD,    "Reintroduce vitamin C, then exfoliating acids — one at a time, once weekly. Use the lowest available concentration. Buffer with ceramide moisturizer."),
        ("Week 8+",    RED_NO,  "Retinoids are last. Begin at the lowest strength, once weekly. Any return of stinging or redness means you moved too fast — step back one stage."),
    ]

    for period, col, body in timeline:
        row = [[
            Paragraph(f"<b>{period}</b>", ParagraphStyle("tp", fontName="Helvetica-Bold",
                fontSize=8.5, leading=13, textColor=white, alignment=TA_CENTER)),
            [Paragraph(body, ParagraphStyle("tb", fontName="Helvetica",
                fontSize=9, leading=14, textColor=TEXT_PRIMARY))]
        ]]
        t = Table(row, colWidths=[72, IW-72])
        t.setStyle(TableStyle([
            ("BACKGROUND",    (0,0),(0,0), col),
            ("BACKGROUND",    (1,0),(1,0), BG),
            ("LEFTPADDING",   (0,0),(-1,-1), 10),
            ("RIGHTPADDING",  (0,0),(-1,-1), 10),
            ("TOPPADDING",    (0,0),(-1,-1), 9),
            ("BOTTOMPADDING", (0,0),(-1,-1), 9),
            ("VALIGN",        (0,0),(-1,-1), "MIDDLE"),
            ("BOX",           (0,0),(-1,-1), 0.5, BORDER),
            ("LINEBELOW",     (0,0),(-1,-1), 0.5, BORDER),
        ]))
        s.append(t)
        s.append(Spacer(1, 2*mm))

    s.append(Spacer(1, 5*mm))
    s.append(Paragraph("Continue Reading at BioSkinRepair", ST["h2"]))
    links = [
        ("Skin Barrier 101", "bioskinrepair.com/skin-barrier-101",
         "The complete science of barrier repair — repair timelines, week-by-week expectations, clinical evidence."),
        ("Ingredients Guide", "bioskinrepair.com/ingredients",
         "Deep profiles of every barrier-repair ingredient: ceramides, niacinamide, peptides, and more."),
        ("Barrier Repair Routines", "bioskinrepair.com/routines",
         "Protocol templates for the minimal, standard, and condition-specific barrier routines."),
    ]
    for title, url, desc in links:
        row = [[
            [Paragraph(f"<b>{title}</b>", ParagraphStyle("lt", fontName="Helvetica-Bold",
                fontSize=9.5, leading=14, textColor=TEXT_PRIMARY, spaceAfter=2)),
             Paragraph(url, ParagraphStyle("lu", fontName="Helvetica",
                fontSize=8, leading=12, textColor=GOLD, spaceAfter=2)),
             Paragraph(desc, ParagraphStyle("ld", fontName="Helvetica",
                fontSize=8.5, leading=13, textColor=TEXT_SECONDARY))]
        ]]
        t = Table(row, colWidths=[IW])
        t.setStyle(TableStyle([
            ("BACKGROUND",    (0,0),(-1,-1), ACCENT_LIGHT),
            ("LEFTPADDING",   (0,0),(-1,-1), 14),
            ("RIGHTPADDING",  (0,0),(-1,-1), 14),
            ("TOPPADDING",    (0,0),(-1,-1), 10),
            ("BOTTOMPADDING", (0,0),(-1,-1), 10),
            ("BOX",           (0,0),(-1,-1), 0.5, BORDER),
            ("LINEBELOW",     (0,0),(-1,-1), 0.5, BORDER),
            ("LINEBEFORE",    (0,0),(0,-1), 3, ACCENT),
        ]))
        s.append(t)
        s.append(Spacer(1, 2*mm))
    return s


# ── Day data ──────────────────────────────────────────────────────────────────
DAYS = [
  { "n":1, "title":"The Reset", "subtitle":"Strip everything back to the three essentials.",
    "blocks":[
      {"type":"body","text":"Your only task today is to simplify. Remove every active — retinoids, vitamin C, exfoliating acids, scrubs, peels, enzyme treatments. Today is not about treating anything. Today is about stopping the ongoing damage so the repair can begin."},
      {"type":"step","label":"What to use today:","text":"Fragrance-free, low-pH gentle cleanser + ceramide-based moisturizer on damp skin + SPF (morning only). That is your entire routine."},
      {"type":"drawing","drawing":three_phase_flow(),"caption":"The three phases of barrier recovery. Phase 1 starts now."},
      {"type":"why","text":"Inflamed, compromised skin cannot efficiently absorb repair ingredients while actively defending against irritants. Every active you remove reduces the inflammatory load and creates space for recovery."},
      {"type":"callout","text":"Rule for Day 1: If a product has more than one active purpose (exfoliates, treats, brightens, anti-ages), set it aside. Keep only cleanser, moisturizer, and SPF."},
    ]},
  { "n":2, "title":"Assess and Eliminate", "subtitle":"Audit every product. Remove the hidden offenders.",
    "blocks":[
      {"type":"body","text":"Read the ingredient list of every product currently in your routine. You are looking for specific chemical classes — not brand names. The most common hidden irritants are not always obvious."},
      {"type":"step","label":"Remove anything containing:","text":"Fragrance / parfum — Denatured alcohol (Alcohol Denat.) — Sulfates (SLS, SLES) — Essential oils (lavender, rose, tea tree, eucalyptus) — Anything with pH above 6.5 (difficult to verify — remove if uncertain)."},
      {"type":"why","text":"Fragrance is the number-one cause of contact sensitisation in skincare. It is a legally protected 'trade secret' category that can contain hundreds of individual compounds, many of which are known allergens. Denatured alcohol disrupts barrier lipids directly and measurably increases TEWL."},
      {"type":"callout","text":"If you are unsure about a product, remove it. You can re-test it after the reset by patch-testing on your inner arm before reintroducing it to your face."},
    ]},
  { "n":3, "title":"Hydration Flooding", "subtitle":"Lock water into the skin before it escapes.",
    "blocks":[
      {"type":"body","text":"A compromised barrier loses water at dramatically higher rates than a healthy one. TEWL (transepidermal water loss) can be three times higher in damaged skin. Today you build a two-layer hydration system to counteract this."},
      {"type":"drawing","drawing":tewl_bar_chart(),"caption":"TEWL rates: healthy skin (8 g/m²/h) vs compromised barrier (24 g/m²/h) vs early recovery at Day 7 (14 g/m²/h). Source: Clinical TEWL benchmarks."},
      {"type":"step","label":"The damp-skin rule:","text":"Apply your moisturizer within 60 seconds of washing your face, while the skin is still damp. This is not optional during the reset — it is the most impactful timing adjustment you can make."},
      {"type":"step","label":"Add a humectant layer:","text":"Apply a few drops of hyaluronic acid serum or glycerin-rich essence to damp skin immediately after washing. Follow with your ceramide moisturizer within 60 seconds. The humectant draws water in; the moisturizer seals it there."},
      {"type":"why","text":"Humectants work by attracting and binding water molecules. Applied to damp skin, they have water nearby to pull in. Applied to dry, compromised skin, they can draw moisture up from deeper layers — the opposite of what you want."},
    ]},
  { "n":4, "title":"Barrier Lipid Replenishment", "subtitle":"Give your barrier the exact structural materials it needs.",
    "blocks":[
      {"type":"body","text":"The skin barrier is a precise lipid matrix. Its composition is approximately 50% ceramides, 25% cholesterol, and 15% fatty acids. This is not a detail — it is a formulation requirement. Your moisturizer should mirror this ratio."},
      {"type":"drawing","drawing":ceramide_pie(),"caption":"Optimal barrier lipid ratio. Moisturizers that replicate this composition — ceramides, cholesterol, fatty acids — provide the structural materials for barrier repair."},
      {"type":"step","label":"Check your moisturizer:","text":"Look for ceramide NP, ceramide AP, or ceramide EOP alongside cholesterol and a listed fatty acid (linoleic acid, palmitic acid, stearic acid). All three should appear in the first half of the ingredient list."},
      {"type":"step","label":"Upgrade your PM formula:","text":"For evenings, introduce a richer occlusive layer — a sleeping mask, thick ceramide balm, or a thin layer of petrolatum-based ointment applied over your regular moisturizer. Overnight is the barrier's primary repair window."},
      {"type":"why","text":"Ceramides are the structural mortar that prevents microscopic gaps in the barrier through which water escapes and irritants enter. You cannot rebuild the structure without supplying the raw materials."},
      {"type":"callout","text":"Products to look for: CeraVe Moisturizing Cream, La Roche-Posay Cicaplast Baume B5, or any formula that explicitly lists ceramide NP + cholesterol + fatty acids in the first half of its ingredient list."},
    ]},
  { "n":5, "title":"Inflammation Monitoring", "subtitle":"Assess progress. Troubleshoot if needed.",
    "blocks":[
      {"type":"body","text":"Day 5 is an assessment checkpoint. After four days on the minimal protocol, you should begin to notice measurable changes — even subtle ones. Barrier repair is not linear, and Day 5 does not always look dramatically different from Day 1."},
      {"type":"drawing","drawing":progress_gauge(),"caption":"Typical Day 5 position on the recovery spectrum. Stinging, redness, and tightness should be reducing — though not necessarily eliminated."},
      {"type":"step","label":"Signs the protocol is working:","text":"Products sting less on application. Redness or flushing is reduced or shorter-lasting. Skin feels less tight immediately after washing. Flaking or rough texture is beginning to soften."},
      {"type":"step","label":"If you see no improvement, check:","text":"Water temperature — must be lukewarm, not hot. Face towel — clean, changed every 2–3 days. Tap water quality — hard water with high mineral content is a common overlooked irritant. Consider rinsing with filtered water."},
      {"type":"why","text":"Inflammation is a biological cascade, not an on/off switch. Even after removing the trigger, the inflammatory response continues for days. No improvement on Day 5 typically means the trigger is still present, not that the protocol is failing."},
      {"type":"note","text":"Note: Active eczema flares, perioral dermatitis, and severe rosacea often require clinical intervention alongside any topical protocol. If your skin is actively worsening rather than plateauing, consult a dermatologist."},
    ]},
  { "n":6, "title":"Reinforce the Routine", "subtitle":"Build the consistency your barrier responds to.",
    "blocks":[
      {"type":"body","text":"By Day 6, your AM and PM routine should feel automatic. Execute both sessions perfectly today. This is the moment where the routine stops feeling like a restriction and starts feeling like a foundation."},
      {"type":"step","label":"Morning:","text":"Gentle cleanse → humectant serum on damp skin → ceramide moisturizer → SPF. No additions."},
      {"type":"step","label":"Evening:","text":"Gentle cleanse → richer ceramide formula or sleeping mask. No additions."},
      {"type":"step","label":"Optional patch-test (niacinamide):","text":"If you have a fragrance-free niacinamide serum and your skin has been calm for two consecutive days, apply a small amount to your inner arm today. Do not apply to your face. Observe for 24 hours."},
      {"type":"why","text":"The barrier rebuilds incrementally. Each day of the correct minimal routine adds structural repair. One deviation — a 'just this once' active or a foaming cleanser — can set the inflammation cascade back by 2–3 days. Boring consistency is the fastest path forward."},
      {"type":"callout","text":"Same products. Same order. Every day. That is the protocol."},
    ]},
  { "n":7, "title":"Evaluate and Plan Forward", "subtitle":"Assess where you are. Map what comes next.",
    "blocks":[
      {"type":"body","text":"You have completed the 7-day reset. Assess your skin against where it was on Day 1 across these specific markers:"},
      {"type":"bullets","items":[
          "Stinging on product application — has it reduced?",
          "Redness or flushing — is it less intense or shorter-lasting?",
          "Post-wash tightness — does skin feel more comfortable?",
          "Flaking or rough texture — is it softening?",
          "Overall reactivity — are you reacting to fewer things?",
      ]},
      {"type":"body","text":"Partial improvement across most markers is a meaningful result — it confirms the trajectory is correct. Continue the minimal routine for at least three more weeks before any additions."},
      {"type":"drawing","drawing":reintroduction_timeline(),"caption":"Your reintroduction roadmap from here. Patience in this phase is what prevents relapse."},
      {"type":"step","label":"Reintroduction order:","text":"Week 4: Niacinamide. Week 6: Vitamin C. Week 7–8: Exfoliating acids (once weekly, lowest concentration). Week 8+: Retinoids (last, always last)."},
      {"type":"why","text":"The most common cause of barrier repair relapse is reintroducing actives before the barrier has sufficiently restored. Each active must be tested in isolation for 2 weeks before adding the next. Your tolerance will increase as the barrier repairs."},
      {"type":"callout","text":"The reset is complete. The repair continues. Keep the foundation strong and reintroduce carefully."},
    ]},
]


# ── Build ─────────────────────────────────────────────────────────────────────

def build():
    OUT = "/Users/sherifelkady/Desktop/bioskinrepair-website/7-day-skin-barrier-reset-guide.pdf"
    MT, MB, ML, MR = 42*mm, 18*mm, 14*mm, 12*mm

    doc = BaseDocTemplate(OUT, pagesize=A4,
        leftMargin=ML, rightMargin=MR, topMargin=MT, bottomMargin=MB,
        title="The 7-Day Skin Barrier Reset Guide",
        author="BioSkinRepair", subject="Skin barrier repair protocol")

    cover_frame = Frame(0, 0, PAGE_W, PAGE_H, id="cover",
                        leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    inner_frame = Frame(ML, MB, PAGE_W-ML-MR, PAGE_H-MT-MB, id="inner",
                        leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    back_frame  = Frame(0, 0, PAGE_W, PAGE_H, id="back",
                        leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)

    doc.addPageTemplates([
        PageTemplate(id="COVER", frames=[cover_frame], onPage=cb_cover),
        PageTemplate(id="INNER", frames=[inner_frame], onPage=cb_inner),
        PageTemplate(id="BACK",  frames=[back_frame],  onPage=cb_back),
    ])

    story = []

    # Cover
    story.append(NextPageTemplate("COVER"))
    story.append(Spacer(1, PAGE_H))

    # Inner pages
    story.append(NextPageTemplate("INNER"))
    story.append(PageBreak())
    for el in page_intro(): story.append(el)

    for day in DAYS:
        story.append(PageBreak())
        for el in page_day(day["n"], day["title"], day["subtitle"], day["blocks"]):
            story.append(el)

    story.append(PageBreak())
    for el in page_ingredients(): story.append(el)

    story.append(PageBreak())
    for el in page_routine(): story.append(el)

    story.append(PageBreak())
    for el in page_next(): story.append(el)

    # Back cover
    story.append(NextPageTemplate("BACK"))
    story.append(PageBreak())
    story.append(Spacer(1, PAGE_H))

    doc.build(story)
    print(f"Done: {OUT}")


if __name__ == "__main__":
    build()
