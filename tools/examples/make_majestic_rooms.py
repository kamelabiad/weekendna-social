"""Majestic Byblos, the other rooms (31 Oct 2026): Weekendna-as-hero carousel for listings 45 (Majestic Room), 46 (Family Room), 47 (Family Suite).
Photos: python3 tools/reel_prep.py photos <dir> 45 46 47 ; usage: python3 tools/examples/make_majestic_rooms.py <photo-dir>"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from hero import *
ROOT = os.path.join(os.path.dirname(__file__), "..", ".."); OUT = f"{ROOT}/posts/2026-10-majestic-rooms"; PH = sys.argv[1]
P = lambda n: Image.open(f"{PH}/{n}.webp").convert("RGB")
slide1(P("47-02"), f"{OUT}/majrooms-1.jpg", "Your Byblos family weekend,", "found for you", "Rooms for 2 to 4 guests · from $150 a night",
       "لقينالكن ويكند عيلة بجبيل", "Majestic Byblos Grand Hotel · Jbeil (Byblos)", framed=True)
place_slide(P("45-01"), f"{OUT}/majrooms-2.jpg", 1, 3, "Majestic Room", "Jbeil (Byblos)",
            ["Twin or king-size bed + a sofa bed", "Private balcony", "More space than the Deluxe Room"], "$150 / night",
            "بلكون خاص وكنباية بتصير تخت")
place_slide(P("46-01"), f"{OUT}/majrooms-3.jpg", 2, 3, "Family Room", "Jbeil (Byblos)",
            ["2 bedrooms: a king bed + twin beds", "Bathroom with a bathtub", "Up to 4 guests"], "$250 / night · $62.50 each for 4",
            "غرفتين نوم وبانيو، لأربعة أشخاص")
place_slide(P("47-01"), f"{OUT}/majrooms-4.jpg", 3, 3, "Family Suite", "Jbeil (Byblos)",
            ["2 bedrooms + a separate living room", "Private balcony, Mediterranean views", "Up to 4 guests"], "$305 / night · about $76 each for 4",
            "غرفتين نوم وصالون وبلكون عالبحر")
last(f"{OUT}/majrooms-5.jpg", "Byblos", "Family rooms and suites by the sea, from $150", "ويكند العيلة بجبيل بيبلش من هون", "BYBLOS")
print("ok")
