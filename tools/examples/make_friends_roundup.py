"""Pure Weekendna roundup (Sat 7 Nov 2026): 4 places for a weekend with friends, split the bill. No collaborator, no owner tags.
Per-person amounts = listing nightly (or Fri/Sat) price / max guests, always "when N share"."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from hero import *
ROOT = os.path.join(os.path.dirname(__file__), "..", ".."); OUT = f"{ROOT}/posts/2026-11-friends-weekend"
P = lambda f: Image.open(f"{ROOT}/reels/public/photos/{f}.webp").convert("RGB")
slide1(P("acampar/42-03"), f"{OUT}/friends-1.jpg", "Your friends' weekend,", "found for you", "4 places for big groups, split the bill",
       "لقينالكن محل لويكند الشلّة", "Batroun · Metn · Faraya")
place_slide(P("legrey/31-02"), f"{OUT}/friends-2.jpg", 1, 4, "Grandpa's Apartment", "Batroun · 45 min from Beirut",
            ["3 bedrooms, up to 9 guests", "A spacious terrace over the town", "In Batroun city center"], "$120 a night · about $13 each when 9 share",
            "لحد ٩ أشخاص بقلب البترون")
place_slide(unbar(P("baabdat/32-02")), f"{OUT}/friends-3.jpg", 2, 4, "Bayt Baabdat", "Metn · 15 min from Beirut",
            ["2 bedrooms, up to 5 guests", "A fireplace, a garden and a barbecue", "Its own pool"], "$100 on Fri & Sat · about $20 each when 5 share",
            "لحد ٥ أشخاص، ١٥ دقيقة عن بيروت")
place_slide(P("acampar/42-02"), f"{OUT}/friends-4.jpg", 3, 4, "Acampar Two bedroom bungalow", "Faraya · 45 min from Beirut",
            ["2 bedrooms and 2 sofa beds, up to 6", "A fireplace and an equipped kitchen", "Near the ski slopes"], "$200 a night · about $33 each when 6 share",
            "لحد ٦ أشخاص مع شومينيه بفاريا", cx=0.7)
place_slide(P("fvc/28-01"), f"{OUT}/friends-5.jpg", 4, 4, "Faraya Village Club Two Bedroom Chalet", "Faraya · Mzaar · 45 min from Beirut",
            ["2 bedrooms and 2 sofa beds, up to 7", "A chimney and a heated pool on site", "Near Mzaar"], "$450 a night · about $64 each when 7 share",
            "لحد ٧ أشخاص مع مسبح مدفّى")
last(f"{OUT}/friends-6.jpg", None, "4 places for 5 to 9 friends, from about $13 each", "ويكند الشلّة بيبلش من هون", main="save",
     head=("Your friends' weekend", "starts here"))
story(P("acampar/42-03"), f"{OUT}/story.jpg", "Your friends' weekend,", "found for you", "4 places for big groups, split the bill",
      "لقينالكن محل لويكند الشلّة", main="save")
print("ok")
