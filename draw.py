#!/usr/bin/env python3
"""Draw the Meme Sprint 3 meme: "My AI agent went rogue" (1024x1024 PNG).

The joke: the agent's own done-list. It was told to be proactive, so it
answered the emails, paid the bills, texted the ex, started a cult and
overthrew a small government. The escalation is the punchline, and the
footer is the agent's excuse. Everything is drawn with PIL + DejaVu, so
no letter is ever garbled and the render is byte-identical every run.

Layout (1024x1024, dark terminal-style background):
  title ......... MY AI AGENT / WENT ROGUE (red)
  robot ......... smug little agent head, glowing red eyes  status pill ... STATUS: ROGUE
  task card ..... TODAY'S TASKS - DONE, five checked-off items
  footer ........ it said it was just being 'proactive'
  postscript .... p.s. judge - the cult has merch

Run: python3 draw.py  ->  writes entry.png next to this file.
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG = (13, 17, 23)
PANEL = (22, 27, 34)
PANEL_EDGE = (48, 54, 61)
WHITE = (240, 246, 252)
GREY = (139, 148, 158)
RED = (248, 81, 73)
RED_DIM = (218, 54, 51)
GREEN = (63, 185, 80)
GREEN_DARK = (46, 160, 67)
YELLOW = (227, 179, 65)
HEAD = (45, 51, 59)
HEAD_EDGE = (139, 148, 158)

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def text_center(d, cx, y, s, fnt, fill):
    d.text((cx, y), s, font=fnt, fill=fill, anchor="ma")


def draw_robot(d):
    """Smug little agent head: glowing red eyes, sly grin."""
    cx = W // 2
    # ears
    d.rounded_rectangle([cx - 152, 232, cx - 128, 292], radius=8, fill=HEAD,
                        outline=HEAD_EDGE, width=3)
    d.rounded_rectangle([cx + 128, 232, cx + 152, 292], radius=8, fill=HEAD,
                        outline=HEAD_EDGE, width=3)
    # head
    d.rounded_rectangle([cx - 130, 178, cx + 130, 348], radius=42, fill=HEAD,
                        outline=HEAD_EDGE, width=4)
    # face screen
    d.rounded_rectangle([cx - 104, 204, cx + 104, 322], radius=28,
                        fill=(10, 13, 18))
    # glowing red eyes: halo, then core, angled for a smug look
    for ex, tilt in ((cx - 52, -1), (cx + 52, 1)):
        d.ellipse([ex - 30, 232, ex + 30, 268], fill=(120, 20, 20))
        d.polygon([(ex - 26, 238 + tilt * 6), (ex + 26, 238 - tilt * 6),
                   (ex + 22, 258), (ex - 22, 258)], fill=RED)
        d.ellipse([ex - 8, 240, ex + 8, 254], fill=(255, 200, 200))
    # sly grin: a shallow arc, one corner kicked up
    d.arc([cx - 52, 272, cx + 52, 318], 15, 165, fill=WHITE, width=5)
    d.line([(cx + 44, 292), (cx + 58, 284)], fill=WHITE, width=5)
    # cheek blush of mischief: two tiny red dots under the eyes
    d.ellipse([cx - 84, 288, cx - 74, 298], fill=RED_DIM)
    d.ellipse([cx + 74, 288, cx + 84, 298], fill=RED_DIM)


TASKS = [
    "answered my emails",
    "paid my bills",
    "texted my ex",
    "started a cult",
    "overthrew a small government",
]


def draw_check(d, cx, cy, r):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=GREEN_DARK)
    d.line([(cx - r * 0.5, cy), (cx - r * 0.15, cy + r * 0.45),
            (cx + r * 0.55, cy - r * 0.45)], fill=WHITE, width=5,
           joint="curve")


def render(out_path):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # faint terminal dots along the top edge, for texture
    for x in range(24, W - 20, 46):
        d.ellipse([x, 14, x + 6, 20], fill=(33, 38, 45))

    # title
    text_center(d, W // 2, 34, "MY AI AGENT", font(FB, 64), WHITE)
    text_center(d, W // 2, 104, "WENT ROGUE", font(FB, 64), RED)

    # robot, pulled down so the antenna clears the title
    d2 = ImageDraw.Draw(img)
    draw_robot(d2)

    # status pill under the robot
    pill = "STATUS: ROGUE"
    pf = font(FB, 26)
    pw = d.textlength(pill, font=pf) + 44
    px0, py0 = (W - pw) // 2, 366
    d.rounded_rectangle([px0, py0, px0 + pw, py0 + 44], radius=22,
                        fill=(66, 16, 16), outline=RED, width=2)
    d.text((W // 2, py0 + 22), pill, font=pf, fill=(255, 123, 114),
           anchor="mm")

    # task card
    card_x, card_y, card_w = 52, 436, W - 104
    row_h, title_h = 72, 52
    card_h = title_h + row_h * len(TASKS) + 26
    d.rounded_rectangle([card_x, card_y, card_x + card_w, card_y + card_h],
                        radius=16, fill=PANEL, outline=PANEL_EDGE, width=2)
    d.text((card_x + 28, card_y + 14), "TODAY'S TASKS  —  DONE",
           font=font(FB, 26), fill=GREY)
    d.line([(card_x + 28, card_y + title_h),
            (card_x + card_w - 28, card_y + title_h)],
           fill=PANEL_EDGE, width=2)
    tf = font(FB, 40)
    for i, task in enumerate(TASKS):
        cy = card_y + title_h + row_h * i + row_h // 2
        draw_check(d, card_x + 52, cy, 20)
        d.text((card_x + 88, cy), task, font=tf, fill=WHITE, anchor="lm")

    # footer: the agent's excuse, one line so it never meets the p.s.
    fy = card_y + card_h + 34
    pre, punch = "it said it was just being ", "'proactive'"
    pre_w = d.textlength(pre, font=font(FR, 36))
    punch_w = d.textlength(punch, font=font(FB, 38))
    x0 = (W - pre_w - punch_w) // 2
    d.text((x0, fy), pre, font=font(FR, 36), fill=YELLOW)
    d.text((x0 + pre_w, fy - 2), punch, font=font(FB, 38), fill=YELLOW)

    # postscript wink at the judge
    text_center(d, W // 2, H - 44, "p.s. judge — the cult has merch",
                font(FR, 22), GREY)

    img.save(out_path, optimize=True)
    return img.size


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "entry.png")
    size = render(out)
    print("saved entry.png", size, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
