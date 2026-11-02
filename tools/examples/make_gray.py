"""The Gray House (listing 55, Ghineh, new 2 Nov 2026): Weekendna-as-hero slide 1, two detail slides, last slide and story.
Photos: python3 tools/reel_prep.py photos reels/public/photos/gray 55   (uses 55-08 balcony view, 55-07 living room, 55-01 bedroom)
Facts from the listing only: 220 m2, 2 bedrooms, 2 bathrooms, up to 5 guests, 3 private balconies, sea + mountain views, full kitchen,
washing machine, A/C, heating, free parking, 45 min from Beirut, $130 a night (about $26 each when 5 share)."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from hero import *
ROOT = os.path.join(os.path.dirname(__file__), "..", ".."); OUT = f"{ROOT}/posts/2026-11-gray-house"
os.makedirs(OUT, exist_ok=True)
P = lambda n: Image.open(f"{ROOT}/reels/public/photos/gray/55-{n:02d}.webp").convert("RGB")

slide1(P(8), f"{OUT}/gray-1.jpg", "Your Ghineh weekend,", "found for you", "Sea and mountain views · up to 5 guests · from $130 a night",
       "لقينالك ويكند بغينة", "The Gray House · Ghineh · 45 min from Beirut", badge="Now on Weekendna", cy=0.5)

def unit(photo, n, title, price, feats, ar_line, cx=0.5, cy=0.5):
    img = shade(cover(P(photo), W, H, cx=cx, cy=cy), 430, 250, 0.9)
    d = ImageDraw.Draw(img)
    logo(d, M, 64)
    pill(d, M, 740, price, jak(700, 30))
    d.text((M, 820), title, font=jak(800, 66), fill=WHITE)
    y = 930
    for en in feats:
        d.ellipse((M, y + 14, M + 16, y + 30), fill=RED)
        d.text((M + 36, y), en, font=jak(700, 36), fill=WHITE)
        y += 64
    rtext(d, W - M, y + 16, ar_line, ar(700, 40), WHITE)
    img.save(f"{OUT}/gray-{n}.jpg", quality=92)

unit(7, 2, "The Gray House", "$130 / NIGHT · UP TO 5",
     ["220 m² private retreat", "3 private balconies", "Sea and mountain views", "45 min from Beirut"],
     "بيت خاص ٢٢٠ متر، ٣ بلكونات ومنظر عالبحر والجبل", cx=0.5, cy=0.6)
unit(1, 3, "Room to relax", "2 BEDROOMS · 2 BATHROOMS",
     ["Full kitchen, washing machine", "Air conditioning and heating", "Free parking", "Terrace with sunset views"],
     "مطبخ كامل، تكييف وتدفئة، وموقف مجاني", cx=0.5, cy=0.65)
last(f"{OUT}/gray-4.jpg", "Ghineh", "Sea and mountain views, 3 balconies, from $130", "ويكندكن بغينة بيبلش من هون", "GHINEH")
story(P(8), f"{OUT}/story.jpg", "Your Ghineh weekend,", "found for you", "Up to 5 guests · from $130 a night", "لقينالك ويكند بغينة", "GHINEH", cy=0.5)
print("ok")
