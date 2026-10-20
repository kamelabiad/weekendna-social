import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

S = "/tmp/claude-0/-home-claude/37eaf9a6-6769-5ff9-9f63-4801d2f782ff/scratchpad"
SRC = f"{S}/karst-src"
OUT = f"{S}/karst-out"
os.makedirs(OUT, exist_ok=True)
F = f"{S}/fonts"
W, H = 1080, 1350
RED = (224, 38, 59)
INK = (34, 34, 34)
WHITE = (255, 255, 255)
SOFT = (253, 237, 239)

L = ImageFont.Layout.RAQM
def jak(w, s): return ImageFont.truetype(f"{F}/fontsource-plus-jakarta-sans-5.3.0/files/plus-jakarta-sans-latin-{w}-normal.woff", s, layout_engine=L)
def out(w, s): return ImageFont.truetype(f"{F}/fontsource-outfit-5.3.0/files/outfit-latin-{w}-normal.woff", s, layout_engine=L)
def ar(w, s): return ImageFont.truetype(f"{F}/fontsource-ibm-plex-sans-arabic-5.3.0/files/ibm-plex-sans-arabic-arabic-{w}-normal.woff", s, layout_engine=L)

def cover(img, w, h, cx=0.5, cy=0.5):
    img = img.convert("RGB")
    r = max(w / img.width, h / img.height)
    img = img.resize((round(img.width * r), round(img.height * r)), Image.LANCZOS)
    x = int((img.width - w) * cx); y = int((img.height - h) * cy)
    return img.crop((x, y, x + w, y + h))

def gradient(h, top_a, bot_a, k=1.6):
    g = Image.new("L", (1, h))
    for y in range(h):
        g.putpixel((0, y), int(top_a + (bot_a - top_a) * (y / (h - 1)) ** k))
    return g.resize((W, h))

def shade(img, start, alpha=235, k=1.6):
    dark = Image.new("RGB", (W, H - start), (12, 12, 14))
    img.paste(dark, (0, start), gradient(H - start, 0, alpha, k))
    top = Image.new("RGB", (W, 220), (12, 12, 14))
    img.paste(top, (0, 0), gradient(220, 120, 0).transpose(Image.FLIP_TOP_BOTTOM).transpose(Image.FLIP_TOP_BOTTOM) if False else Image.linear_gradient("L").resize((W, 220)).point(lambda v: int((255 - v) * 0.45)))
    return img

def logo(d, x, y, color=WHITE, size=46):
    f1 = out(700, size); f2 = ar(700, int(size * 1.02))
    d.text((x, y), "weekend", font=f1, fill=color)
    w = d.textlength("weekend", font=f1)
    d.text((x + w + 2, y - int(size * 0.08)), "نا", font=f2, fill=RED if color == WHITE else RED, direction="rtl")

def pill(d, x, y, text, font, fg=WHITE, bg=RED, pad=(22, 12)):
    w = d.textlength(text, font=font)
    bb = font.getbbox(text)
    h = bb[3] - bb[1]
    d.rounded_rectangle((x, y, x + w + pad[0] * 2, y + h + pad[1] * 2 + 6), radius=40, fill=bg)
    d.text((x + pad[0], y + pad[1] - bb[1] + 3), text, font=font, fill=fg)

def rtext(d, xr, y, text, font, fill):
    w = d.textlength(text, font=font, direction="rtl")
    d.text((xr - w, y), text, font=font, fill=fill, direction="rtl")

def dots(d, n, active, color=WHITE):
    cx = W // 2 - (n - 1) * 14; y = H - 44
    for i in range(n):
        r = 7 if i == active else 5
        c = color if i == active else tuple(list(color[:3])) + (0,)
        d.ellipse((cx + i * 28 - r, y - r, cx + i * 28 + r, y + r), fill=color if i == active else (200, 200, 200))

M = 72

