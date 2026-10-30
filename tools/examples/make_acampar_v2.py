"""Acampar new bungalows (Reel, 4 Nov 2026): story in the Weekendna-as-hero design. Photos: reels/public/photos/acampar (39-42)."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from hero import *
ROOT = os.path.join(os.path.dirname(__file__), "..", ".."); OUT = f"{ROOT}/posts/2026-11-acampar-bungalows"
P = lambda n: Image.open(f"{ROOT}/reels/public/photos/acampar/{n}.webp").convert("RGB")
story(P("42-02"), f"{OUT}/story.jpg", "Your fireplace weekend", "in Faraya, found for you", "2 new bungalows · up to 6 guests · from $80",
      "ويكند عالشومينيه بفاريا", "FARAYA", cx=0.7, badge="New on Weekendna")
print("ok")
