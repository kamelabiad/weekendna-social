import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

S = "/tmp/claude-0/-home-claude/37eaf9a6-6769-5ff9-9f63-4801d2f782ff/scratchpad"
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

def ctext(d, y, t, f, fill, rtl=False):
    w = d.textlength(t, font=f, direction="rtl" if rtl else None)
    d.text(((W - w) / 2, y), t, font=f, fill=fill, direction="rtl" if rtl else None)

def button(d, y, t, f=None, bg=RED, fg=WHITE):
    f = f or jak(800, 36); bw = d.textlength(t, font=f)
    d.rounded_rectangle(((W - bw) / 2 - 40, y, (W + bw) / 2 + 40, y + 82), radius=44, fill=bg)
    d.text(((W - bw) / 2, y + 20), t, font=f, fill=fg)
