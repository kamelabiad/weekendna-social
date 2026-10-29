"""Royal Chalets and Restaurant carousel (Bcharre & the Cedars, listing 54). Photos: python3 tools/reel_prep.py photos reels/public/photos/royal 54"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from brand import *
ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
SRC = os.path.join(ROOT, "reels/public/photos/royal")
OUT = os.path.join(ROOT, "posts/2026-11-royal-chalets"); os.makedirs(OUT, exist_ok=True)
P = lambda n: Image.open(f"{SRC}/54-{n:02d}.webp").convert("RGB")
DARK = (26, 24, 28)
def framed(img, photo, x0, y0, pw, ph, radius=36):
    p = cover(photo, pw, ph).filter(ImageFilter.UnsharpMask(radius=1.2, percent=60, threshold=2))
    mask = Image.new("L", (pw, ph), 0); ImageDraw.Draw(mask).rounded_rectangle((0, 0, pw, ph), radius=radius, fill=255)
    sh = Image.new("RGBA", (pw + 80, ph + 80), (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle((40, 52, pw + 40, ph + 52), radius=radius + 4, fill=(0, 0, 0, 70))
    sh = sh.filter(ImageFilter.GaussianBlur(18)); img.paste(sh, (x0 - 40, y0 - 40), sh); img.paste(p, (x0, y0), mask)

# 1: framed facade
img = Image.new("RGB", (W, H), SOFT); d = ImageDraw.Draw(img); logo(d, M, 64, color=INK)
pw, ph = 700, 700; x0 = (W - pw) // 2; y0 = 160
framed(img, P(1), x0, y0, pw, ph)
pf = jak(700, 26); t = "BCHARRE & THE CEDARS"; tw = d.textlength(t, font=pf)
pill(d, int((W - tw) / 2 - 22), y0 + ph + 40, t, pf)
ctext(d, y0 + ph + 115, "Royal Chalets and Restaurant", jak(800, 54), INK)
ctext(d, y0 + ph + 190, "رويال شاليهات ومطعم", ar(700, 38), (63, 63, 63), rtl=True)
ctext(d, y0 + ph + 255, "Where the mountains meet the sky", jak(500, 32), (63, 63, 63))
ctext(d, y0 + ph + 310, "@dianatawkk", jak(600, 30), (90, 90, 90))
img.save(f"{OUT}/royal-1.jpg", quality=92)

# 2: facts
img = Image.new("RGB", (W, H), DARK); d = ImageDraw.Draw(img); logo(d, M, 64)
framed(img, P(8), M, 170, W - 2 * M, 400)
d.text((M, 620), "Mountain views,", font=jak(800, 62), fill=WHITE)
d.text((M, 692), "near the ski slopes", font=jak(800, 62), fill=WHITE)
items = [("6 bedrooms, up to 12 guests", "٦ غرف نوم، لحد ١٢ ضيف"), ("Fireplace and heating", "شيمينيه وتدفئة"),
         ("Terrace, garden and barbecue", "تراس وجنينة وشوي"), ("Full kitchen · free parking", "مطبخ كامل وباركينغ مجاني")]
y = 815
for en, a in items:
    d.ellipse((M, y + 14, M + 16, y + 30), fill=RED)
    d.text((M + 36, y), en, font=jak(700, 34), fill=WHITE)
    rtext(d, W - M, y + 44, a, ar(500, 28), (200, 200, 200)); y += 108
d.text((M, 1255), "$80", font=jak(800, 76), fill=RED)
d.text((M + d.textlength("$80", font=jak(800, 76)) + 14, 1288), "/ night · about $7 each when 12 share", font=jak(500, 30), fill=WHITE)
img.save(f"{OUT}/royal-2.jpg", quality=92)

# 3: cosy interior
img = Image.new("RGB", (W, H), SOFT); d = ImageDraw.Draw(img); logo(d, M, 64, color=INK)
framed(img, P(10), (W - 760) // 2, 170, 760, 760)
ctext(d, 990, "Cosy mountain living", jak(800, 62), INK)
ctext(d, 1075, "Family-friendly · pets allowed", jak(500, 34), (63, 63, 63))
ctext(d, 1140, "للعيلة، والحيوانات الأليفة مسموحة", ar(700, 38), INK, rtl=True)
img.save(f"{OUT}/royal-3.jpg", quality=92)

# 4: follow CTA
img = Image.new("RGB", (W, H), RED); d = ImageDraw.Draw(img); logo(d, M, 64, accent=INK)
ctext(d, 400, "Your mountain", jak(800, 96), WHITE)
ctext(d, 510, "weekend starts here", jak(800, 76), WHITE)
ctext(d, 640, "Bcharre & the Cedars, from $80", jak(500, 36), WHITE)
ctext(d, 710, "ويكندكن بالجبل بيبلش من هون", ar(700, 44), WHITE, rtl=True)
ctext(d, 850, "A new place to escape to every week", jak(700, 38), WHITE)
f = jak(800, 48); t = "Follow @weekendna.lb"; bw = d.textlength(t, font=f)
d.rounded_rectangle(((W - bw) / 2 - 50, 925, (W + bw) / 2 + 50, 1025), radius=50, fill=WHITE)
d.text(((W - bw) / 2, 945), t, font=f, fill=RED)
ctext(d, 1065, "تابعونا، كل أسبوع محل جديد", ar(700, 40), WHITE, rtl=True)
ctext(d, 1190, "Request your dates on WhatsApp · link in bio", jak(500, 30), (255, 225, 228))
img.save(f"{OUT}/royal-4.jpg", quality=92)
print("ok")
