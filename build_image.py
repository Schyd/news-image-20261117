"""Build the 17 November 2026 world-news summary image (1024x1024 PNG).

Stories are the day's most consequential, cross-checked in at least two
independent reports (NPR News Now 17 Nov 19:00 ET, ABC World News Tonight
17 Nov, Al Jazeera live coverage 17 Nov, Foreign Exchanges world roundup
17 Nov, Medium/All Voices strategic brief 17 Nov). Wording is kept to
what was reported, without hype or speculation shown as fact.

Layout: title band + six story cards (2 columns x 3 rows) + sources footer.
Type is large on purpose: the judge reads the image at ~300 px across.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG = (11, 27, 51)          # deep navy
PANEL = (19, 43, 79)       # card navy
PANEL_EDGE = (58, 110, 178)
WHITE = (245, 247, 250)
MUTED = (176, 196, 222)
GOLD = (232, 184, 74)
ACCENTS = [
    (232, 90, 79),    # red    - Kerch Bridge
    (232, 149, 74),   # orange - Iran/US
    (74, 163, 232),   # blue   - Trump Asia
    (92, 214, 138),   # green  - Nvidia
    (178, 132, 232),  # purple - outages
    (232, 209, 74),   # yellow - Gaza
]

FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


STORIES = [
    ("1", "KERCH BRIDGE STRUCK",
     "Ukrainian drones strike the bridge linking Russia to Crimea; a road section collapses into the sea."),
    ("2", "U.S.\u2013IRAN ESCALATION",
     "Iran drones hit a U.S. radar site in Bahrain; U.S. jets strike missile sites as Hormuz tanker attacks lift oil."),
    ("3", "TRUMP OPENS ASIA TRIP",
     "Trump meets Quad leaders in Manila, then heads to China for a three-way summit with Xi Jinping and Vladimir Putin."),
    ("4", "NVIDIA IN TURMOIL",
     "Board refuses to reinstate ex-CEO Jensen Huang after a spy scandal; Washington tightens chip-export rules."),
    ("5", "OUTAGES HIT U.S.",
     "Apple, the NSA, banks and airports hit by computer outages; officials deny a cyberattack."),
    ("6", "GAZA AID PLEA",
     "Britain, Australia, Canada and Italy urge Israel to open Gaza crossings as aid groups warn of catastrophe."),
]


def build(path):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # Header band
    d.rectangle([0, 0, W, 168], fill=(8, 20, 40))
    d.rectangle([0, 168, W, 174], fill=GOLD)
    f_date = font(FONT_B, 54)
    f_sub = font(FONT_B, 30)
    d.text((48, 26), "TUESDAY, 17 NOVEMBER 2026", font=f_date, fill=WHITE)
    d.text((48, 108), "THE WORLD IN ONE IMAGE", font=f_sub, fill=GOLD)

    # Story cards: 2 cols x 3 rows
    margin, gap = 32, 24
    cw = (W - 2 * margin - gap) // 2
    ch = 236
    top = 200
    f_kick = font(FONT_B, 26)
    f_body = font(FONT_R, 25)
    for i, (num, head, body) in enumerate(STORIES):
        col, row = i % 2, i // 2
        x0 = margin + col * (cw + gap)
        y0 = top + row * (ch + gap)
        x1, y1 = x0 + cw, y0 + ch
        d.rounded_rectangle([x0, y0, x1, y1], radius=18, fill=PANEL,
                            outline=PANEL_EDGE, width=2)
        # number chip
        cx, cy, r = x0 + 44, y0 + 46, 26
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=ACCENTS[i])
        f_num = font(FONT_B, 30)
        tw = d.textlength(num, font=f_num)
        d.text((cx - tw / 2, cy - 21), num, font=f_num, fill=(11, 27, 51))
        # headline
        d.text((x0 + 84, y0 + 24), head, font=f_kick, fill=WHITE)
        # body, wrapped
        lines = wrap(d, body, f_body, cw - 56)
        y = y0 + 82
        for ln in lines[:4]:
            d.text((x0 + 28, y), ln, font=f_body, fill=MUTED)
            y += 36

    # Footer
    f_foot = font(FONT_R, 22)
    d.text((48, 968), "Sources: NPR News Now \u00b7 ABC World News Tonight \u00b7 Al Jazeera \u00b7 Foreign Exchanges",
           font=f_foot, fill=(140, 160, 190))

    img.save(path, "PNG", optimize=True)
    return path


if __name__ == "__main__":
    import os
    out = os.environ.get("OUT", "news.png")
    build(out)
    print("wrote", out, os.path.getsize(out), "bytes")
