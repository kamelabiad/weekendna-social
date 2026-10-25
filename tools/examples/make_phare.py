"""Phare du Nord Venue carousel (wedding venue, Batroun). Photos: python3 tools/reel_prep.py photos reels/public/photos/phare 49"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from brand import *

ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
SRC = os.path.join(ROOT, "reels/public/photos/phare")
OUT = os.path.join(ROOT, "posts/2026-11-phare-du-nord")
os.makedirs(OUT, exist_ok=True)
P = lambda n: Image.open(f"{SRC}/49-{n:02d}.webp")

# 1: hero
img = shade(cover(P(3), W, H, cy=0.5), 600)
d = ImageDraw.Draw(img)
logo(d, M, 64)
pill(d, M, 800, "WEDDING VENUE · BATROUN", jak(700, 28))
d.text((M, 880), "Phare du Nord", font=jak(800, 104), fill=WHITE)
d.text((M, 1010), "Sunset weddings by the sea,", font=jak(500, 40), fill=WHITE)
d.text((M, 1060), "up to 450 guests", font=jak(500, 40), fill=WHITE)
rtext(d, W - M, 1140, "عرس عالبحر وقت المغيب، لحد ٤٥٠ ضيف", ar(700, 42), WHITE)
d.text((M, 1220), "@pharedunord", font=jak(600, 30), fill=(235, 235, 235))
img.save(f"{OUT}/phare-1.jpg", quality=92)

# 2: facts
img = shade(cover(P(6), W, H, cy=0.45), 420, 250, 0.9)
d = ImageDraw.Draw(img)
logo(d, M, 64)
d.text((M, 740), "Ceremony and party,", font=jak(800, 66), fill=WHITE)
d.text((M, 818), "one place by the sea", font=jak(800, 66), fill=WHITE)
feats = ["Up to 450 seated guests", "Ceremony on site, bridal suite", "Bring the caterer of your choice", "200 parking spaces and valet"]
y = 940
for en in feats:
    d.ellipse((M, y + 14, M + 16, y + 30), fill=RED)
    d.text((M + 36, y), en, font=jak(700, 36), fill=WHITE)
    y += 64
rtext(d, W - M, y + 16, "الإكليل والسهرة بنفس المحل", ar(700, 40), WHITE)
img.save(f"{OUT}/phare-2.jpg", quality=92)

# 3: night view
img = shade(cover(P(4), W, H, cx=0.4), 860, 230)
d = ImageDraw.Draw(img)
logo(d, M, 64)
d.text((M, 1060), "Lit up by night", font=jak(800, 70), fill=WHITE)
rtext(d, W - M, 1160, "وبالليل، أحلى وأحلى", ar(700, 44), WHITE)
img.save(f"{OUT}/phare-3.jpg", quality=92)

# 4: CTA
img = Image.new("RGB", (W, H), SOFT)
d = ImageDraw.Draw(img)
logo(d, M, 64, color=INK)
ph = cover(P(1), 520, 640, cy=0.55).filter(ImageFilter.UnsharpMask(radius=1.2, percent=60, threshold=2))
mask = Image.new("L", ph.size, 0); ImageDraw.Draw(mask).rounded_rectangle((0, 0, 520, 640), radius=36, fill=255)
img.paste(ph, (W // 2 - 260, 150), mask)
ctext(d, 840, "Planning your wedding?", jak(800, 62), INK)
ctext(d, 925, "Send your date and guest count. The venue", jak(500, 34), (63, 63, 63))
ctext(d, 970, "replies on WhatsApp with a quote.", jak(500, 34), (63, 63, 63))
ctext(d, 1035, "ابعتو التاريخ وعدد الضيوف", ar(700, 38), INK, rtl=True)
ctext(d, 1085, "وبيردّو عليكن عالواتساب بسعر", ar(500, 34), (63, 63, 63), rtl=True)
button(d, 1160, "weekendna.com · link in bio")
img.save(f"{OUT}/phare-4.jpg", quality=92)
print("ok")
