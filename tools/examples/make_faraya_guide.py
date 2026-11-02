"""City Guide #1: A weekend in Faraya (Wed 18 Nov 2026). Photos: Weekendna listing photos only (reels/public/photos/acampar, fvc).
Sights come from a primary/visitor source listed in posts/2026-11-faraya-guide/sources.txt. Food slide is OMITTED until places are
verified by 2 independent sources dated within 12 months (PLAYBOOK "CITY GUIDES"). Run `source tools/setup.sh` first."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from hero import *
ROOT = os.path.join(os.path.dirname(__file__), "..", ".."); O = f"{ROOT}/posts/2026-11-faraya-guide"; os.makedirs(O, exist_ok=True)
P = lambda f: Image.open(f"{ROOT}/reels/public/photos/{f}.webp").convert("RGB")
slide1(P("acampar/42-02"), f"{O}/guide-1.jpg", "A weekend in Faraya", "Stay · Explore · Plan", "Fireplaces, mountain views and Roman ruins, 45 min from Beirut",
       "ويكند بفاريا: وين تقعد وشو تشوف", "Faraya · Faqra · Mzaar")
place_slide(P("acampar/42-04"), f"{O}/guide-2.jpg", 1, 5, "Where to stay", "Stay · Acampar Faraya · 45 min from Beirut",
            ["Wooden bungalows, most with a fireplace", "Mountain views and a terrace", "For 2 to 6 guests"], "From $80 a night", "بنغلوهات خشب مع شومينيه")
place_slide(P("fvc/26-01"), f"{O}/guide-3.jpg", 2, 5, "Where to stay", "Stay · Faraya Village Club · Mzaar",
            ["A chimney in every chalet", "A heated pool on site", "From a studio for 2 to a chalet for 7"], "From $150 a night", "شاليهات مع شومينيه ومسبح مدفّأ")

def list_slide(photo, out, num, total, tag, title, title_ar, items, note, cy=0.5):
    """Guide slide: photo strip, section pill, title, up to 5 cards (category, name, one line), note. items = [(cat, name, line)]"""
    DARK = (26, 24, 28); CARD = (14, 13, 16)
    img = Image.new("RGB", (W, H), DARK); d = ImageDraw.Draw(img); logo(d, M, 64)
    t = f"{num}/{total}"; d.text((W - M - d.textlength(t, font=jak(700, 32)), 70), t, font=jak(700, 32), fill=(200, 200, 200))
    pw, ph = W - 2 * M, 250
    p = cover(photo, pw, ph, cy=cy).filter(ImageFilter.UnsharpMask(radius=1.4, percent=70, threshold=2))
    m = Image.new("L", (pw, ph), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, pw, ph), radius=30, fill=255)
    img.paste(p, (M, 135), m); d = ImageDraw.Draw(img)
    pill(d, M, 410, tag.upper(), jak(700, 24))
    d.text((M, 458), title, font=fit(d, title, W - 2 * M - 260, 800, 54), fill=WHITE)
    rtext(d, W - M, 478, title_ar, arfit(d, title_ar, 250, 700, 32), (230, 230, 230))
    n = len(items); ch = 124 if n >= 5 else 150; gap = 10; y = 560 if n >= 5 else 575
    for cat, name, line in items:
        d.rounded_rectangle((M, y, W - M, y + ch), radius=24, fill=CARD)
        d.text((M + 28, y + 14), cat.upper(), font=jak(700, 20), fill=RED)
        d.text((M + 28, y + 36), name, font=fit(d, name, W - 2 * M - 56, 800, 34 if n >= 5 else 38), fill=WHITE)
        d.text((M + 28, y + ch - (36 if n >= 5 else 44)), line, font=fit(d, line, W - 2 * M - 56, 500, 24 if n >= 5 else 26, 20), fill=(205, 205, 205)); y += ch + gap
    d.text((M, y + 14), note, font=fit(d, note, W - 2 * M, 500, 24, 20), fill=(190, 190, 190))
    img.save(out, quality=92)

list_slide(P("acampar/42-05"), f"{O}/guide-4.jpg", 3, 5, "Where to eat", "Eat in Faraya", "وين تاكل بفاريا",
    [("Lebanese", "Jnaynit al Khaweja", "A garden-style stop for mezze and a long mountain meal"),
     ("Lebanese", "Em Sherif Deli", "Lebanese classics in a relaxed, casual setting"),
     ("Italian", "Mario e Mario", "Pizza and pasta"),
     ("Grill & seafood", "Meat the Fish", "Grilled meat and seafood for a hearty lunch or dinner"),
     ("Coffee", "LTTL BEAN", "A warm drink and something sweet")],
    "Check opening hours and seasonal availability before visiting.")
list_slide(P("acampar/42-01"), f"{O}/guide-5.jpg", 4, 5, "What to do", "Make it an adventure", "خليها مغامرة",
    [("Winter", "Ski and snowboard", "Mzaar Kfardebian, when the snow and slopes are open"),
     ("Winter", "Snowmobile rides", "With a local operator, when conditions allow"),
     ("Summer", "Hiking and mountain walks", "Highland trails and cooler mountain air"),
     ("All seasons", "Scenic outings", "Viewpoints, photos and relaxed mountain drives")],
    "Availability depends on weather, season and local operators.")
list_slide(P("acampar/42-04"), f"{O}/guide-6.jpg", 5, 5, "Places to visit", "Explore Faraya", "شو تزور بفاريا",
    [("Nature", "Chabrouh Dam", "A mountain reservoir and scenic spot for photos and a walk"),
     ("History", "Faqra Roman Ruins", "Ancient stone remains in a mountain setting"),
     ("Landmark", "Faqra Natural Bridge", "A dramatic natural rock bridge in the highlands"),
     ("Viewpoint", "Saint Charbel Statue", "A hilltop landmark with wide views over the mountains")],
    "Check opening times before you go.")
last(f"{O}/guide-7.jpg", None, "Plan your Faraya weekend", "خطّطوا ويكندكن بفاريا", main="save", head=("Your Faraya", "weekend starts here"))
story(P("acampar/42-02"), f"{O}/story.jpg", "A weekend", "in Faraya", "Stays, sights and a simple plan", "ويكند بفاريا", main="save")
print("ok")
