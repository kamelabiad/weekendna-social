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
place_slide(P("acampar/42-04"), f"{O}/guide-2.jpg", 1, 4, "Acampar Faraya", "Stay · Faraya · 45 min from Beirut",
            ["Wooden bungalows, most with a fireplace", "Mountain views and a terrace", "For 2 to 6 guests"], "From $80 a night", "بنغلوهات خشب مع شومينيه")
place_slide(P("fvc/26-01"), f"{O}/guide-3.jpg", 2, 4, "Faraya Village Club", "Stay · Mzaar · 45 min from Beirut",
            ["A chimney in every chalet", "A heated pool on site", "From a studio for 2 to a chalet for 7"], "From $150 a night", "شاليهات مع شومينيه ومسبح مدفّأ")
place_slide(P("acampar/42-01"), f"{O}/guide-4.jpg", 3, 4, "Explore nearby", "Faqra · Faraya",
            ["Faqra Natural Bridge, a 38 m rock bridge", "Qalaat Faqra, Roman ruins and a 15 m tower", "Chabrouh Dam, above Faraya village"], "Check opening times before you go", "جسر فقرا الطبيعي، قلعة فقرا وسد شبروح")
place_slide(P("acampar/42-05"), f"{O}/guide-5.jpg", 4, 4, "Your Faraya weekend", "Plan it in 3 steps",
            ["Sat: a Faqra walk, then a fireplace evening", "Sun: Chabrouh Dam, then the drive back", "Winter roads: check the weather and bring warm layers"], "Snow depends on the weather", "السبت والأحد بفاريا")
last(f"{O}/guide-6.jpg", None, "Plan your Faraya weekend", "خطّطوا ويكندكن بفاريا", main="save", head=("Your Faraya", "weekend starts here"))
story(P("acampar/42-02"), f"{O}/story.jpg", "A weekend", "in Faraya", "Stays, sights and a simple plan", "ويكند بفاريا", main="save")
print("ok")
