"""Majestic Byblos v2 (30 Oct 2026): Weekendna-as-hero redesign of slide 1, slide 3 and the story. Slide 2 unchanged.
Usage: python3 tools/examples/make_majestic_v2.py <balcony-photo 23-03.webp> <post-folder>"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from brand import *
photo, POST = sys.argv[1], sys.argv[2]
ph = Image.open(photo).convert("RGB")
DARKB = (12, 12, 14)

def big_button(d, cx, y, t, f, h, bg, fg, pad=60):
    bw = d.textlength(t, font=f)
    d.rounded_rectangle((cx - bw / 2 - pad, y, cx + bw / 2 + pad, y + h), radius=h // 2, fill=bg)
    bb = f.getbbox(t); d.text((cx - bw / 2, y + (h - (bb[3] - bb[1])) / 2 - bb[1]), t, font=f, fill=fg)

# ---------- Slide 1: benefit hook + Found on Weekendna ----------
img = cover(ph, W, H, cx=0.58, cy=0.5).filter(ImageFilter.UnsharpMask(radius=1.4, percent=50, threshold=2))
img = shade(img, 500, alpha=245, k=1.25); d = ImageDraw.Draw(img)
logo(d, M, 64)
pill(d, M, 168, "Found on Weekendna", jak(800, 46), pad=(32, 18))
d.text((M, 892), "Your Byblos weekend,", font=jak(800, 78), fill=WHITE)
d.text((M, 984), "found for you", font=jak(800, 78), fill=WHITE)
d.text((M, 1100), "Private balcony · sea or city views · from $130", font=jak(600, 34), fill=WHITE)
rtext(d, W - M, 1160, "لقينالك ويكند بجبيل", ar(700, 44), WHITE)
d.text((M, 1262), "Majestic Byblos Grand Hotel · Jbeil", font=jak(500, 28), fill=(215, 215, 215))
sw = d.textlength("Swipe", font=jak(700, 30)); d.text((W - M - sw - 34, 1260), "Swipe", font=jak(700, 30), fill=WHITE)
cx0 = W - M - 20; d.line([(cx0, 1268), (cx0 + 12, 1280), (cx0, 1292)], fill=WHITE, width=5, joint="curve")
img.save(f"{POST}/majestic-1.jpg", quality=92)

# ---------- Slide 3: strong follow + next step ----------
img = Image.new("RGB", (W, H), RED); d = ImageDraw.Draw(img); logo(d, M, 64, accent=INK)
pt = "Found on Weekendna"; pf = jak(700, 30); pw = d.textlength(pt, font=pf)
pill(d, int((W - pw) / 2 - 22), 180, pt, pf, fg=RED, bg=WHITE)
ctext(d, 270, "Your Byblos", jak(800, 92), WHITE); ctext(d, 375, "weekend starts here", jak(800, 72), WHITE)
ctext(d, 480, "Sea views + private balcony, from $130", jak(500, 34), WHITE)
ctext(d, 536, "ويكندكن بجبيل بيبلش من هون", ar(700, 38), WHITE, rtl=True)
d.rounded_rectangle((90, 625, W - 90, 895), radius=36, fill=WHITE)
ctext(d, 650, "Want this place?", jak(800, 44), RED)
ctext(d, 725, "Comment BYBLOS and we'll", jak(800, 44), INK)
ctext(d, 778, "check availability for you", jak(800, 44), INK)
ctext(d, 842, "بدك هالمكان؟ اكتبلنا بالتعليق وبنتأكدلك", ar(600, 28), (90, 90, 90), rtl=True)
big_button(d, W / 2, 940, "Follow @weekendna.lb", jak(800, 52), 118, INK, WHITE)
ctext(d, 1085, "New places every week", jak(800, 54), WHITE)
ctext(d, 1160, "تابعونا، كل أسبوع محل جديد", ar(700, 36), WHITE, rtl=True)
ctext(d, 1265, "Request your dates on WhatsApp · nothing to pay yet · link in bio", jak(500, 25), (255, 228, 230))
img.save(f"{POST}/majestic-3.jpg", quality=92)

# ---------- Story 1080x1920 ----------
SW, SH = 1080, 1920
bg = cover(ph, SW, SH).filter(ImageFilter.GaussianBlur(40)); img = Image.blend(bg, Image.new("RGB", (SW, SH), DARKB), 0.55)
d = ImageDraw.Draw(img); logo(d, 72, 110, size=56)
pt = "Found on Weekendna"; pf = jak(700, 34); pw = d.textlength(pt, font=pf)
pill(d, int((SW - pw) / 2 - 24), 215, pt, pf)
fw, fh = 900, 760
card = cover(ph, fw, fh, cx=0.6).filter(ImageFilter.UnsharpMask(radius=1.2, percent=50, threshold=2))
m = Image.new("L", (fw, fh), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, fw, fh), radius=36, fill=255)
img.paste(card, (90, 310), m); d = ImageDraw.Draw(img)
def sc(y, t, f, fill, rtl=False):
    w = d.textlength(t, font=f, direction="rtl" if rtl else None); d.text(((SW - w) / 2, y), t, font=f, fill=fill, direction="rtl" if rtl else None)
sc(1110, "Your Byblos weekend,", jak(800, 68), WHITE); sc(1195, "found for you", jak(800, 68), WHITE)
sc(1292, "Private balcony · sea or city views · from $130", jak(500, 32), WHITE)
sc(1346, "لقينالك ويكند بجبيل", ar(700, 42), WHITE, rtl=True)
d.rounded_rectangle((90, 1425, SW - 90, 1560), radius=32, fill=WHITE)
sc(1443, "Want this place?", jak(800, 38), RED); sc(1505, "Reply BYBLOS for availability", jak(700, 33), INK)
big_button(d, SW / 2, 1595, "Follow @weekendna.lb", jak(800, 48), 112, RED, WHITE)
sc(1730, "New places every week", jak(700, 34), WHITE); sc(1785, "تابعونا، كل أسبوع محل جديد", ar(600, 32), WHITE, rtl=True)
sc(1850, "weekendna.com · link in bio", jak(500, 30), (225, 225, 225))
img.save(f"{POST}/story.jpg", quality=92)
print("ok")
