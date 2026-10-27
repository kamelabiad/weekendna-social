import os, sys
sys.path.insert(0, os.path.dirname(__file__))
S0 = "/tmp/claude-0/-home-claude/37eaf9a6-6769-5ff9-9f63-4801d2f782ff/scratchpad"
os.environ["WK_WORK"] = S0
from brand import *
from PIL import ImageEnhance
OUT = f"{S0}/acampar-out"; os.makedirs(OUT, exist_ok=True)
for f in os.listdir(OUT):
    if f.startswith("acampar-"): os.remove(f"{OUT}/{f}")
sv = lambda img, n: img.save(f"{OUT}/acampar-{n}.jpg", quality=92)
def L(id): return [Image.open(f"{S0}/src-{id}/" + l.split('/')[-1]).convert("RGB") for l in open(f"{S0}/src-{id}/list.txt").read().split()]
a39, a40 = L(39), L(40)
ext, small_in = a39[0], a39[1]
terrace, big_in = a40[0], a40[2]
DARK = (26, 24, 28)

# 1 hero
img = cover(ext, W, H, cx=0.62); img = shade(img, 620, 240); d = ImageDraw.Draw(img); logo(d, M, 64)
pill(d, M, 800, "FARAYA · NEW ON WEEKENDNA", jak(700, 28))
d.text((M, 876), "Acampar", font=jak(800, 110), fill=WHITE)
d.text((M, 1010), "Cosy wooden bungalows,", font=jak(500, 38), fill=WHITE)
d.text((M, 1058), "close to the ski slopes", font=jak(500, 38), fill=WHITE)
rtext(d, W - M, 1132, "بنغلوهات خشب دافية، قراب عالتلج", ar(700, 40), WHITE)
sv(img, 1)

# 2 two huts
img = Image.new("RGB", (W, H), SOFT); d = ImageDraw.Draw(img); logo(d, M, 64, color=INK)
d.text((M, 150), "Pick your hut", font=jak(800, 72), fill=INK)
def tile(im, w, h, r=28, cx=0.5, cy=0.5):
    t = ImageEnhance.Brightness(cover(im, w, h, cx, cy)).enhance(1.2)
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w, h), radius=r, fill=255); return t, m
y = 270
for im, name, sub, price in [(small_in, "Small hut", "For 2 · fireplace · kitchenette", "$80"),
                              (big_in, "Big hut", "Up to 4 · sofa bed · fireplace", "$100")]:
    t, m = tile(im, W - 2 * M, 330, cy=0.55); img.paste(t, (M, y), m)
    d.text((M, y + 350), name, font=jak(800, 44), fill=INK)
    pw = d.textlength(price, font=jak(800, 44)); nw = d.textlength("/ night", font=jak(500, 28))
    d.text((W - M - pw - nw - 10, y + 350), price, font=jak(800, 44), fill=RED)
    d.text((W - M - nw, y + 364), "/ night", font=jak(500, 28), fill=(90, 90, 90))
    d.text((M, y + 408), sub, font=jak(500, 30), fill=(90, 90, 90))
    y += 520
sv(img, 2)

# 3 terrace + features
img = Image.new("RGB", (W, H), DARK)
top = ImageEnhance.Brightness(cover(terrace, W, 780, cx=0.5, cy=0.5)).enhance(1.05)
img.paste(top, (0, 0)); img.paste(Image.new("RGB", (W, 120), DARK), (0, 660), gradient(120, 0, 255, 1.0))
d = ImageDraw.Draw(img); logo(d, M, 64)
d.text((M, 800), "Fireplace on,", font=jak(800, 66), fill=WHITE)
d.text((M, 876), "snow outside", font=jak(800, 66), fill=WHITE)
y = 990
for en in ["Fireplace and a small kitchenette", "Terrace with a mountain view", "BBQ and free parking", "Near the Faraya ski slopes"]:
    d.ellipse((M, y + 14, M + 16, y + 30), fill=RED); d.text((M + 36, y), en, font=jak(700, 34), fill=WHITE); y += 62
sv(img, 3)

# 4 CTA
img = Image.new("RGB", (W, H), RED); d = ImageDraw.Draw(img); logo(d, M, 64, accent=INK)
ctext(d, 470, "From $80", jak(800, 110), WHITE)
ctext(d, 600, "a night", jak(800, 66), WHITE)
ctext(d, 710, "Your winter escape in Faraya", jak(500, 38), WHITE)
ctext(d, 790, "ابعتوا تواريخكن عالواتساب، بلا ما تدفعوا شي هلّق", ar(700, 42), WHITE, rtl=True)
button(d, 920, "weekendna.com · link in bio", bg=WHITE, fg=RED)
sv(img, 4)
print("ok")
