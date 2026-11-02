"""Flat illustrated scenes for City Guides when no real photo of a place exists (honest: drawn, not photographic). Each returns a PIL image 1080x780."""
import math, random
from PIL import Image, ImageDraw, ImageFilter
SW, SH, K = 1080, 780, 2

def _grad(d, w, h, top, bot):
    for y in range(h):
        t = y / h; d.line((0, y, w, y), fill=tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3)))

def _mount(d, pts, col, snow=None):
    d.polygon(pts, fill=col)

def _pine(d, x, y, s, col=(24, 70, 62), snow=(245, 248, 252)):
    for i in range(4):
        w = s * (1 - i * 0.2); yy = y - i * s * 0.55
        d.polygon([(x - w / 2, yy), (x + w / 2, yy), (x, yy - s * 0.8)], fill=col)
        d.polygon([(x - w * 0.3, yy - s * 0.35), (x + w * 0.3, yy - s * 0.35), (x, yy - s * 0.8)], fill=snow)
    d.rectangle((x - s * 0.05, y, x + s * 0.05, y + s * 0.25), fill=(70, 50, 40))

def winter():
    w, h = SW * K, SH * K; im = Image.new("RGB", (w, h)); d = ImageDraw.Draw(im)
    _grad(d, w, h, (255, 190, 140), (150, 190, 235))
    d.ellipse((w * .68, h * .12, w * .68 + 220, h * .12 + 220), fill=(255, 236, 190))
    _mount(d, [(0, h * .62), (w * .22, h * .30), (w * .45, h * .58), (w * .7, h * .24), (w, h * .6), (w, h), (0, h)], (205, 220, 240))
    _mount(d, [(0, h * .75), (w * .3, h * .48), (w * .6, h * .72), (w * .85, h * .5), (w, h * .7), (w, h), (0, h)], (235, 242, 250))
    _mount(d, [(0, h * .9), (w * .4, h * .66), (w, h * .86), (w, h), (0, h)], (255, 255, 255))
    random.seed(4)
    for x in range(40, w, 150):
        _pine(d, x + random.randint(-20, 20), h * (0.80 + random.random() * .12), 150 + random.randint(0, 60))
    # lift cable + chairs
    d.line((0, h * .12, w, h * .38), fill=(40, 40, 50), width=5)
    for fx in (.22, .5, .78):
        x = w * fx; y = h * .12 + (h * .26) * fx
        d.line((x, y, x, y + 70), fill=(40, 40, 50), width=4); d.rounded_rectangle((x - 34, y + 70, x + 34, y + 104), radius=8, fill=(215, 40, 55))
    # skier
    sx, sy = w * .56, h * .86
    d.line((sx - 60, sy + 70, sx + 70, sy + 56), fill=(30, 30, 40), width=7); d.polygon([(sx - 14, sy - 50), (sx + 20, sy - 50), (sx + 30, sy + 30), (sx - 6, sy + 36)], fill=(215, 40, 55))
    d.ellipse((sx - 8, sy - 86, sx + 24, sy - 54), fill=(245, 205, 170)); d.line((sx + 20, sy - 30, sx + 70, sy + 20), fill=(30, 30, 40), width=5)
    return im.resize((SW, SH), Image.LANCZOS)

