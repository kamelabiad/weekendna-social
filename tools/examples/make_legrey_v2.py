"""Le Grey v2 (30 Oct 2026): Weekendna-as-hero slide 1, last slide (legrey-4) and story; slides 2-3 unchanged. Photos: reels/public/photos/legrey (48, 31)."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from hero import *
ROOT = os.path.join(os.path.dirname(__file__), "..", ".."); OUT = f"{ROOT}/posts/2026-11-le-grey"
P = lambda n: Image.open(f"{ROOT}/reels/public/photos/legrey/{n}.webp").convert("RGB")
slide1(P("48-07"), f"{OUT}/legrey-1.jpg", "Your Batroun weekend,", "found for you", "2 apartments · up to 9 guests · from $80 a night",
       "لقينالك ويكند بالبترون", "Le Grey Haven & Grandpa's Apartment · Batroun", badge="Now on Weekendna", cy=0.55)
last(f"{OUT}/legrey-4.jpg", "Batroun", "Sea and mountain views, close to the beach, from $80", "ويكندكن بالبترون بيبلش من هون", "BATROUN")
story(P("48-07"), f"{OUT}/story.jpg", "Your Batroun weekend,", "found for you", "2 apartments · up to 9 guests · from $80", "لقينالك ويكند بالبترون", "BATROUN", cy=0.5)
print("ok")
