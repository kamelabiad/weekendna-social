"""Pure Weekendna roundup (Sat 14 Nov 2026): sea or mountain? 2 sea-view rooms + 2 mountain stays with a fireplace. No collaborator, no owner tags.
Photos: python3 tools/reel_prep.py photos reels/public/photos/seamtn 23 24 26 39 ; ... reels/public/photos/royal 54"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from hero import *
ROOT = os.path.join(os.path.dirname(__file__), "..", ".."); OUT = f"{ROOT}/posts/2026-11-sea-or-mountain"
P = lambda f: Image.open(f"{ROOT}/reels/public/photos/{f}.webp").convert("RGB")
slide1(P("seamtn/23-03"), f"{OUT}/seamtn-1.jpg", "Sea or mountain?", "Your weekend, found", "2 by the sea, 2 in the mountains, from $80 a night",
       "بحر أو جبل؟ لقينالكن ويكندكن", "Byblos · Batroun · Faraya · Bcharre & the Cedars", cx=0.5)
place_slide(P("seamtn/24-02"), f"{OUT}/seamtn-2.jpg", 1, 4, "Aqualand Hotel & Resort", "Sea · Batroun · 35 min from Beirut",
            ["Deluxe room with a sea-view terrace", "A spa bath in the room", "Beach access, for 2 guests"], "$180 a night",
            "غرفة مع تراس عالبحر بالبترون")
place_slide(P("seamtn/23-01"), f"{OUT}/seamtn-3.jpg", 2, 4, "Majestic Byblos Grand Hotel", "Sea · Byblos",
            ["Deluxe room with a private balcony", "Sea or Byblos city views", "Twin or king bed, for 2 guests"], "$130 a night",
            "بلكون خاص وبحر جبيل")
place_slide(P("seamtn/39-02"), f"{OUT}/seamtn-4.jpg", 3, 4, "Acampar Faraya", "Mountain · Faraya · 45 min from Beirut",
            ["A cozy studio bungalow with a fireplace", "Mountain views, near the ski slopes", "Made for couples"], "$80 a night",
            "بنغلو خشب مع شومينيه بفاريا")
place_slide(P("royal/54-08"), f"{OUT}/seamtn-5.jpg", 4, 4, "Royal Chalets and Restaurant", "Mountain · Bcharre & the Cedars",
            ["A fireplace and mountain views", "6 bedrooms, up to 12 guests", "Near the ski slopes"], "From $80 a night · about $7 each when 12 share",
            "شومينيه ومنظر عالجبل، ببشري والأرز")
last(f"{OUT}/seamtn-6.jpg", None, "Sea or mountain, from $80 a night", "ويكندكن بيبلش من هون", main="save",
     head=("Your weekend", "starts here"))
story(P("seamtn/23-03"), f"{OUT}/story.jpg", "Sea or mountain?", "Your weekend, found", "2 by the sea, 2 in the mountains, from $80",
      "بحر أو جبل؟ لقينالكن ويكندكن", main="save")
print("ok")
