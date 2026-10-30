"""Weekendna-as-hero design pieces (Kamel approved the Majestic Byblos version, 30 Oct 2026).
Same layout as tools/examples/make_majestic_v2.py, as functions, so every post uses the identical design:
  slide1(...)  benefit hook + big red "Found on Weekendna" badge high under the logo, place name small
  last(...)    "Your <place> weekend starts here" + benefit + white main-action card + dark Follow button + "New places every week"
  story(...)   9:16: framed photo, badge, short white box, large red Follow button, "New places every week"
main= "comment" (Comment <KEYWORD> and we'll check availability) or "save" (Save this for your next weekend; non-collab posts only).
Arabic strings must not contain Latin letters. Run `source tools/setup.sh` first."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from brand import *
DARKB = (12, 12, 14)
GREY = (215, 215, 215)

def big_button(d, cx, y, t, f, h, bg, fg, pad=60):
    bw = d.textlength(t, font=f)
    d.rounded_rectangle((cx - bw / 2 - pad, y, cx + bw / 2 + pad, y + h), radius=h // 2, fill=bg)
    bb = f.getbbox(t); d.text((cx - bw / 2, y + (h - (bb[3] - bb[1])) / 2 - bb[1]), t, font=f, fill=fg)

def fit(d, t, w, weight, size, minsize=26):
    while size > minsize and d.textlength(t, font=jak(weight, size)) > w: size -= 2
    return jak(weight, size)

def arfit(d, t, w, weight, size, minsize=24):
    while size > minsize and d.textlength(t, font=ar(weight, size), direction="rtl") > w: size -= 2
    return ar(weight, size)

def _bg(photo, w, h, cx, cy, framed):
    if not framed:
        return cover(photo, w, h, cx=cx, cy=cy).filter(ImageFilter.UnsharpMask(radius=1.4, percent=50, threshold=2))
    bg = cover(photo, w, h).filter(ImageFilter.GaussianBlur(40)); bg = Image.blend(bg, Image.new("RGB", (w, h), DARKB), 0.45)
    fw = w - 2 * M; fh = 590
    card = cover(photo, fw, fh, cx=cx, cy=cy).filter(ImageFilter.UnsharpMask(radius=1.2, percent=60, threshold=2))
    m = Image.new("L", (fw, fh), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, fw, fh), radius=36, fill=255)
    bg.paste(card, (M, 260), m); return bg

def slide1(photo, out, line1, line2, sub, ar_line, small, badge="Found on Weekendna", cx=0.5, cy=0.5, framed=False, swipe=True):
    img = _bg(photo, W, H, cx, cy, framed)
    img = shade(img, 500, alpha=245, k=1.25); d = ImageDraw.Draw(img)
    logo(d, M, 64)
    pill(d, M, 168, badge, jak(800, 46), pad=(32, 18))
    f = fit(d, max(line1, line2, key=len), W - 2 * M, 800, 78)
    d.text((M, 892), line1, font=f, fill=WHITE)
    d.text((M, 984), line2, font=f, fill=WHITE)
    d.text((M, 1100), sub, font=fit(d, sub, W - 2 * M, 600, 34), fill=WHITE)
    rtext(d, W - M, 1160, ar_line, arfit(d, ar_line, W - 2 * M, 700, 44), WHITE)
    d.text((M, 1262), small, font=fit(d, small, W - 2 * M - 200, 500, 28, 20), fill=GREY)
    if swipe:
        sw = d.textlength("Swipe", font=jak(700, 30)); d.text((W - M - sw - 34, 1260), "Swipe", font=jak(700, 30), fill=WHITE)
        c0 = W - M - 20; d.line([(c0, 1268), (c0 + 12, 1280), (c0, 1292)], fill=WHITE, width=5, joint="curve")
    img.convert("RGB").save(out, quality=92)

def last(out, place, benefit, benefit_ar, kw=None, main="comment", head=None):
    """head: optional (line1, line2) instead of ("Your <place>", "weekend starts here")."""
    img = Image.new("RGB", (W, H), RED); d = ImageDraw.Draw(img); logo(d, M, 64, accent=INK)
    pt = "Found on Weekendna"; pf = jak(700, 30); pw = d.textlength(pt, font=pf)
    pill(d, int((W - pw) / 2 - 22), 180, pt, pf, fg=RED, bg=WHITE)
    h1, h2 = head or (f"Your {place}", "weekend starts here")
    ctext(d, 270, h1, fit(d, h1, W - 2 * M, 800, 92), WHITE); ctext(d, 375, h2, fit(d, h2, W - 2 * M, 800, 72), WHITE)
    ctext(d, 480, benefit, fit(d, benefit, W - 2 * M, 500, 34), WHITE)
    ctext(d, 536, benefit_ar, arfit(d, benefit_ar, W - 2 * M, 700, 38), WHITE, rtl=True)
    d.rounded_rectangle((90, 625, W - 90, 895), radius=36, fill=WHITE)
    if main == "save":
        ctext(d, 650, "Don't lose this one", jak(800, 44), RED)
        ctext(d, 725, "Save this for your", jak(800, 44), INK)
        ctext(d, 778, "next weekend", jak(800, 44), INK)
        ctext(d, 842, "احفظوها لويكندكن الجاي", ar(600, 28), (90, 90, 90), rtl=True)
    else:
        ctext(d, 650, "Want this place?", jak(800, 44), RED)
        ctext(d, 725, f"Comment {kw} and we'll", jak(800, 44), INK)
        ctext(d, 778, "check availability for you", jak(800, 44), INK)
        ctext(d, 842, "بدك هالمكان؟ اكتبلنا بالتعليق وبنتأكدلك", ar(600, 28), (90, 90, 90), rtl=True)
    big_button(d, W / 2, 940, "Follow @weekendna.lb", jak(800, 52), 118, INK, WHITE)
    ctext(d, 1085, "New places every week", jak(800, 54), WHITE)
    ctext(d, 1160, "تابعونا، كل أسبوع محل جديد", ar(700, 36), WHITE, rtl=True)
    ctext(d, 1265, "Request your dates on WhatsApp · nothing to pay yet · link in bio", jak(500, 25), (255, 228, 230))
    img.save(out, quality=92)

def story(photo, out, line1, line2, sub, ar_line, kw=None, cx=0.5, cy=0.5, main="comment", badge="Found on Weekendna", box=None):
    """box: optional (red line, ink line) for the white box, e.g. ("Sea or mountain?", "Reply SEA or MOUNTAIN")."""
    SW, SH = 1080, 1920
    bg = cover(photo, SW, SH).filter(ImageFilter.GaussianBlur(40)); img = Image.blend(bg, Image.new("RGB", (SW, SH), DARKB), 0.55)
    d = ImageDraw.Draw(img); logo(d, 72, 110, size=56)
    pf = jak(700, 34); pw = d.textlength(badge, font=pf)
    pill(d, int((SW - pw) / 2 - 24), 215, badge, pf)
    fw, fh = 900, 760
    card = cover(photo, fw, fh, cx=cx, cy=cy).filter(ImageFilter.UnsharpMask(radius=1.2, percent=50, threshold=2))
    m = Image.new("L", (fw, fh), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, fw, fh), radius=36, fill=255)
    img.paste(card, (90, 310), m); d = ImageDraw.Draw(img)
    def sc(y, t, f, fill, rtl=False):
        w = d.textlength(t, font=f, direction="rtl" if rtl else None); d.text(((SW - w) / 2, y), t, font=f, fill=fill, direction="rtl" if rtl else None)
    f = fit(d, max(line1, line2, key=len), SW - 120, 800, 68)
    sc(1110, line1, f, WHITE); sc(1195, line2, f, WHITE)
    sc(1292, sub, fit(d, sub, SW - 120, 500, 32), WHITE)
    sc(1346, ar_line, arfit(d, ar_line, SW - 120, 700, 42), WHITE, rtl=True)
    d.rounded_rectangle((90, 1425, SW - 90, 1560), radius=32, fill=WHITE)
    if box: a, b = box
    elif main == "save": a, b = "Don't lose this one", "Save it for your next weekend"
    else: a, b = "Want this place?", f"Reply {kw} for availability"
    sc(1443, a, jak(800, 38), RED); sc(1505, b, fit(d, b, SW - 240, 700, 33), INK)
    big_button(d, SW / 2, 1595, "Follow @weekendna.lb", jak(800, 48), 112, RED, WHITE)
    sc(1730, "New places every week", jak(700, 34), WHITE); sc(1785, "تابعونا، كل أسبوع محل جديد", ar(600, 32), WHITE, rtl=True)
    sc(1850, "weekendna.com · link in bio", jak(500, 30), (225, 225, 225))
    img.save(out, quality=92)

def unbar(photo, thr=18):
    """Crop black letterbox bars (some owners upload phone screenshots with bars)."""
    g = photo.convert("L").point(lambda v: 255 if v > thr else 0); bb = g.getbbox()
    return photo.crop(bb) if bb else photo

def place_slide(photo, out, num, total, name, where, facts, price, ar_line, cx=0.5, cy=0.5, tag=None):
    """Roundup / Drop slide: framed photo, number, place name, area pill, 3 facts, price, Arabic line. tag: optional red badge on the photo (e.g. "Confirmed Thursday")."""
    DARK = (26, 24, 28)
    img = Image.new("RGB", (W, H), DARK); d = ImageDraw.Draw(img); logo(d, M, 64)
    t = f"{num}/{total}"; d.text((W - M - d.textlength(t, font=jak(700, 32)), 70), t, font=jak(700, 32), fill=(200, 200, 200))
    pw, ph = W - 2 * M, 600
    p = cover(photo, pw, ph, cx=cx, cy=cy).filter(ImageFilter.UnsharpMask(radius=1.4, percent=70, threshold=2))
    m = Image.new("L", (pw, ph), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, pw, ph), radius=36, fill=255)
    img.paste(p, (M, 150), m); d = ImageDraw.Draw(img)
    if tag: pill(d, M + 24, 150 + 24, tag, jak(800, 34), pad=(26, 14))
    pill(d, M, 785, where.upper(), jak(700, 26))
    d.text((M, 850), name, font=fit(d, name, W - 2 * M, 800, 60), fill=WHITE)
    y = 945
    for f in facts:
        d.ellipse((M, y + 14, M + 14, y + 28), fill=RED); d.text((M + 32, y), f, font=fit(d, f, W - 2 * M - 40, 600, 34), fill=WHITE); y += 58
    d.text((M, y + 22), price, font=fit(d, price, W - 2 * M, 800, 44), fill=RED)
    rtext(d, W - M, 1265, ar_line, arfit(d, ar_line, W - 2 * M, 600, 34), (230, 230, 230))
    img.save(out, quality=92)
