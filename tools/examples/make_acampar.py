import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from brand import *
OUT = f"{S}/acampar-out"; os.makedirs(OUT, exist_ok=True)
sv = lambda img, n: img.save(f"{OUT}/acampar-{n}.jpg", quality=92)
fs = [l.split('/')[-1] for l in open(f"{S}/src-39/list.txt").read().split()]
ext = Image.open(f"{S}/src-39/{fs[0]}").convert("RGB"); inn = Image.open(f"{S}/src-39/{fs[1]}").convert("RGB")

# 1 hero: snow
img = cover(ext, W, H, cx=0.62); img = shade(img, 620, 240); d = ImageDraw.Draw(img); logo(d, M, 64)
pill(d, M, 800, "FARAYA · NEW ON WEEKENDNA", jak(700, 28))
d.text((M, 876), "Acampar", font=jak(800, 110), fill=WHITE)
d.text((M, 1010), "A cosy bungalow for two,", font=jak(500, 38), fill=WHITE)
d.text((M, 1058), "close to the ski slopes", font=jak(500, 38), fill=WHITE)
rtext(d, W - M, 1132, "بنغلو دافي لشخصين، قريب عالتلج", ar(700, 40), WHITE)
sv(img, 1)

# 2 interior + features
img = Image.new("RGB", (W, H), (26, 24, 28))
top = cover(inn, W, 780, cx=0.5, cy=0.6)
from PIL import ImageEnhance
top = ImageEnhance.Brightness(top).enhance(1.25)
img.paste(top, (0, 0)); img.paste(Image.new("RGB", (W, 120), (26, 24, 28)), (0, 660), gradient(120, 0, 255, 1.0))
d = ImageDraw.Draw(img); logo(d, M, 64)
d.text((M, 800), "Fireplace on,", font=jak(800, 66), fill=WHITE)
d.text((M, 876), "snow outside", font=jak(800, 66), fill=WHITE)
y = 990
for en in ["Studio bungalow for 2", "Fireplace and a small kitchenette", "Terrace with a mountain view, BBQ", "Near the Faraya ski slopes"]:
    d.ellipse((M, y + 14, M + 16, y + 30), fill=RED); d.text((M + 36, y), en, font=jak(700, 34), fill=WHITE); y += 62
sv(img, 2)

# 3 CTA
img = Image.new("RGB", (W, H), RED); d = ImageDraw.Draw(img); logo(d, M, 64, accent=INK)
ctext(d, 470, "Only $80", jak(800, 110), WHITE)
ctext(d, 600, "a night for two", jak(800, 66), WHITE)
ctext(d, 710, "Your winter escape in Faraya", jak(500, 38), WHITE)
ctext(d, 790, "شوفو الأيام الفاضية واحجزو عالواتساب", ar(700, 42), WHITE, rtl=True)
button(d, 920, "weekendna.com · link in bio", bg=WHITE, fg=RED)
sv(img, 3)
print("ok")