# ---------- Slide 1: hero ----------
img = cover(Image.open(f"{SRC}/39956276d28a.webp"), W, H, cx=0.45)
img = shade(img, 640)
d = ImageDraw.Draw(img)
logo(d, M, 64)
pill(d, M, 820, "WEDDING VENUE · BATROUN", jak(700, 28))
d.text((M, 900), "Domaine du Karst", font=jak(800, 98), fill=WHITE)
d.text((M, 1030), "Up to 300 guests · ceremony and party", font=jak(500, 38), fill=WHITE)
d.text((M, 1078), "in one place, under the stars", font=jak(500, 38), fill=WHITE)
rtext(d, W - M, 1150, "قاعة أعراس بالبترون، لحد ٣٠٠ ضيف", ar(700, 40), (255, 255, 255))
img.save(f"{OUT}/karst-1.jpg", quality=92)

# ---------- Slide 2: features ----------
img = cover(Image.open(f"{SRC}/5b675a484aa9.webp"), W, H, cx=0.45)
img = shade(img, 380, 250, 0.9)
d = ImageDraw.Draw(img)
logo(d, M, 64)
d.text((M, 760), "Your whole day,", font=jak(800, 70), fill=WHITE)
d.text((M, 840), "one venue", font=jak(800, 70), fill=WHITE)
feats = [("Open-air terraces with string lights", "تراسات مفتوحة مع أضواء"),
         ("Pool area with an indoor bar", "مسبح وبار داخلي"),
         ("180° view of Sannine and Beirut", "منظر ١٨٠° عصنين وبيروت"),
         ("Celebrations until 4am", "السهرة لحد الـ٤ الصبح")]
y = 950
for en, a in feats:
    d.ellipse((M, y + 14, M + 16, y + 30), fill=RED)
    d.text((M + 36, y), en, font=jak(700, 34), fill=WHITE)
    y += 62
img.save(f"{OUT}/karst-2.jpg", quality=92)

# ---------- Slide 3: CTA ----------
img = Image.new("RGB", (W, H), SOFT)
d = ImageDraw.Draw(img)
logo(d, M, 64, color=INK)
ph = Image.open(f"{SRC}/210a02608bff.webp").convert("RGB")
ph = ph.resize((600, 600), Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=1.2, percent=60, threshold=2))
mask = Image.new("L", ph.size, 0); ImageDraw.Draw(mask).rounded_rectangle((0, 0, 600, 600), radius=36, fill=255)
sh = Image.new("RGBA", (680, 680), (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle((40, 50, 640, 650), radius=40, fill=(0, 0, 0, 60))
sh = sh.filter(ImageFilter.GaussianBlur(18))
img.paste(sh, (W // 2 - 340, 150 - 40), sh)
img.paste(ph, (W // 2 - 300, 150), mask)
def ctext(y, t, f, fill, rtl=False):
    w = d.textlength(t, font=f, direction="rtl" if rtl else None)
    d.text(((W - w) / 2, y), t, font=f, fill=fill, direction="rtl" if rtl else None)
ctext(800, "Planning your wedding?", jak(800, 62), INK)
ctext(885, "Send your date and guest count. The owner", jak(500, 34), (63, 63, 63))
ctext(930, "replies on WhatsApp with a free quote.", jak(500, 34), (63, 63, 63))
ctext(1000, "عم تحضّرو لعرسكن؟ ابعتو التاريخ وعدد الضيوف", ar(700, 36), INK, rtl=True)
ctext(1050, "وصاحب المحل بيرد عليكن عالواتساب", ar(500, 34), (63, 63, 63), rtl=True)
bf = jak(800, 36); t = "weekendna.com · link in bio"
bw = d.textlength(t, font=bf)
d.rounded_rectangle(((W - bw) / 2 - 40, 1140, (W + bw) / 2 + 40, 1222), radius=44, fill=RED)
d.text(((W - bw) / 2, 1160), t, font=bf, fill=WHITE)
img.save(f"{OUT}/karst-3.jpg", quality=92)
print("ok")
