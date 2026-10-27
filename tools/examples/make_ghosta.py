import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from brand import *
SRC = f"{S}/ghosta-src"; OUT = f"{S}/ghosta-out"; os.makedirs(OUT, exist_ok=True)
def save(img, n): img.save(f"{OUT}/ghosta-{n}.jpg", quality=92)

# 1 hero: the view
img = cover(Image.open(f"{SRC}/p14.webp"), W, H, cx=0.55)
img = shade(img, 620); d = ImageDraw.Draw(img); logo(d, M, 64)
pill(d, M, 730, "JOUNIEH HILLS · 800 M UP", jak(700, 28))
d.text((M, 806), "Ghosta", font=jak(800, 104), fill=WHITE)
d.text((M, 930), "Guest House", font=jak(800, 104), fill=WHITE)
d.text((M, 1090), "Wake up to a 180° view from Beirut to Byblos", font=jak(500, 36), fill=WHITE)
rtext(d, W - M, 1150, "بيت ضيافة بغوسطا، منظر من بيروت لجبيل", ar(700, 38), WHITE)
save(img, 1)

# 2 balcony at night + features
img = cover(Image.open(f"{SRC}/p19.webp"), W, H, cx=0.5)
img = shade(img, 420, 248, 0.9); d = ImageDraw.Draw(img); logo(d, M, 64)
d.text((M, 760), "Room for", font=jak(800, 70), fill=WHITE)
d.text((M, 840), "the whole family", font=jak(800, 70), fill=WHITE)
feats = ["5 bedrooms · sleeps up to 12", "400 m² with a full kitchen and BBQ",
         "10 min to the beach, 20 to Beirut", "20 min to the Faraya ski slopes"]
y = 950
for en in feats:
    d.ellipse((M, y + 14, M + 16, y + 30), fill=RED)
    d.text((M + 36, y), en, font=jak(700, 34), fill=WHITE); y += 62
save(img, 2)

# 3 living room
img = cover(Image.open(f"{SRC}/p8.webp"), W, H, cx=0.5)
img = shade(img, 820, 230); d = ImageDraw.Draw(img); logo(d, M, 64)
d.text((M, 1090), "Bright, roomy spaces", font=jak(800, 62), fill=WHITE)
d.text((M, 1162), "for everyone", font=jak(800, 62), fill=WHITE)
save(img, 3)

# 4 night view + CTA
img = cover(Image.open(f"{SRC}/p26.webp"), W, H, cx=0.5)
dark = Image.new("RGB", (W, H), (10, 12, 20)); img = Image.blend(img, dark, 0.35)
img = shade(img, 500, 220, 1.0); d = ImageDraw.Draw(img); logo(d, M, 64)
ctext(d, 740, "And this, every night ✦".replace(" ✦", ""), jak(800, 66), WHITE)
ctext(d, 830, "From $220 a night · up to 12 guests", jak(600 if False else 500, 38), WHITE)
ctext(d, 905, "ابعتوا تواريخكن عالواتساب، بلا ما تدفعوا شي هلّق", ar(700, 40), WHITE, rtl=True)
button(d, 1010, "weekendna.com · link in bio")
save(img, 4)
print("ok")
