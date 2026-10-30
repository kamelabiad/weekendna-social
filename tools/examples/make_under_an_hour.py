"""Pure Weekendna guide (Mon 9 Nov 2026): weekends under an hour from Beirut. Travel times = each listing's minutesFromBeirut. No collaborator, no owner tags."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from hero import *
ROOT = os.path.join(os.path.dirname(__file__), "..", ".."); OUT = f"{ROOT}/posts/2026-11-under-an-hour"
P = lambda f: Image.open(f"{ROOT}/reels/public/photos/{f}.webp").convert("RGB")
slide1(P("ghosta/37-20"), f"{OUT}/hour-1.jpg", "Your weekend, under", "an hour from Beirut", "4 places, 15 to 45 min away, sea or mountain",
       "لقينالكن ويكند على أقل من ساعة من بيروت", "Metn · Jounieh hills · Batroun")
place_slide(unbar(P("baabdat/32-05")), f"{OUT}/hour-2.jpg", 1, 4, "Bayt Baabdat", "Metn · 15 min from Beirut",
            ["A fireplace, a garden and a barbecue", "Its own pool, day use or overnight", "2 bedrooms, up to 5 guests"], "$80 a night · $100 Fri & Sat",
            "١٥ دقيقة عن بيروت، بالمتن")
place_slide(P("ghosta/37-19"), f"{OUT}/hour-3.jpg", 2, 4, "Ghosta Guest House", "Above Jounieh · 25 min from Beirut",
            ["A 180° view from Beirut to Byblos", "5 bedrooms, up to 12 guests", "800 m above the sea"], "From $220 a night · about $18 each when 12 share",
            "٢٥ دقيقة عن بيروت، فوق جونية")
place_slide(P("aqualand/24-01"), f"{OUT}/hour-4.jpg", 3, 4, "Aqualand Hotel & Resort", "Batroun · 35 min from Beirut",
            ["Sea views and beach access", "Rooms for 2", "Garden, heating and valet parking"], "From $150 a night",
            "٣٥ دقيقة عن بيروت، بالبترون")
place_slide(P("legrey/48-05"), f"{OUT}/hour-5.jpg", 4, 4, "Le Grey Haven", "Batroun · 45 min from Beirut",
            ["2 bedrooms, up to 4 guests", "Sea and mountain views", "Close to the beach, pubs and restaurants"], "$80 a night · about $20 each when 4 share",
            "٤٥ دقيقة عن بيروت، بالبترون")
last(f"{OUT}/hour-6.jpg", None, "4 places 15 to 45 min from Beirut, from $80", "ويكندكن أقرب مما بتفكروا", main="save",
     head=("Your weekend is", "closer than you think"))
story(P("ghosta/37-20"), f"{OUT}/story.jpg", "Your weekend, under", "an hour from Beirut", "4 places, 15 to 45 min away",
      "ويكند على أقل من ساعة من بيروت", main="save")
print("ok")
