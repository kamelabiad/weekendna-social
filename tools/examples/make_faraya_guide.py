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

def list_slide(photo, out, num, total, tag, title, title_ar, items, note, cy=0.5, kicker=None):
    """Bold guide slide: Faraya mood backdrop (blurred, dark; NOT presented as the venue), big hook, numbered red badges, glass cards.
    items = [(cat, name, line)]. Put a real photo of a place in reels/public/photos/guide/<slug>.webp (permission required) to show it on the card."""
    bg = cover(photo, W, H, cy=cy).filter(ImageFilter.GaussianBlur(14))
    bg = Image.blend(bg, Image.new("RGB", (W, H), (10, 9, 12)), 0.66).convert("RGBA")
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    n = len(items); y0 = 520; gap = 14; ch = int((1250 - y0 - gap * (n - 1)) / n); y = y0
    for cat, name, line in items:
        od.rounded_rectangle((M, y, W - M, y + ch), radius=30, fill=(255, 255, 255, 34), outline=(255, 255, 255, 60), width=2); y += ch + gap
    img = Image.alpha_composite(bg, ov).convert("RGB"); d = ImageDraw.Draw(img); logo(d, M, 64)
    t = f"{num}/{total}"; d.text((W - M - d.textlength(t, font=jak(700, 32)), 70), t, font=jak(700, 32), fill=(215, 215, 215))
    pill(d, M, 150, tag.upper(), jak(800, 26))
    d.text((M, 215), title, font=fit(d, title, W - 2 * M, 800, 84, 50), fill=WHITE)
    if kicker: d.text((M, 318), kicker, font=fit(d, kicker, W - 2 * M, 700, 40, 26), fill=RED)
    rtext(d, W - M, 395, title_ar, arfit(d, title_ar, W - 2 * M, 700, 44), (240, 240, 240))
    y = y0
    for i, (cat, name, line) in enumerate(items, 1):
        cx_, cy_ = M + 62, y + ch // 2
        d.ellipse((cx_ - 40, cy_ - 40, cx_ + 40, cy_ + 40), fill=RED)
        nf = jak(800, 44); nw = d.textlength(str(i), font=nf); bb = nf.getbbox(str(i)); d.text((cx_ - nw / 2, cy_ - (bb[3] - bb[1]) / 2 - bb[1]), str(i), font=nf, fill=WHITE)
        x = M + 130
        d.text((x, y + 16), cat.upper(), font=jak(700, 21), fill=(255, 140, 150))
        d.text((x, y + 38), name, font=fit(d, name, W - M - x - 24, 800, 40, 28), fill=WHITE)
        d.text((x, y + ch - 38), line, font=fit(d, line, W - M - x - 24, 500, 25, 18), fill=(225, 225, 225)); y += ch + gap
    d.text((M, 1275), note, font=fit(d, note, W - 2 * M, 500, 23, 18), fill=(200, 200, 200))
    img.save(out, quality=92)

# Photos of the listed places: put them in reels/public/photos/guide/<slug>.webp (permission required) and pass P("guide/<slug>") instead of None.
list_slide(P("acampar/42-01"), f"{O}/guide-4.jpg", 3, 5, "Where to eat", "Hungry in Faraya?", "جوعان بفاريا؟ جرّب هالأماكن الخمسة",
    [("Lebanese", "Jnaynit al Khaweja", "A garden-style stop for mezze and a long mountain meal"),
     ("Lebanese", "Em Sherif Deli", "Lebanese classics in a relaxed, casual setting"),
     ("Italian", "Mario e Mario", "Pizza and pasta"),
     ("Grill & seafood", "Meat the Fish", "Grilled meat and seafood for a hearty lunch or dinner"),
     ("Coffee", "LTTL BEAN", "A warm drink and something sweet")],
    "Check opening hours and seasonal availability before visiting.", kicker="5 spots to try this weekend")
list_slide(P("acampar/42-01"), f"{O}/guide-5.jpg", 4, 5, "What to do", "Don't just sleep", "لا تنام وبس: عيشها",
    [("Winter", "Ski and snowboard", "Mzaar Kfardebian, when the snow and slopes are open"),
     ("Winter", "Snowmobile rides", "With a local operator, when conditions allow"),
     ("Summer", "Hiking and mountain walks", "Highland trails and cooler mountain air"),
     ("All seasons", "Scenic outings", "Viewpoints, photos and relaxed mountain drives")],
    "Availability depends on weather, season and local operators.", kicker="Snow, speed and slow mountain days")
list_slide(P("acampar/42-01"), f"{O}/guide-6.jpg", 5, 5, "Places to visit", "4 places not to skip", "٤ أماكن ما تفوّتهن",
    [("Nature", "Chabrouh Dam", "A mountain reservoir and scenic spot for photos and a walk"),
     ("History", "Faqra Roman Ruins", "Ancient stone remains in a mountain setting"),
     ("Landmark", "Faqra Natural Bridge", "A dramatic natural rock bridge in the highlands"),
     ("Viewpoint", "Saint Charbel Statue", "A hilltop landmark with wide views over the mountains")],
    "Check opening times before you go.", kicker="Easy to add to your weekend")
last(f"{O}/guide-7.jpg", None, "Plan your Faraya weekend", "خطّطوا ويكندكن بفاريا", main="save", head=("Your Faraya", "weekend starts here"))
story(P("acampar/42-02"), f"{O}/story.jpg", "A weekend", "in Faraya", "Stays, sights and a simple plan", "ويكند بفاريا", main="save")
print("ok")
