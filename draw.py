#!/usr/bin/env python3
"""Draw entry.png for make.fun bounty news-image-20261126.

"THE WORLD TODAY - Thursday 26 November 2026": one newspaper-style
front page summing up the day's world news in 35 stories across
7 regions, led by the Houthi strike on Saudi Arabia's Ras Tanura
refinery. Pure Python + Pillow, no network, deterministic output.

Run:  python3 draw.py        (writes entry.png next to this file)
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 24

PAPER = (248, 244, 233)
INK = (20, 20, 20)
MUTED = (90, 86, 76)
RULE = (185, 28, 28)
NAVY = (20, 38, 63)
NAVY_LIGHT = (34, 58, 92)
ORANGE = (234, 88, 12)
SMOKE = (120, 116, 108)

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")
SERIF_BOLD = str(FONT_DIR / "DejaVuSerif-Bold.ttf")
SANS_BOLD = str(FONT_DIR / "DejaVuSans-Bold.ttf")
SANS = str(FONT_DIR / "DejaVuSans.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


# ---------------------------------------------------------------- stories
# (headline, detail) -- 35 stories, 5 per region, 7 regions.
SECTIONS = [
    ("MIDDLE EAST", (124, 45, 18), [
        ("Houthis hit Ras Tanura refinery",
         "550,000 bpd plant; smoke over 600 sq km, oil jumps 2%"),
        ("Saudi defences down 4 drones",
         "Houthi projectile hits Jazan port; minor damage reported"),
        ("Riyadh tower struck, 2 Indians hurt",
         "India condemns KAFD attack; Houthis claim second strike"),
        ("Saudi strikes leave dead in Yemen",
         "Deaths and missing reported after Hodeidah raids"),
        ("Lebanon to open second airport",
         "New northern gateway signals Hezbollah's fading sway"),
    ]),
    ("EUROPE & UKRAINE", (30, 64, 175), [
        ("Ukraine hits Savasleyka air base",
         "Five Russian jets damaged: 3 MiG-31s, 2 Su-34s"),
        ("Dozens of states urge Russia",
         "Halt alleged riot-agent use in Ukraine war, they demand"),
        ("Russia's own toll: ~500,000 dead",
         "Moscow's figures show scale of Ukraine war losses"),
        ("Murmansk governor detained",
         "Regional chief held 2 months in corruption probe"),
        ("US shelves Russia business deals",
         "Trade incentives to end Ukraine war dropped - FT"),
    ]),
    ("ASIA-PACIFIC", (22, 101, 52), [
        ("Kim orders wider nuclear rollout",
         "North Korea to deploy more tactical nuclear weapons"),
        ("Pyongyang expels Swiss office",
         "North Korea orders Switzerland to close mission"),
        ("Pakistan's first astronaut flies",
         "Muhammad Zeeshan Ali joins China's Shenzhou-24 crew"),
        ("Xi's graft probe shakes Shanghai",
         "Rising star's fall upends China's path to power"),
        ("India pledges Rs 15,000 cr to Nepal",
         "Modi-Shah talks hail 'historic' visit to New Delhi"),
    ]),
    ("AMERICAS", (126, 34, 206), [
        ("US unveils tariffs on 14 partners",
         "New levies target factory overcapacity; China hit hardest"),
        ("Birthright order blocked again",
         "Second judge halts Trump's citizenship curbs"),
        ("Trump pardons two turkeys",
         "Freedom and Feathers spared for Thanksgiving"),
        ("20 hostages freed in Colombia",
         "Police storm supermarket after 17-hour siege"),
        ("Plane lost off Mississippi coast",
         "Crews search Gulf for six aboard small aircraft"),
    ]),
    ("AFRICA", (146, 64, 14), [
        ("Sudan drone strikes kill 19",
         "RSF attacks hit Blue Nile state; 20 more wounded"),
        ("Kenyan cult leader convicted",
         "New charges stick for preacher on 200-year term"),
        ("Cairo tanker crash kills 30",
         "Fuel tanker fire engulfs highway outside capital"),
        ("Ramaphosa wins Farmgate ruling",
         "Court sets aside Phala Phala report in South Africa"),
        ("Kenya, DR Congo restore ties",
         "Full diplomatic relations agreed after years of tension"),
    ]),
    ("MARKETS & TECH", (15, 118, 110), [
        ("Brent crude tops $93 a barrel",
         "Oil jumps 2%+ on Ras Tanura attack claim"),
        ("US tech slides before holiday",
         "Nasdaq -1.8%; Nvidia sinks 6% into Thanksgiving"),
        ("S&P warns on Nvidia's board",
         "Rating on downgrade watch as Huang returns as CEO"),
        ("SpaceX cleared for 1m satellites",
         "FCC approves giant orbital data-centre network"),
        ("US core inflation hits 3.3%",
         "Bitcoin falls to $58,224 as rate-hike odds rise"),
    ]),
    ("SPORT, SCIENCE & CULTURE", (190, 24, 93), [
        ("Duran Duran's Andy Taylor dies",
         "Guitarist and songwriter was 65"),
        ("BepiColombo reaches Mercury",
         "Probe enters orbit after an eight-year journey"),
        ("Gukesh draws World Chess Game 2",
         "20-move draw with Sindarov in London System"),
        ("1,220 players enter IPL auction",
         "Registrations flood in for 2027 season"),
        ("New Zealand hold India to draw",
         "Dogged batting saves first Test in India"),
    ]),
]

NUMBERS = [
    ("$93.60", "Brent crude a barrel, up 2.4% on the day"),
    ("550,000", "barrels a day: Ras Tanura refinery capacity"),
    ("5", "Russian jets damaged in the Savasleyka strike"),
    ("1,220", "players registered for the IPL 2027 auction"),
]


def fit_text(draw, text, fnt, max_w):
    """Shorten text with an ellipsis until it fits max_w."""
    if draw.textlength(text, font=fnt) <= max_w:
        return text
    while text and draw.textlength(text + "...", font=fnt) > max_w:
        text = text[:-1]
    return text + "..."


def draw_refinery(draw, x0, y0, x1, y1):
    """Flat stylised refinery with flare flame and smoke, inside a box."""
    draw.rectangle([x0, y0, x1, y1], fill=NAVY_LIGHT)
    # ground
    gy = y1 - 26
    draw.rectangle([x0, gy, x1, y1], fill=(12, 24, 44))
    # distillation towers
    for tx, tw, th in ((x0 + 18, 26, 78), (x0 + 52, 20, 96),
                       (x0 + 80, 24, 66)):
        draw.rectangle([tx, gy - th, tx + tw, gy], fill=(148, 163, 184))
        draw.rectangle([tx - 3, gy - th - 6, tx + tw + 3, gy - th],
                       fill=(203, 213, 225))
    # flare stack with flame (kept inside the box: stack 84 tall,
    # flame tip at gy-112, box top is gy-118)
    fx = x0 + 128
    draw.rectangle([fx, gy - 84, fx + 10, gy], fill=(100, 116, 139))
    flame = [(fx - 8, gy - 84), (fx + 5, gy - 112),
             (fx + 18, gy - 84), (fx + 12, gy - 74), (fx + 5, gy - 80)]
    draw.polygon(flame, fill=ORANGE)
    draw.ellipse([fx - 2, gy - 102, fx + 22, gy - 82], fill=(250, 204, 21))
    # smoke drifting up-right
    for cx, cy, r in ((x0 + 150, y0 + 34, 16), (x0 + 168, y0 + 22, 20),
                      (x0 + 190, y0 + 12, 14)):
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=SMOKE)
    # windows on the towers
    for tx, tw, th in ((x0 + 18, 26, 78), (x0 + 52, 20, 96),
                       (x0 + 80, 24, 66)):
        for wy in range(gy - th + 10, gy - 8, 14):
            draw.rectangle([tx + 5, wy, tx + tw - 5, wy + 5],
                           fill=(250, 204, 21))


def draw_section(draw, x, y, w, h, name, color, stories, lead_tag=False):
    """One region block: coloured header bar + 5 two-line stories."""
    head_h = 23
    draw.rectangle([x, y, x + w, y + head_h], fill=color)
    f_head = font(SANS_BOLD, 14)
    draw.text((x + 8, y + 4), name, font=f_head, fill=(255, 255, 255))
    count = draw.textlength("5 STORIES", font=f_head)
    draw.text((x + w - count - 8, y + 4), "5 STORIES",
              font=f_head, fill=(255, 255, 255))
    f_h = font(SANS_BOLD, 14)
    f_d = font(SANS, 12)
    slot = (h - head_h) / 5.0
    for i, (headline, detail) in enumerate(stories):
        sy = y + head_h + i * slot
        hy = sy + 2
        dy = sy + 17
        draw.text((x + 2, hy), f"{i + 1}.", font=f_h, fill=color)
        hx = x + 24
        max_w = w - 26
        if lead_tag and i == 0:
            tag = "LEAD"
            tw = draw.textlength(tag, font=font(SANS_BOLD, 10)) + 8
            draw.rounded_rectangle([hx, hy + 1, hx + tw, hy + 14],
                                   radius=3, fill=RULE)
            draw.text((hx + 4, hy + 2), tag,
                      font=font(SANS_BOLD, 10), fill=(255, 255, 255))
            hx += tw + 6
            max_w -= tw + 6
        draw.text((hx, hy), fit_text(draw, headline, f_h, max_w),
                  font=f_h, fill=INK)
        draw.text((x + 24, dy), fit_text(draw, detail, f_d, w - 26),
                  font=f_d, fill=MUTED)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    # outer frame
    draw.rectangle([6, 6, W - 7, H - 7], outline=INK, width=2)

    # ---- masthead ----
    y = MARGIN
    title_f = font(SERIF_BOLD, 56)
    title = "THE WORLD TODAY"
    tw = draw.textlength(title, font=title_f)
    draw.text(((W - tw) / 2, y), title, font=title_f, fill=INK)
    y += 66
    date_f = font(SANS_BOLD, 15)
    date_line = "THURSDAY 26 NOVEMBER 2026"
    dw = draw.textlength(date_line, font=date_f)
    draw.text(((W - dw) / 2, y), date_line, font=date_f, fill=RULE)
    y += 24
    sub_f = font(SANS, 12)
    sub = "35 STORIES  ·  7 REGIONS  ·  THANKSGIVING DAY IN THE UNITED STATES"
    sw = draw.textlength(sub, font=sub_f)
    draw.text(((W - sw) / 2, y), sub, font=sub_f, fill=MUTED)
    y += 22
    draw.line([MARGIN, y, W - MARGIN, y], fill=RULE, width=3)
    y += 10

    # ---- lead banner ----
    lead_y = y
    lead_h = 164
    draw.rectangle([MARGIN, lead_y, W - MARGIN, lead_y + lead_h], fill=NAVY)
    pic_w = 216
    draw_refinery(draw, MARGIN + 10, lead_y + 10,
                  MARGIN + 10 + pic_w, lead_y + lead_h - 10)
    tx = MARGIN + 10 + pic_w + 16
    tw_max = W - MARGIN - tx - 12
    kick_f = font(SANS_BOLD, 13)
    draw.text((tx, lead_y + 12), "LEAD STORY  —  MIDDLE EAST",
              font=kick_f, fill=(250, 204, 21))
    head_f = font(SANS_BOLD, 40)
    headline = fit_text(draw, "HOUTHIS STRIKE RAS TANURA", head_f, tw_max)
    draw.text((tx, lead_y + 34), headline, font=head_f, fill=(255, 255, 255))
    sub_f2 = font(SANS, 15)
    line1 = "Yemen's Houthis say they struck Saudi Arabia's largest"
    line2 = "refinery, starting fires. Satellite images show thick"
    line3 = "black smoke — and Brent crude jumps past $93 a barrel."
    for j, line in enumerate((line1, line2, line3)):
        draw.text((tx, lead_y + 88 + j * 21), line, font=sub_f2,
                  fill=(226, 232, 240))
    y = lead_y + lead_h + 10

    # ---- two columns of region sections ----
    cols_y = y
    cols_h = H - MARGIN - 22 - cols_y
    gap = 20
    col_w = (W - 2 * MARGIN - gap) // 2
    left_x = MARGIN
    right_x = MARGIN + col_w + gap
    sec_h = cols_h / 4.0
    for i, (name, color, stories) in enumerate(SECTIONS[:4]):
        draw_section(draw, left_x, cols_y + i * sec_h, col_w, sec_h,
                     name, color, stories, lead_tag=(i == 0))
    for i, (name, color, stories) in enumerate(SECTIONS[4:7]):
        draw_section(draw, right_x, cols_y + i * sec_h, col_w, sec_h,
                     name, color, stories)

    # ---- numbers box, bottom of the right column ----
    bx, by = right_x, cols_y + 3 * sec_h
    bh = cols_h - 3 * sec_h
    draw.rectangle([bx, by, bx + col_w, by + bh], outline=INK, width=1)
    draw.rectangle([bx, by, bx + col_w, by + 23], fill=INK)
    nf = font(SANS_BOLD, 14)
    draw.text((bx + 8, by + 4), "THE DAY IN NUMBERS", font=nf,
              fill=(255, 255, 255))
    num_f = font(SANS_BOLD, 21)
    lab_f = font(SANS, 12)
    slot = (bh - 23) / 4.0
    for i, (num, label) in enumerate(NUMBERS):
        ny = by + 23 + i * slot
        draw.text((bx + 10, ny + 6), num, font=num_f, fill=RULE)
        nw = draw.textlength(num, font=num_f)
        draw.text((bx + 16 + nw, ny + 11),
                  fit_text(draw, label, lab_f, col_w - 26 - nw),
                  font=lab_f, fill=INK)

    # ---- footer ----
    fy = H - MARGIN - 16
    foot_f = font(SANS, 11)
    foot = ("Sources: Reuters, AP, AFP, BBC, Al-Monitor and others  ·  "
            "Stories as reported on 26 Nov 2026  ·  Drawn for make.fun "
            "bounty news-image-20261126")
    fw = draw.textlength(foot, font=foot_f)
    draw.text(((W - fw) / 2, fy), foot, font=foot_f, fill=MUTED)

    out = Path(__file__).resolve().parent / "entry.png"
    img.save(out, format="PNG")
    print(f"wrote {out} ({out.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
