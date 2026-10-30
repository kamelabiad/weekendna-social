"""Ghosta v3 (30 Oct 2026): Weekendna-as-hero slide 1, last slide (ghosta-4) and story; slides 2-3 unchanged.
Photos: reels/public/photos/ghosta/37-NN.webp (37-14 coast view, 37-26 night lights, 37-19 balcony at dusk)."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from hero import *
ROOT = os.path.join(os.path.dirname(__file__), "..", ".."); OUT = f"{ROOT}/posts/2026-10-ghosta-guest-house"
P = lambda n: Image.open(f"{ROOT}/reels/public/photos/ghosta/37-{n:02d}.webp").convert("RGB")
slide1(P(14), f"{OUT}/ghosta-1.jpg", "Your weekend above", "the coast, found for you", "Sleeps 12 · 25 min from Beirut · from $220 a night",
       "لقينالك ويكند فوق الساحل", "Ghosta Guest House · hills above Jounieh")
last(f"{OUT}/ghosta-4.jpg", "Ghosta", "A 180° view from Beirut to Byblos, sleeps 12", "ويكندكن فوق جونية بيبلش من هون", "GHOSTA")
story(P(14), f"{OUT}/story.jpg", "Your weekend above", "the coast", "Sleeps 12 · 25 min from Beirut · from $220", "لقينالك ويكند فوق الساحل", "GHOSTA")
print("ok")
