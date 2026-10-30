"""Phare du Nord v2 (30 Oct 2026): Weekendna-as-hero slide 1, last slide (phare-4) and story; slides 2-3 unchanged. Photos: reels/public/photos/phare (49)."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from hero import *
ROOT = os.path.join(os.path.dirname(__file__), "..", ".."); OUT = f"{ROOT}/posts/2026-11-phare-du-nord"
P = lambda n: Image.open(f"{ROOT}/reels/public/photos/phare/49-{n:02d}.webp").convert("RGB")
slide1(P(3), f"{OUT}/phare-1.jpg", "Your sunset wedding", "by the sea, found for you", "Up to 450 guests · ceremony on site · bridal suite",
       "لقينالك محل لعرسك عالبحر", "Phare du Nord Venue · Batroun", badge="Now on Weekendna", cy=0.5)
last(f"{OUT}/phare-4.jpg", "Batroun", "Up to 450 guests, ceremony and party in one place", "عرسكن عالبحر بيبلش من هون", "PHARE",
     head=("Your sunset wedding", "starts here"))
story(P(3), f"{OUT}/story.jpg", "Your sunset wedding", "by the sea", "Up to 450 guests · Batroun", "لقينالك محل لعرسك عالبحر", "PHARE", cy=0.5)
print("ok")
