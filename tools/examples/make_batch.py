import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from brand import *

def load(id, n, crop_bars=None):
    f = [l.split('/')[-1] for l in open(f"{S}/src-{id}/list.txt").read().split()][n - 1]
    im = Image.open(f"{S}/src-{id}/{f}").convert("RGB")
    if crop_bars: im = im.crop((0, crop_bars[0], im.width, crop_bars[1]))
    return im

def feats(d, y, items, size=34, step=62):
    for en in items:
        d.ellipse((M, y + 14, M + 16, y + 30), fill=RED)
        d.text((M + 36, y), en, font=jak(700, size), fill=WHITE); y += step

# ================= Bayt Baabdat =================
OUT = f"{S}/baabdat-out"; os.makedirs(OUT, exist_ok=True)
sv = lambda img, n: img.save(f"{OUT}/baabdat-{n}.jpg", quality=92)

img = cover(load(32, 5), W, H, cy=0.55); img = shade(img, 640); d = ImageDraw.Draw(img); logo(d, M, 64)
pill(d, M, 760, "BROUMMANA · METN", jak(700, 28))
d.text((M, 836), "Bayt Baabdat", font=jak(800, 100), fill=WHITE)
d.text((M, 970), "Your own private pool and garden", font=jak(500, 38), fill=WHITE)
d.text((M, 1018), "in the Metn hills", font=jak(500, 38), fill=WHITE)
rtext(d, W - M, 1092, "مسبح خاص وجنينة، بقلب المتن", ar(700, 40), WHITE)
sv(img, 1)

img = cover(load(32, 6, (400, 1586)), W, H, cy=0.6); img = shade(img, 420, 248, 0.9); d = ImageDraw.Draw(img); logo(d, M, 64)
d.text((M, 760), "Day use", font=jak(800, 70), fill=WHITE)
d.text((M, 840), "or overnight", font=jak(800, 70), fill=WHITE)
feats(d, 950, ["2 bedrooms · up to 5 guests", "Private pool and garden", "Fireplace and BBQ", "Book for the day or the night"])
sv(img, 2)

img = cover(load(32, 1, (201, 1799)), W, H, cy=0.5); img = shade(img, 860, 230); d = ImageDraw.Draw(img); logo(d, M, 64)
d.text((M, 1100), "Green, quiet", font=jak(800, 64), fill=WHITE)
d.text((M, 1174), "and all yours", font=jak(800, 64), fill=WHITE)
sv(img, 3)

img = cover(load(32, 8), W, H, cy=0.45); img = Image.blend(img, Image.new("RGB", (W, H), (10, 10, 14)), 0.45)
img = shade(img, 450, 225, 1.0); d = ImageDraw.Draw(img); logo(d, M, 64)
ctext(d, 760, "From $100 a night", jak(800, 68), WHITE)
ctext(d, 852, "Day use or overnight · up to 5 guests", jak(500, 36), WHITE)
ctext(d, 922, "شوفو الأيام الفاضية واحجزو عالواتساب", ar(700, 40), WHITE, rtl=True)
button(d, 1030, "weekendna.com · link in bio")
sv(img, 4)

# ================= Faraya Village Club =================
OUT = f"{S}/faraya-out"; os.makedirs(OUT, exist_ok=True)
sv = lambda img, n: img.save(f"{OUT}/faraya-{n}.jpg", quality=92)
DARK = (26, 24, 28)

def tile(im, w, h, r=28, cx=0.5, cy=0.5):
    t = cover(im, w, h, cx, cy).filter(ImageFilter.UnsharpMask(radius=1.0, percent=50, threshold=2))
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w, h), radius=r, fill=255)
    return t, m

# slide 1: title + 2x2 grid
img = Image.new("RGB", (W, H), DARK); d = ImageDraw.Draw(img); logo(d, M, 64)
pill(d, M, 150, "FARAYA · MZAAR", jak(700, 28))
d.text((M, 222), "Faraya Village Club", font=jak(800, 76), fill=WHITE)
d.text((M, 316), "Ski season is almost here ❄".replace(" ❄", ""), font=jak(500, 38), fill=(235, 235, 235))
rtext(d, W - M, 372, "موسم التزلج قرّب، احجزو شاليهكن بفاريا", ar(700, 36), WHITE)
g = 20; tw = (W - 2 * M - g) // 2; th = 400; y0 = 460
for k, (id, n) in enumerate([(26, 1), (26, 2), (26, 3), (26, 6)]):
    t, m = tile(load(id, n), tw, th); img.paste(t, (M + (k % 2) * (tw + g), y0 + (k // 2) * (th + g)), m)
sv(img, 1)

# slide 2: three ways to stay
img = Image.new("RGB", (W, H), SOFT); d = ImageDraw.Draw(img); logo(d, M, 64, color=INK)
d.text((M, 150), "3 ways to stay", font=jak(800, 72), fill=INK)
rows = [((27, 1), "Studio Chalet", "2 guests · 7 min to Mzaar", "$150"),
        ((28, 1), "Two-Bedroom Chalet", "Up to 7 guests · fireplace", "$450"),
        ((26, 5), "Suite & Spa with Jacuzzi", "2 guests · jacuzzi + fireplace", "$450")]
y = 280; ph = 300
for (id, n), name, sub, price in rows:
    t, m = tile(load(id, n), 300, ph, r=24); img.paste(t, (M, y), m)
    d.text((M + 336, y + 70), name, font=jak(800, 40), fill=INK)
    d.text((M + 336, y + 128), sub, font=jak(500, 30), fill=(90, 90, 90))
    d.text((M + 336, y + 186), price, font=jak(800, 40), fill=RED)
    d.text((M + 336 + d.textlength(price, font=jak(800, 40)) + 10, y + 198), "/ night", font=jak(500, 28), fill=(90, 90, 90))
    y += ph + 34
d.text((M, 1290 - 20), "Heated pool · spa · gym · BBQ · free parking", font=jak(600 if False else 500, 28), fill=(90, 90, 90))
sv(img, 2)

# slide 3: cosy + CTA
img = Image.new("RGB", (W, H), DARK); d = ImageDraw.Draw(img); logo(d, M, 64)
t, m = tile(load(27, 5), 452, 600); img.paste(t, (M, 170), m)
t, m = tile(load(26, 4), 452, 600); img.paste(t, (M + 472, 170), m)
ctext(d, 830, "Fireplace nights,", jak(800, 64), WHITE)
ctext(d, 910, "snowy mornings", jak(800, 64), WHITE)
ctext(d, 1008, "احجزو عالواتساب، اللينك بالبايو", ar(700, 38), WHITE, rtl=True)
button(d, 1100, "weekendna.com · link in bio")
sv(img, 3)
print("ok")
