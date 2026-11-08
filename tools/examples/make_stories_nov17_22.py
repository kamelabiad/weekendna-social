"""Story-only days Tue 17, Sat 21, Sun 22 Nov 2026 (weekly task 8 Nov; template: make_growth_plan_nov.py). Plain images, answers by reply/DM.
Photos: python3 tools/reel_prep.py photos reels/public/photos/casaverde 60 ; .../ghosta 37 ; .../majestic 23. Run `source tools/setup.sh` first."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from hero import *
ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
P = lambda d, n: Image.open(f"{ROOT}/reels/public/photos/{d}/{n}.webp").convert("RGB")
STORIES = {
    "2026-11-stories-17": (P("casaverde", "60-03"), "Independence weekend:", "stay or escape?", "Reply and we'll send you a place for it", "",
                           ("Stay in town or escape?", "Reply STAY or ESCAPE")),
    "2026-11-stories-21": (P("ghosta", "37-19"), "Where in Lebanon", "is this view?", "Hint: 25 min from Beirut. Reply with your guess", "",
                           ("Guess the area", "Reply JOUNIEH, METN or BYBLOS")),
    "2026-11-stories-22": (P("majestic", "23-03"), "Happy Independence", "Day, Lebanon", "Yesterday's view: above Jounieh. Where should we explore next?", "",
                           ("Where next?", "Reply NORTH, SOUTH or BEKAA")),
}
for folder, (ph, l1, l2, sub, ar_line, box) in STORIES.items():
    os.makedirs(f"{ROOT}/posts/{folder}", exist_ok=True)
    story(ph, f"{ROOT}/posts/{folder}/story.jpg", l1, l2, sub, ar_line, badge="Weekendna", box=box)
print("ok")
