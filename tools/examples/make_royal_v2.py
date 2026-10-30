"""Royal Chalets v2 (30 Oct 2026): Weekendna-as-hero slide 1, last slide (royal-4) and story; slides 2-3 unchanged.
Photos: reels/public/photos/royal/54-NN.webp (python3 tools/reel_prep.py photos reels/public/photos/royal 54)"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from hero import *
ROOT = os.path.join(os.path.dirname(__file__), "..", ".."); OUT = f"{ROOT}/posts/2026-11-royal-chalets"
P = lambda n: Image.open(f"{ROOT}/reels/public/photos/royal/54-{n:02d}.webp").convert("RGB")
slide1(P(1), f"{OUT}/royal-1.jpg", "Your Cedars weekend,", "found for you", "Fireplace · up to 12 guests · from $80 a night",
       "لقينالك ويكند بالأرز", "Royal Chalets and Restaurant · Bcharre & the Cedars", badge="Now on Weekendna", framed=True, cy=0.45)
last(f"{OUT}/royal-4.jpg", "Cedars", "Fireplace, mountain views, near the slopes, from $80", "ويكندكن بالأرز بيبلش من هون", "CEDARS")
story(P(1), f"{OUT}/story.jpg", "Your Cedars weekend,", "found for you", "Fireplace · up to 12 guests · from $80", "لقينالك ويكند بالأرز", "CEDARS", cy=0.45)
print("ok")
