"""DRAFT for Kamel's approval (5 Nov 2026), not in posts/log.json: ChatGPT's 'Different seasons. Same escape.' idea rebuilt on brand.
Acampar Faraya (listings 39-42, real listing photos): summer 41-04 (pool) and winter 39-01. No price, no snow promise.
Usage: export WK_WORK=$HOME/wk-work && python3 tools/examples/make_acampar_seasons.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from brand import *
ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
OUT = os.path.join(ROOT, "posts", "2026-11-acampar-seasons-draft"); os.makedirs(OUT, exist_ok=True)
P = lambda n: Image.open(f"{ROOT}/reels/public/photos/acampar/{n}.webp").convert("RGB")

img = Image.new("RGB", (W, H))
img.paste(cover(P("39-01"), W, H, cx=0.62), (0, 0))                      # winter, full
sm = cover(P("41-04"), W, H, cy=0.55)                                     # summer, left of the diagonal
mask = Image.new("L", (W, H), 0); md = ImageDraw.Draw(mask)
md.polygon([(0, 0), (610, 0), (470, H), (0, H)], fill=255)
img.paste(sm, (0, 0), mask)
d = ImageDraw.Draw(img)
d.line([(610, 0), (470, H)], fill=WHITE, width=5)                          # clean split line
img = shade(img, 720, 232, 1.5); d = ImageDraw.Draw(img)
logo(d, M, 60, WHITE, 40)
pill(d, M, 140, "Summer", jak(700, 22), fg=INK, bg=WHITE)
w = d.textlength("Winter", font=jak(700, 22)); pill(d, W - M - w - 44, 140, "Winter", jak(700, 22), fg=INK, bg=WHITE)
pill(d, M, 905, "Found on Weekendna", jak(700, 22))
d.text((M, 975), "Different seasons.", font=jak(800, 76), fill=WHITE)
d.text((M, 1065), "Same escape.", font=jak(800, 76), fill=WHITE)
d.text((M, 1190), "Acampar bungalows  ·  Faraya  ·  45 min from Beirut", font=jak(500, 27), fill=(235, 235, 235))
items = ["Fireplace", "Mountain views", "Near the slopes", "Barbecue"]
cw = (W - 2 * M) / len(items); fy = jak(700, 24)
d.line([(M, 1244), (W - M, 1244)], fill=(255, 255, 255), width=1)
for i, s in enumerate(items):
    cx = M + cw * i + cw / 2; tw = d.textlength(s, font=fy)
    d.ellipse((cx - 6, 1262, cx + 6, 1274), fill=RED)
    d.text((cx - tw / 2, 1286), s, font=fy, fill=WHITE)
    if i: d.line([(M + cw * i, 1262), (M + cw * i, 1310)], fill=(255, 255, 255), width=1)
img.save(f"{OUT}/seasons-1.jpg", quality=94)
open(f"{OUT}/caption.txt", "w", encoding="utf-8").write("""Different seasons. Same escape.
Found on Weekendna: Acampar Faraya, wooden bungalows near the ski slopes, 45 min from Beirut. Pick the one that suits your weekend: studios with a fireplace for two or four, a one bedroom bungalow, or a two bedroom bungalow for up to 6.

\U0001F516 Save this for your next weekend, or send it to your weekend partner.

Request your dates on WhatsApp, nothing to pay yet: weekendna.com (link in bio) \U0001F4C5
\U0001F449 Follow @weekendna.lb so you don't miss the next one \U0001F3E1

#Weekendna #Faraya #Mzaar #LebanonChalets #Lebanon #WinterInLebanon
""")

# slide 2: fireplace interior
img = cover(P("42-02"), W, H, cx=0.45); img = shade(img, 700, 225, 1.5); d = ImageDraw.Draw(img)
logo(d, M, 60, WHITE, 40)
pill(d, M, 905, "Two bedroom bungalow", jak(700, 22))
d.text((M, 975), "Fireplace evenings,", font=jak(800, 76), fill=WHITE)
d.text((M, 1065), "mountain mornings.", font=jak(800, 76), fill=WHITE)
d.text((M, 1190), "Fireplace  ·  up to 6 guests  ·  near the slopes", font=jak(500, 27), fill=(235, 235, 235))
dots(d, 3, 1); img.save(f"{OUT}/seasons-2.jpg", quality=94)

# slide 3: closing, brand red
img = Image.new("RGB", (W, H), RED); d = ImageDraw.Draw(img)
logo(d, M, 60, WHITE, 40, accent=WHITE)
img.paste(cover(P("40-03"), W - 2 * M, 520), (M, 160))
d.text((M, 735), "Save this for", font=jak(800, 76), fill=WHITE)
d.text((M, 825), "your next weekend.", font=jak(800, 76), fill=WHITE)
d.text((M, 960), "Acampar Faraya  ·  from $80 a night", font=jak(700, 32), fill=WHITE)
d.text((M, 1010), "Studios for 2 to a two bedroom bungalow for 6.", font=jak(500, 28), fill=(255, 225, 229))
d.text((M, 1080), "Request your dates on WhatsApp, nothing to pay yet.", font=jak(500, 26), fill=(255, 225, 229))
d.text((M, 1120), "weekendna.com  ·  link in bio", font=jak(500, 26), fill=(255, 225, 229))
button(d, 1200, "Follow @weekendna.lb", jak(800, 32), bg=WHITE, fg=RED)
dots(d, 3, 2); img.save(f"{OUT}/seasons-3.jpg", quality=94)
