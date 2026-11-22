"""Story-only / teaser stories Tue 24, Thu 26, Sat 28, Sun 29 Nov 2026 (weekly task 22 Nov; template: make_stories_nov17_22.py).
Plain images, answers by reply/DM (Kamel can add poll/question stickers by hand).
Photos: python3 tools/reel_prep.py photos reels/public/photos/legrey 48 ; .../ghosta 37 ; .../majestic 23 ; .../solitere 65 66 67 68.
Run `source tools/setup.sh` first, then tools/make_story_video.py on each folder."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from hero import *
ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
P = lambda d, n: Image.open(f"{ROOT}/reels/public/photos/{d}/{n}.webp").convert("RGB")
STORIES = {
    "2026-11-stories-24": (P("legrey", "48-07"), "How many are you", "this weekend?", "Tell us and we'll send you a place that fits", "",
                           ("2, 4 or a big group?", "Reply 2, 4 or 10+")),
    "2026-11-stories-26": (P("ghosta", "37-19"), "New Weekend Edit:", "a coast from one balcony", "Up to 12 guests, 25 min from Beirut. Now on our feed", "",
                           ("Who would you bring?", "Send this to your group")),
    "2026-11-stories-28": (P("majestic", "23-03"), "Do I pay to", "request dates?", "No. WhatsApp opens with your dates, the owner replies and confirms", "",
                           ("Nothing to pay Weekendna", "Ask us anything: reply here")),
    "2026-11-stories-29": (P("solitere", "65-04"), "This week: Byblos,", "Kaslik, Ghosta, Batroun", "Where should we explore next?", "",
                           ("Where next?", "Reply NORTH, METN or BEKAA")),
}
for folder, (ph, l1, l2, sub, ar_line, box) in STORIES.items():
    os.makedirs(f"{ROOT}/posts/{folder}", exist_ok=True)
    story(ph, f"{ROOT}/posts/{folder}/story.jpg", l1, l2, sub, ar_line, badge="Weekendna", box=box)
print("ok")