def food():
    w, h = SW * K, SH * K; im = Image.new("RGB", (w, h), (116, 72, 44)); d = ImageDraw.Draw(im)
    for y in range(0, h, 60): d.line((0, y, w, y + 8), fill=(104, 63, 38), width=4)
    def plate(cx, cy, r, fill, rim=(250, 250, 248)):
        d.ellipse((cx - r - 14, cy - r - 8, cx + r + 22, cy + r + 24), fill=(80, 48, 30))
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=rim); d.ellipse((cx - r * .8, cy - r * .8, cx + r * .8, cy + r * .8), fill=fill)
    random.seed(7)
    cx, cy = w * .30, h * .55; plate(cx, cy, 260, (244, 232, 196))   # hummus
    d.ellipse((cx - 150, cy - 150, cx + 150, cy + 150), outline=(232, 196, 90), width=16); d.ellipse((cx - 70, cy - 70, cx + 70, cy + 70), fill=(238, 222, 176))
    for _ in range(40): a = random.random() * 6.28; rr = random.random() * 200; d.ellipse((cx + math.cos(a) * rr, cy + math.sin(a) * rr, cx + math.cos(a) * rr + 12, cy + math.sin(a) * rr + 12), fill=(190, 70, 40))
    cx, cy = w * .72, h * .45; plate(cx, cy, 230, (90, 150, 70))   # tabbouleh
    for _ in range(420):
        a = random.random() * 6.28; rr = random.random() * 190; x = cx + math.cos(a) * rr; y = cy + math.sin(a) * rr
        d.ellipse((x, y, x + 14, y + 10), fill=random.choice([(60, 120, 50), (120, 180, 80), (200, 50, 40), (240, 235, 200)]))
    cx, cy = w * .52, h * .84; d.ellipse((cx - 300, cy - 150, cx + 300, cy + 150), fill=(205, 160, 100)); d.ellipse((cx - 250, cy - 110, cx + 250, cy + 110), fill=(228, 190, 130))
    for i in range(3): d.arc((cx - 250 + i * 60, cy - 110, cx + 250 - i * 60, cy + 110), 200, 340, fill=(190, 140, 80), width=8)
    cx, cy = w * .90, h * .80; d.ellipse((cx - 150, cy - 150, cx + 150, cy + 150), fill=(240, 240, 240)); d.ellipse((cx - 100, cy - 100, cx + 100, cy + 100), fill=(190, 80, 30)); d.ellipse((cx - 85, cy - 85, cx + 85, cy + 85), fill=(150, 50, 20))
    d.ellipse((cx - 60, cy - 70, cx - 20, cy - 40), fill=(220, 150, 90))
    return im.resize((SW, SH), Image.LANCZOS).filter(ImageFilter.GaussianBlur(0.4))

def landmark():
    w, h = SW * K, SH * K; im = Image.new("RGB", (w, h)); d = ImageDraw.Draw(im)
    _grad(d, w, h, (120, 160, 220), (255, 210, 170))
    _mount(d, [(0, h * .6), (w * .25, h * .35), (w * .5, h * .6), (w * .8, h * .3), (w, h * .55), (w, h), (0, h)], (150, 170, 205))
    _mount(d, [(0, h * .78), (w * .35, h * .55), (w, h * .8), (w, h), (0, h)], (96, 130, 100))
    # rock arch (natural bridge)
    d.polygon([(w * .12, h), (w * .18, h * .42), (w * .38, h * .30), (w * .62, h * .30), (w * .82, h * .42), (w * .88, h)], fill=(150, 118, 92))
    d.ellipse((w * .30, h * .42, w * .70, h * 1.15), fill=(255, 205, 165))
    d.polygon([(w * .12, h), (w * .24, h * .6), (w * .30, h * .65), (w * .30, h)], fill=(120, 92, 72)); d.polygon([(w * .88, h), (w * .76, h * .6), (w * .70, h * .65), (w * .70, h)], fill=(120, 92, 72))
    for i in range(14): y = h * (.34 + i * .035); d.line((w * (.20 + i * .005), y, w * (.80 - i * .005), y + 6), fill=(128, 100, 78), width=4)
    # roman columns
    for k in range(4):
        x = w * (.80 + k * .045); d.rectangle((x, h * .58, x + 28, h * .84), fill=(236, 224, 200)); d.rectangle((x - 8, h * .56, x + 36, h * .585), fill=(220, 206, 180))
    random.seed(3)
    for x in range(30, w, 170): _pine(d, x + random.randint(-20, 20), h * (.90 + random.random() * .05), 170, col=(30, 84, 70), snow=(60, 110, 90))
    return im.resize((SW, SH), Image.LANCZOS)
