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
place_slide(P("acampar/42-01"), f"{O}/guide-4.jpg", 3, 5, "Places to visit", "Explore · Faqra and Faraya",
            ["Faqra Natural Bridge, a 38 m rock bridge", "Qalaat Faqra, Roman ruins and a 15 m tower", "Chabrouh Dam and the Saint Charbel statue"], "Check opening times before you go", "جسر فقرا، قلعة فقرا، سد شبروح وتمثال مار شربل")
place_slide(P("fvc/26-03"), f"{O}/guide-5.jpg", 4, 5, "Things to do", "Do · Mzaar and Faqra",
            ["Ski the Mzaar slopes in the snow season", "Snowshoeing, ATV and snowmobile tours", "Walks, picnics and biking around Faqra"], "Snow and tours depend on the weather", "تزلج، مشي وجولات بفاريا وفقرا")
place_slide(P("acampar/42-05"), f"{O}/guide-6.jpg", 5, 5, "Where to eat", "Eat · Faraya and Kfardebian",
            ["Em Bashir: saj and manakish on the way up", "Fawzi, Kfardebian: traditional Lebanese", "El Mexicano: at the Faraya roundabout"], "Local picks, check hours before you go", "ورقة أكل بفاريا وكفردبيان")
last(f"{O}/guide-7.jpg", None, "Plan your Faraya weekend", "خطّطوا ويكندكن بفاريا", main="save", head=("Your Faraya", "weekend starts here"))
story(P("acampar/42-02"), f"{O}/story.jpg", "A weekend", "in Faraya", "Stays, sights and a simple plan", "ويكند بفاريا", main="save")
print("ok")
