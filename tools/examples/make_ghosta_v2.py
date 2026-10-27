"""Ghosta carousel, v2: question hook on the cover, big-number slide, distance chips, and a share prompt on the last slide.
Run: source tools/setup.sh; python3 tools/examples/make_ghosta_v2.py <photos-folder> <out-folder>
Photos are the listing photos downloaded as p<N>.webp (37 coast view, 22 night lights, 20 balcony at dusk, 24 living, 10 bedroom, 11 balcony)."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
os.environ.setdefault("WK_WORK", os.path.expanduser("~/wk-work"))
from brand import *
from PIL import ImageEnhance
SRC, OUT = sys.argv[1], sys.argv[2]; os.makedirs(OUT, exist_ok=True)
P = lambda n: Image.open(f"{SRC}/p{n}.webp").convert("RGB")
sv = lambda img, n: img.save(f"{OUT}/ghosta-{n}.jpg", quality=92)
INKBG = (16, 18, 28)

def swipe(d, y=1262):
    f = jak(800, 28); w = d.textlength("Swipe", font=f); x = W - M - (w + 44 + 52)
    pill(d, x, y, "Swipe" + " " * 9, f, fg=INK, bg=WHITE)
    ax = x + 22 + w + 14; ay = y + 28
    d.line((ax, ay, ax + 30, ay), fill=INK, width=5); d.line((ax + 18, ay - 12, ax + 31, ay), fill=INK, width=5); d.line((ax + 18, ay + 12, ax + 31, ay), fill=INK, width=5)

def tile(im, w, h, r=30, cx=0.5, cy=0.5):
    t = ImageEnhance.Brightness(cover(im, w, h, cx, cy)).enhance(1.08)
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w, h), radius=r, fill=255); return t, m

# 1 cover: a question, then the name
img = cover(P(37), W, H, cx=0.5, cy=0.5); img = shade(img, 430, 250, 1.0); d = ImageDraw.Draw(img); logo(d, M, 64)
pill(d, M, 700, "GHOSTA GUEST HOUSE · JOUNIEH HILLS", jak(700, 26))
d.text((M, 790), "Wake up above", font=jak(800, 104), fill=WHITE)
d.text((M, 905), "the whole coast?", font=jak(800, 104), fill=WHITE)
rtext(d, W - M, 1062, "فيقو فوق الساحل كله؟", ar(700, 56), WHITE)
d.text((M, 1160), "A 180° view from Beirut to Byblos", font=jak(500, 36), fill=WHITE)
swipe(d, 1250); sv(img, 1)

# 2 big number + three photos
img = Image.new("RGB", (W, H), SOFT); d = ImageDraw.Draw(img); logo(d, M, 64, color=INK)
d.text((M, 170), "Sleeps 12.", font=jak(800, 104), fill=INK)
f1, f2 = jak(800, 54), jak(800, 120); x = M
d.text((x, 308), "From about", font=f1, fill=INK); x += d.textlength("From about", font=f1) + 22
d.text((x, 268), "$18", font=f2, fill=RED); x += d.textlength("$18", font=f2) + 22
d.text((x, 308), "each", font=f1, fill=INK)
y = 470; gap = 18; wd = (W - 2 * M - gap) // 2
t, m = tile(P(24), W - 2 * M, 360, cy=0.6); img.paste(t, (M, y), m)
t, m = tile(P(10), wd, 300, cx=0.4); img.paste(t, (M, y + 360 + gap), m)
t, m = tile(P(11), wd, 300); img.paste(t, (M + wd + gap, y + 360 + gap), m)
x = M
for s in ["5 bedrooms", "400 m²", "Kitchen + BBQ"]:
    pill(d, x, 1210, s, jak(700, 28), fg=WHITE, bg=INK); x += d.textlength(s, font=jak(700, 28)) + 44 + 16
d.text((M, 1285), "$220 a night for the whole house", font=jak(500, 30), fill=(90, 90, 90)); sv(img, 2)

# 3 distances
img = cover(P(20), W, H, cx=0.5); img = Image.blend(img, Image.new("RGB", (W, H), INKBG), 0.35)
img = shade(img, 300, 245, 0.9); d = ImageDraw.Draw(img); logo(d, M, 64)
d.text((M, 470), "Everything", font=jak(800, 96), fill=WHITE)
d.text((M, 580), "is close", font=jak(800, 96), fill=RED)
y = 790
for big, small in [("10 min", "to the beach"), ("25 min", "to Beirut"), ("20 min", "to the Faraya slopes")]:
    d.rounded_rectangle((M, y, W - M, y + 118), radius=30, fill=(255, 255, 255))
    d.text((M + 34, y + 26), big, font=jak(800, 54), fill=RED)
    d.text((M + 290, y + 36), small, font=jak(700, 40), fill=INK); y += 140
rtext(d, W - M, 1250, "عالبحر، عبيروت وعفاريا، كلّن قريبين", ar(700, 38), WHITE); sv(img, 3)

# 4 share prompt + CTA
img = cover(P(22), W, H, cx=0.5); img = Image.blend(img, Image.new("RGB", (W, H), INKBG), 0.45)
d = ImageDraw.Draw(img); logo(d, M, 64)
ctext(d, 360, "Send this to", jak(800, 92), WHITE); ctext(d, 470, "who you\u2019d bring", jak(800, 92), RED)
ctext(d, 610, "ابعتها للي بدّك ياه معك", ar(700, 56), WHITE, rtl=True)
ctext(d, 790, "Ghosta Guest House · from $220 a night", jak(600, 36), WHITE) if False else ctext(d, 790, "Ghosta Guest House · from $220 a night", jak(700, 36), WHITE)
ctext(d, 860, "ابعتوا تواريخكن عالواتساب، بلا ما تدفعوا شي هلّق", ar(700, 38), WHITE, rtl=True)
button(d, 960, "weekendna.com · link in bio")
ctext(d, 1110, "Save it for your next weekend 🔖".replace(" 🔖", ""), jak(500, 32), (230, 230, 230)); sv(img, 4)
print("ok")
