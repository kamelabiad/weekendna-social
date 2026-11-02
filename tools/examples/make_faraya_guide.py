"""City Guide #1: A weekend in Faraya (Wed 18 Nov 2026). Photos: Weekendna listing photos only (reels/public/photos/acampar, fvc).
Sights come from a primary/visitor source listed in posts/2026-11-faraya-guide/sources.txt. Food slide is OMITTED until places are
verified by 2 independent sources dated within 12 months (PLAYBOOK "CITY GUIDES"). Run `source tools/setup.sh` first."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from hero import *
ROOT = os.path.join(os.path.dirname(__file__), "..", ".."); O = f"{ROOT}/posts/2026-11-faraya-guide"; os.makedirs(O, exist_ok=True)
P = lambda f: Image.open(f"{ROOT}/reels/public/photos/{f}.webp").convert("RGB")

import os as _os
def _icon(d, kind, cx, cy, r=46, col=(26, 24, 28)):
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=WHITE)
    if kind == "eat":
        for k in (-14, -5, 4):
            d.line((cx + k - 8, cy - 26, cx + k - 8, cy - 4), fill=col, width=4)
        d.line((cx - 18, cy - 4, cx - 18, cy + 26), fill=col, width=6); d.line((cx - 14, cy - 26, cx - 14, cy - 2), fill=col, width=4)
        d.polygon([(cx + 14, cy - 28), (cx + 26, cy - 28), (cx + 26, cy + 4), (cx + 14, cy + 4)], fill=col); d.line((cx + 20, cy + 4, cx + 20, cy + 28), fill=col, width=6)
    elif kind == "do":
        for ang in range(0, 180, 30):
            import math
            dx, dy = math.cos(math.radians(ang)) * 28, math.sin(math.radians(ang)) * 28
            d.line((cx - dx, cy - dy, cx + dx, cy + dy), fill=col, width=5)
    elif kind == "see":
        d.polygon([(cx - 28, cy - 14), (cx, cy - 30), (cx + 28, cy - 14)], fill=col)
        for k in (-20, -7, 6, 19): d.rectangle((cx + k - 3, cy - 10, cx + k + 3, cy + 18), fill=col)
        d.rectangle((cx - 30, cy + 20, cx + 30, cy + 27), fill=col)
    else:  # stay
        d.rectangle((cx - 30, cy + 2, cx + 30, cy + 14), fill=col); d.rectangle((cx - 30, cy - 22, cx - 24, cy + 22), fill=col)
        d.rounded_rectangle((cx - 20, cy - 10, cx - 2, cy + 2), radius=4, fill=col); d.rectangle((cx - 2, cy - 10, cx + 28, cy + 2), fill=col)

def photo_slide(photo, out, num, total, kind, title, sub, place, items, foot=None, cy=0.5, cx=0.5):
    """Big-photo guide slide (Kamel's layout, 2 Nov 2026): photo top, round icon, title, one line, location pin, rows. items = [(name, desc)].
    photo: a REAL photo of the place(s). Real place photos go in reels/public/photos/guide/<slug>.webp; until then the caller passes the Faraya winter image."""
    PH = 780
    img = Image.new("RGB", (W, H), (22, 20, 25))
    ph = cover(photo, W, PH, cx=cx, cy=cy).filter(ImageFilter.UnsharpMask(radius=1.4, percent=60, threshold=2)).convert("RGBA")
    ov = Image.new("RGBA", (W, PH), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    for y in range(PH):
        a = int(150 * max(0, 1 - y / 220)) + int(255 * max(0, (y - (PH - 420)) / 420) ** 1.2)
        od.line((0, y, W, y), fill=(22, 20, 25, min(255, a)))
    img.paste(Image.alpha_composite(ph, ov).convert("RGB"), (0, 0)); d = ImageDraw.Draw(img); logo(d, M, 64)
    t = f"{num}/{total}"; tf = jak(700, 30); tw = d.textlength(t, font=tf)
    d.rounded_rectangle((W - M - tw - 40, 52, W - M, 108), radius=28, fill=(0, 0, 0)); d.text((W - M - tw - 20, 62), t, font=tf, fill=WHITE)
    _icon(d, kind, M + 52, 640)
    d.text((M + 130, 590), title, font=fit(d, title, W - 2 * M - 130, 800, 72, 40), fill=WHITE)
    d.text((M + 130, 678), sub, font=fit(d, sub, W - 2 * M - 130, 500, 30, 20), fill=(225, 225, 225))
    pill(d, M, 800, place, jak(700, 24), bg=(46, 43, 50))
    n = len(items); y = 870; rh = min(98, int((1265 - y) / n)); 
    for name, desc in items:
        d.ellipse((M, y + 14, M + 18, y + 32), fill=RED)
        d.text((M + 36, y), name, font=fit(d, name, W - 2 * M - 40, 800, 38, 26), fill=WHITE)
        if desc: d.text((M + 36, y + 46), desc, font=fit(d, desc, W - 2 * M - 40, 500, 26, 18), fill=(205, 205, 205))
        y += rh
    if foot: d.text((M, 1285), foot, font=fit(d, foot, W - 2 * M, 700, 28, 20), fill=RED)
    img.save(out, quality=92)

import guide_scenes as GS, tempfile, subprocess
_T = tempfile.mkdtemp(); subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), "..", "guide_scenes.py"), _T], check=True, capture_output=True)
SC = lambda n: Image.open(f"{_T}/{n}.png").convert("RGB")
SNOW = P("acampar/42-01")  # Faraya winter image (Acampar), used until real photos of the sights/food exist
slide1(SC("winter"), f"{O}/guide-1.jpg", "A weekend in Faraya", "Stay · Eat · Do · Explore", "Snow, fireplaces and mountain views, 45 min from Beirut",
       "", "Faraya · Faqra · Mzaar")
photo_slide(P("acampar/42-04"), f"{O}/guide-2.jpg", 1, 5, "stay", "Where to stay", "Acampar Faraya, 45 min from Beirut", "Faraya",
            [("Wooden bungalows, most with a fireplace", ""), ("Mountain views and a terrace", ""), ("For 2 to 6 guests", "")], "From $80 a night", cy=0.55)
photo_slide(P("fvc/26-01"), f"{O}/guide-3.jpg", 2, 5, "stay", "Where to stay", "Faraya Village Club, Mzaar", "Mzaar",
            [("A chimney in every chalet", ""), ("A heated pool on site", ""), ("From a studio for 2 to a chalet for 7", "")], "From $150 a night")
photo_slide(SC("food"), f"{O}/guide-4.jpg", 3, 5, "eat", "Food and drinks", "From mezze to pizza and coffee", "Faraya",
            [("Jnaynit al Khaweja", "Garden-style Lebanese, mezze and a long mountain meal"), ("Em Sherif Deli", "Lebanese classics in a relaxed, casual setting"),
             ("Mario e Mario", "Pizza and pasta"), ("Meat the Fish", "Grilled meat and seafood for lunch or dinner"), ("LTTL BEAN", "A warm drink and something sweet")],
            "Check opening hours before you go", cy=0.5)
photo_slide(SC("ski"), f"{O}/guide-5.jpg", 4, 5, "do", "Activities", "Snow, speed and slow mountain days", "Mzaar and Faraya",
            [("Ski and snowboard", "Mzaar Kfardebian, when the snow and slopes are open"), ("Snowmobile rides", "With a local operator, when conditions allow"),
             ("Hiking and mountain walks", "Highland trails and cooler mountain air"), ("Scenic outings", "Viewpoints, photos and relaxed mountain drives")],
            "Depends on weather, season and operators", cy=0.5)
photo_slide(SC("village"), f"{O}/guide-6.jpg", 5, 5, "see", "Places to visit", "Four easy additions to your weekend", "Faqra and Faraya",
            [("Chabrouh Dam", "A mountain reservoir and scenic spot for a walk"), ("Faqra Roman Ruins", "Ancient stone remains in a mountain setting"),
             ("Faqra Natural Bridge", "A dramatic natural rock bridge"), ("Saint Charbel Statue", "A hilltop landmark with wide mountain views")],
            "Check opening times before you go", cy=0.5)
last(f"{O}/guide-7.jpg", None, "Plan your Faraya weekend", "", main="save", head=("Your Faraya", "weekend starts here"))
story(SC("winter"), f"{O}/story.jpg", "A weekend", "in Faraya", "Stays, food, activities and places to visit", "", main="save")
print("ok")
