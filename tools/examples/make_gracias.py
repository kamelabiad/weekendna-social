import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from brand import *
OUT = f"{S}/gracias-out"; os.makedirs(OUT, exist_ok=True)
sv = lambda img, n: img.save(f"{OUT}/gracias-{n}.jpg", quality=92)
ph = Image.open(f"{S}/src-19/balcony.webp").convert("RGB")

# 1 hero
img = cover(ph, W, H, cx=0.35); img = shade(img, 700); d = ImageDraw.Draw(img); logo(d, M, 64)
pill(d, M, 860, "BATROUN · NEW ON WEEKENDNA", jak(700, 28))
d.text((M, 936), "Gracias Guesthouse", font=jak(800, 88), fill=WHITE)
d.text((M, 1060), "Morning coffee with a sea view", font=jak(500, 38), fill=WHITE)
rtext(d, W - M, 1130, "قهوة الصبح عالبلكون، والبحر قدّامك", ar(700, 40), WHITE)
sv(img, 1)

# 2 details over blurred photo
bg = cover(ph, W, H, cx=0.3).filter(ImageFilter.GaussianBlur(28))
img = Image.blend(bg, Image.new("RGB", (W, H), (14, 18, 26)), 0.55); d = ImageDraw.Draw(img); logo(d, M, 64)
t = cover(ph, W - 2 * M, 560, cx=0.25, cy=0.45); m = Image.new("L", t.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0) + t.size, radius=32, fill=255)
img.paste(t, (M, 170), m)
d.text((M, 790), "A Batroun stay", font=jak(800, 66), fill=WHITE)
d.text((M, 866), "for up to 4", font=jak(800, 66), fill=WHITE)
y = 990
for en in ["Balcony with a sea view", "Up to 4 guests", "Owner replies on WhatsApp"]:
    d.ellipse((M, y + 14, M + 16, y + 30), fill=RED); d.text((M + 36, y), en, font=jak(700, 34), fill=WHITE); y += 62
sv(img, 2)

# 3 CTA
img = Image.new("RGB", (W, H), RED); d = ImageDraw.Draw(img); logo(d, M, 64, accent=INK)
ctext(d, 480, "Planning a Batroun", jak(800, 76), WHITE)
ctext(d, 570, "weekend?", jak(800, 76), WHITE)
ctext(d, 690, "Request your dates on WhatsApp, nothing to pay yet", jak(500, 36), WHITE)
ctext(d, 770, "ابعتوا تواريخكن عالواتساب، بلا ما تدفعوا شي هلّق", ar(700, 42), WHITE, rtl=True)
button(d, 900, "weekendna.com · link in bio", bg=WHITE, fg=RED)
sv(img, 3)
print("ok")
