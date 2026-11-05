"""SAMPLE v2 for Kamel's approval (5 Nov 2026, not scheduled): photo-led, restrained, ON BRAND (red #e0263b, Plus Jakarta Sans, Outfit logo).
Ghosta Guest House (listing 37). Facts from api.weekendna.com 5 Nov 2026: 400 sqm, 800 m above sea, 180 deg view Beirut to Byblos, 25 min from Beirut,
5 bedrooms, 7 beds, 3 bathrooms, up to 12 guests, $220/night (about $18 each when 12 share), full kitchen, barbecue, parking.
Usage: export WK_WORK=$HOME/wk-work && python3 tools/examples/make_quiet_luxury_sample.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from brand import *

ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
OUT = os.path.join(ROOT, "posts", "2026-11-ghosta-quiet-luxury-sample"); os.makedirs(OUT, exist_ok=True)
P = lambda n: Image.open(f"{ROOT}/reels/public/photos/ghosta/37-{n}.webp").convert("RGB")
N = 5

def slide(i, photo, kicker, l1, l2, foot, cy=0.5):
    img = cover(photo, W, H, cy=cy)
    img = shade(img, 700, 225, 1.5)
    d = ImageDraw.Draw(img)
    logo(d, M, 60, WHITE, 40)
    pill(d, M, 905, kicker, jak(700, 22))
    d.text((M, 975), l1, font=jak(800, 76), fill=WHITE)
    d.text((M, 1065), l2, font=jak(800, 76), fill=WHITE)
    d.text((M, 1190), foot, font=jak(500, 27), fill=(235, 235, 235))
    dots(d, N, i)
    img.save(f"{OUT}/ghosta-{i+1}.jpg", quality=94)

slide(0, P("14"), "Found on Weekendna", "Above the bay,", "a warm weekend.", "Ghosta Guest House  ·  25 min from Beirut")
slide(1, P("19"), "800 m above the sea", "Evenings out here,", "high above the bay.", "Sea view  ·  mountain view  ·  180° to Byblos", cy=0.55)
slide(2, P("18"), "400 m² apartment", "Room to gather,", "slow evenings.", "Full kitchen  ·  barbecue  ·  free parking")
slide(3, P("34"), "7 beds  ·  3 bathrooms", "Five bedrooms,", "room for twelve.", "Heating  ·  air conditioning")

# 5: closing, brand red
img = Image.new("RGB", (W, H), RED); d = ImageDraw.Draw(img)
logo(d, M, 60, WHITE, 40, accent=WHITE)
img.paste(cover(P("26"), W - 2 * M, 520), (M, 160))
d.text((M, 735), "Save this for", font=jak(800, 76), fill=WHITE)
d.text((M, 825), "your next weekend.", font=jak(800, 76), fill=WHITE)
d.text((M, 960), "From $220 a night  ·  up to 12 guests", font=jak(700, 32), fill=WHITE)
d.text((M, 1010), "About $18 each when 12 share.", font=jak(500, 28), fill=(255, 225, 229))
d.text((M, 1080), "Request your dates on WhatsApp, nothing to pay yet.", font=jak(500, 26), fill=(255, 225, 229))
d.text((M, 1120), "weekendna.com  ·  link in bio", font=jak(500, 26), fill=(255, 225, 229))
button(d, 1200, "Follow @weekendna.lb", jak(800, 32), bg=WHITE, fg=RED)
dots(d, N, 4)
img.save(f"{OUT}/ghosta-5.jpg", quality=94)
