"""Two Batroun apartments by the same owner: Le Grey Apartments (Haven, 48) + Grandpa's Apartment (31).
Photos: python3 tools/reel_prep.py photos reels/public/photos/legrey 48 31"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from brand import *

ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
SRC = os.path.join(ROOT, "reels/public/photos/legrey")
OUT = os.path.join(ROOT, "posts/2026-11-le-grey")
os.makedirs(OUT, exist_ok=True)
P = lambda n: Image.open(f"{SRC}/{n}.webp")

# 1: hero (balcony view)
img = shade(cover(P("48-07"), W, H, cy=0.55), 520, 250, 1.1)
d = ImageDraw.Draw(img)
logo(d, M, 64)
pill(d, M, 820, "APARTMENTS · BATROUN", jak(700, 28))
d.text((M, 900), "Le Grey", font=jak(800, 110), fill=WHITE)
d.text((M, 1035), "Two family apartments in Batroun,", font=jak(500, 40), fill=WHITE)
d.text((M, 1085), "from $80 a night", font=jak(500, 40), fill=WHITE)
rtext(d, W - M, 1160, "شقتين بالبترون، من ٨٠ دولار بالليلة", ar(700, 42), WHITE)
d.text((M, 1230), "@legreyapt", font=jak(600, 30), fill=(235, 235, 235))
img.save(f"{OUT}/legrey-1.jpg", quality=92)

def unit(photo, n, title, price, feats, ar_line, cx=0.5):
    img = shade(cover(P(photo), W, H, cx=cx), 430, 250, 0.9)
    d = ImageDraw.Draw(img)
    logo(d, M, 64)
    pill(d, M, 740, price, jak(700, 30))
    d.text((M, 820), title, font=jak(800, 66), fill=WHITE)
    y = 930
    for en in feats:
        d.ellipse((M, y + 14, M + 16, y + 30), fill=RED)
        d.text((M + 36, y), en, font=jak(700, 36), fill=WHITE)
        y += 64
    rtext(d, W - M, y + 16, ar_line, ar(700, 40), WHITE)
    img.save(f"{OUT}/legrey-{n}.jpg", quality=92)

unit("48-05", 2, "Le Grey Haven", "$80 / NIGHT · UP TO 4",
     ["2 bedrooms, newly renovated bathroom", "65-inch Smart TV, Netflix, surround sound", "Sea and mountain view", "Close to the beach, pubs and restaurants"],
     "غرفتين نوم، وقريبة عالبحر والمطاعم", cx=0.45)
unit("31-02", 3, "Grandpa's Apartment", "$120 / NIGHT · UP TO 9",
     ["3 bedrooms, ideal for big groups", "Spacious terrace over the town", "Garden, full kitchen, washing machine", "In Batroun city center"],
     "٣ غرف نوم لـ٩ أشخاص، بقلب البترون", cx=0.5)

# 4: CTA
img = Image.new("RGB", (W, H), SOFT)
d = ImageDraw.Draw(img)
logo(d, M, 64, color=INK)
ph = cover(P("48-04"), 520, 640, cy=0.6).filter(ImageFilter.UnsharpMask(radius=1.2, percent=60, threshold=2))
mask = Image.new("L", ph.size, 0); ImageDraw.Draw(mask).rounded_rectangle((0, 0, 520, 640), radius=36, fill=255)
img.paste(ph, (W // 2 - 260, 150), mask)
ctext(d, 840, "From $80 / night", jak(800, 66), INK)
ctext(d, 930, "Request your dates on WhatsApp, nothing to pay yet.", jak(500, 34), (63, 63, 63))
ctext(d, 975, "24h electricity, Wi-Fi, free parking.", jak(500, 34), (63, 63, 63))
ctext(d, 1040, "ابعتوا تواريخكن عالواتساب، بلا ما تدفعوا شي هلّق", ar(700, 38), INK, rtl=True)
button(d, 1150, "weekendna.com · link in bio")
img.save(f"{OUT}/legrey-4.jpg", quality=92)
print("ok")
