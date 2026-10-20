import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from brand import *
OUT = f"{S}/majestic-out"; os.makedirs(OUT, exist_ok=True)
sv = lambda img, n: img.save(f"{OUT}/majestic-{n}.jpg", quality=92)
DARK = (26, 24, 28)
ph = Image.open(f"{S}/src-23/de078e179857-1600.webp").convert("RGB")

# 1: framed facade
img = Image.new("RGB", (W, H), SOFT); d = ImageDraw.Draw(img); logo(d, M, 64, color=INK)
pw, phh = 560, 860
p = ph.resize((pw, phh), Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=1.2, percent=60, threshold=2))
mask = Image.new("L", (pw, phh), 0); ImageDraw.Draw(mask).rounded_rectangle((0, 0, pw, phh), radius=36, fill=255)
sh = Image.new("RGBA", (pw + 80, phh + 80), (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle((40, 52, pw + 40, phh + 52), radius=40, fill=(0, 0, 0, 55))
sh = sh.filter(ImageFilter.GaussianBlur(18)); x0 = (W - pw) // 2; y0 = 150
img.paste(sh, (x0 - 40, y0 - 40), sh); img.paste(p, (x0, y0), mask)
pf = jak(700, 26); t = "BYBLOS · JBEIL"; tw = d.textlength(t, font=pf)
pill(d, int((W - tw) / 2 - 22), y0 + phh + 40, t, pf)
ctext(d, y0 + phh + 110, "Majestic Byblos Grand Hotel", jak(800, 58), INK)
ctext(d, y0 + phh + 190, "فندق ماجستيك بجبيل، عالبحر", ar(700, 36), (63, 63, 63), rtl=True)
sv(img, 1)

# 2: deluxe room details
img = Image.new("RGB", (W, H), DARK); d = ImageDraw.Draw(img); logo(d, M, 64)
pill(d, M, 200, "THE DELUXE ROOM", jak(700, 28))
d.text((M, 280), "Sea or city views", font=jak(800, 76), fill=WHITE)
d.text((M, 370), "from your balcony", font=jak(800, 76), fill=WHITE)
items = [("Twin or king-size bed", "تختين أو تخت كينغ"), ("Private balcony", "بلكون خاص"),
         ("Mediterranean or Byblos city views", "منظر عالبحر أو على جبيل"), ("Air conditioning · free parking", "مكيّف وباركينغ مجاني")]
y = 540
for en, a in items:
    d.ellipse((M, y + 14, M + 16, y + 30), fill=RED)
    d.text((M + 36, y), en, font=jak(700, 36), fill=WHITE)
    rtext(d, W - M, y + 48, a, ar(500, 30), (200, 200, 200)); y += 120
d.text((M, 1080), "$130", font=jak(800, 84), fill=RED)
d.text((M + d.textlength("$130", font=jak(800, 84)) + 14, 1118), "/ night · 2 guests", font=jak(500, 36), fill=WHITE)
sv(img, 2)

# 3: CTA
img = Image.new("RGB", (W, H), RED); d = ImageDraw.Draw(img); logo(d, M, 64, accent=INK)
ctext(d, 470, "Your Byblos", jak(800, 96), WHITE)
ctext(d, 580, "weekend starts here", jak(800, 76), WHITE)
ctext(d, 710, "Sea views, a private balcony, from $130", jak(500, 36), WHITE)
ctext(d, 790, "ويكندكن بجبيل بيبلش من هون", ar(700, 44), WHITE, rtl=True)
button(d, 920, "weekendna.com · link in bio", bg=WHITE, fg=RED)
sv(img, 3)
print("ok")
