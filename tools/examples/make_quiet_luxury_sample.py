"""SAMPLE for Kamel's approval (5 Nov 2026, not scheduled): the quiet-luxury look asked for in MARKETING_DIRECTION.md (Six Senses as inspiration only).
Ghosta Guest House (listing 37), 5-slide 4:5 carousel on real listing photos. Ivory ground, one thin serif, tracked small caps, no badge, no logo intro, no animation.
Photos: reels/public/photos/ghosta (python3 tools/reel_prep.py photos reels/public/photos/ghosta 37). Facts (api.weekendna.com, 5 Nov 2026): 400 sqm apartment, 800 m above sea level,
180 degree view Beirut to Byblos, 25 min from Beirut, 5 bedrooms, 7 beds, 3 bathrooms, up to 12 guests, $220/night (about $18 each when 12 share), heating, full kitchen, barbecue, parking.
Usage: source tools/setup.sh && python3 tools/examples/make_quiet_luxury_sample.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from brand import *

ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
OUT = os.path.join(ROOT, "posts", "2026-11-ghosta-quiet-luxury-sample"); os.makedirs(OUT, exist_ok=True)
P = lambda n: Image.open(f"{ROOT}/reels/public/photos/ghosta/37-{n}.webp").convert("RGB")
IVORY = (245, 240, 232); INK = (38, 33, 30); MUTED = (122, 113, 104); LINE = (214, 205, 193)
CF = os.path.join(F, "fontsource-cormorant-garamond-5.2.5", "files")
def serif(w, s, it=False): return ImageFont.truetype(f"{CF}/cormorant-garamond-latin-{w}-{'italic' if it else 'normal'}.woff", s, layout_engine=L)
MX = 72

def tracked(d, x, y, text, font, fill, track=5, anchor="l"):
    w = sum(d.textlength(c, font=font) + track for c in text) - track
    if anchor == "c": x = (W - w) / 2
    for c in text:
        d.text((x, y), c, font=font, fill=fill); x += d.textlength(c, font=font) + track
    return w

def frame(photo, box):
    x0, y0, x1, y1 = box
    return cover(photo, x1 - x0, y1 - y0)

def base():
    img = Image.new("RGB", (W, H), IVORY); d = ImageDraw.Draw(img)
    logo(d, MX, 62, color=INK, size=34)
    return img, d

def put(img, photo, box, cx=0.5, cy=0.5):
    x0, y0, x1, y1 = box
    img.paste(cover(photo, x1 - x0, y1 - y0, cx=cx, cy=cy), (x0, y0))

small = jak(500, 21)

# 1. Cover
img, d = base()
put(img, P("14"), (MX, 150, W - MX, 910))
tracked(d, MX, 962, "FOUND ON WEEKENDNA", small, MUTED, 6)
d.text((MX, 1000), "Above the bay,", font=serif(300, 104), fill=INK)
d.text((MX, 1108), "a warm weekend.", font=serif(300, 104, True), fill=INK)
d.line((MX, 1262, W - MX, 1262), fill=LINE, width=2)
tracked(d, MX, 1284, "GHOSTA  ·  25 MIN FROM BEIRUT", small, MUTED, 5)
img.save(f"{OUT}/ghosta-1.jpg", quality=94)

# 2. The view
img, d = base()
put(img, P("19"), (MX, 150, W - MX, 910), cy=0.55)
tracked(d, MX, 962, "800 M ABOVE THE SEA", small, MUTED, 6)
d.text((MX, 1000), "Evenings out here,", font=serif(300, 104), fill=INK)
d.text((MX, 1108), "high above the bay.", font=serif(300, 104, True), fill=INK)
d.line((MX, 1262, W - MX, 1262), fill=LINE, width=2)
tracked(d, MX, 1284, "SEA VIEW  ·  MOUNTAIN VIEW", small, MUTED, 5)
img.save(f"{OUT}/ghosta-2.jpg", quality=94)

# 3. The space
img, d = base()
put(img, P("18"), (MX, 150, W - MX, 910))
tracked(d, MX, 962, "400 SQUARE METRES", small, MUTED, 6)
d.text((MX, 1000), "Room to gather,", font=serif(300, 104), fill=INK)
d.text((MX, 1108), "slow evenings.", font=serif(300, 104, True), fill=INK)
d.line((MX, 1262, W - MX, 1262), fill=LINE, width=2)
tracked(d, MX, 1284, "FULL KITCHEN  ·  BARBECUE  ·  FREE PARKING", small, MUTED, 5)
img.save(f"{OUT}/ghosta-3.jpg", quality=94)

# 4. The rooms
img, d = base()
put(img, P("34"), (MX, 150, W - MX, 910))
tracked(d, MX, 962, "7 BEDS  ·  3 BATHROOMS", small, MUTED, 6)
d.text((MX, 1000), "Five bedrooms,", font=serif(300, 104), fill=INK)
d.text((MX, 1108), "room for twelve.", font=serif(300, 104, True), fill=INK)
d.line((MX, 1262, W - MX, 1262), fill=LINE, width=2)
tracked(d, MX, 1284, "HEATING  ·  AIR CONDITIONING", small, MUTED, 5)
img.save(f"{OUT}/ghosta-4.jpg", quality=94)

# 5. Save + details
img, d = base()
put(img, P("26"), (MX, 150, W - MX, 690))
d.text((MX, 740), "Save this for", font=serif(300, 96), fill=INK)
d.text((MX, 836), "your next weekend.", font=serif(300, 96, True), fill=INK)
d.line((MX, 972, W - MX, 972), fill=LINE, width=2)
tracked(d, MX, 1000, "FROM $220 A NIGHT  ·  UP TO 12 GUESTS", jak(600, 24), INK, 4)
d.text((MX, 1048), "About $18 each when 12 share.", font=jak(400, 28), fill=MUTED)
d.text((MX, 1130), "Request your dates on WhatsApp, nothing to pay yet.", font=jak(400, 25), fill=MUTED)
d.text((MX, 1170), "weekendna.com  ·  link in bio", font=jak(400, 25), fill=MUTED)
tracked(d, MX, 1236, "FOLLOW @WEEKENDNA.LB", jak(700, 26), INK, 5)
d.text((MX, 1278), "A new place every week.", font=serif(400, 34, True), fill=MUTED)
img.save(f"{OUT}/ghosta-5.jpg", quality=94)

cap = """Above the bay, a warm weekend.
Found on Weekendna: Ghosta Guest House, a 400 m² apartment 800 m above sea level in Kaslik and Jounieh, 25 min from Beirut, with a 180° view from Beirut to Byblos. 5 bedrooms and 7 beds for up to 12 guests, heating, a full kitchen, a barbecue and free parking. $220 a night, about $18 each when 12 share.

\U0001F516 Save this for your next weekend, and send it to the group chat.

Request your dates on WhatsApp, nothing to pay yet: weekendna.com (link in bio) \U0001F4C5
\U0001F449 Follow @weekendna.lb so you don't miss the next one. We find a new place for your weekend every week \U0001F3E1

#Weekendna #Lebanon #Jounieh #Kaslik #LebanonWeekend #GuestHouse
"""
open(f"{OUT}/caption.txt", "w", encoding="utf-8").write(cap)
print("ok")
