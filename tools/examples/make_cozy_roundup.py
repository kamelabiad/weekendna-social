"""Pure Weekendna roundup (Mon 2 Nov 2026): 4 cozy stays with a fireplace for a rainy weekend. No collaborator, no owner tags.
Photos: reels/public/photos/{baabdat,acampar,fvc,royal}."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from hero import *
ROOT = os.path.join(os.path.dirname(__file__), "..", ".."); OUT = f"{ROOT}/posts/2026-11-cozy-weekend"
P = lambda f: Image.open(f"{ROOT}/reels/public/photos/{f}.webp").convert("RGB")
slide1(P("acampar/42-02"), f"{OUT}/cozy-1.jpg", "Your rainy weekend,", "found for you", "4 cozy stays with a fireplace, from $80 a night",
       "لقينالكن ٤ محلات دافية لويكند الشتي", "Metn · Faraya · Bcharre & the Cedars", cx=0.75)
place_slide(unbar(P("baabdat/32-02")), f"{OUT}/cozy-2.jpg", 1, 4, "Bayt Baabdat", "Metn · 15 min from Beirut",
            ["A fireplace, a garden and a barbecue", "2 bedrooms, up to 5 guests", "Its own pool for warmer days"], "$80 a night · $100 Fri & Sat",
            "شومينيه وجنينة، ١٥ دقيقة عن بيروت")
place_slide(P("acampar/42-04"), f"{OUT}/cozy-3.jpg", 2, 4, "Acampar Faraya", "Faraya · 45 min from Beirut",
            ["Wooden bungalows, most with a fireplace", "Near the ski slopes, mountain views", "From 2 up to 6 guests"], "From $80 a night",
            "بنغلوهات خشب مع شومينيه بفاريا")
place_slide(P("fvc/28-07"), f"{OUT}/cozy-4.jpg", 3, 4, "Faraya Village Club", "Faraya · Mzaar · 45 min from Beirut",
            ["Chalets with a chimney", "A heated pool on site", "From 2 up to 7 guests"], "From $150 a night",
            "شاليهات مع شومينيه ومسبح مدفّى")
place_slide(P("royal/54-10"), f"{OUT}/cozy-5.jpg", 4, 4, "Royal Chalets and Restaurant", "Bcharre & the Cedars",
            ["A fireplace and mountain views", "6 bedrooms, up to 12 guests", "Near the ski slopes"], "From $80 a night · about $7 each when 12 share",
            "شومينيه وتلج، ببشري والأرز")
last(f"{OUT}/cozy-6.jpg", None, "4 stays with a fireplace, from $80 a night", "ويكند الشتي الدافي بيبلش من هون", main="save",
     head=("Your cozy weekend", "starts here"))
story(P("acampar/42-02"), f"{OUT}/story.jpg", "Your rainy weekend,", "found for you", "4 cozy stays with a fireplace, from $80",
      "لقينالكن ٤ محلات دافية", main="save", cx=0.75)
print("ok")
