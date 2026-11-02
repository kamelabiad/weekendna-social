"""Story-only days + Discovery Reel for the organic growth plan (Kamel, 2 Nov 2026; PLAYBOOK "ORGANIC GROWTH PLAN").
Stories are plain images (the Graph API can't publish poll/question/link stickers): questions are answered by reply or DM.
Photos: reels/public/photos/{aqualand,legrey,acampar,gray}. Run `source tools/setup.sh` first."""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from hero import *
ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
P = lambda d, n: Image.open(f"{ROOT}/reels/public/photos/{d}/{n}.webp").convert("RGB")

STORIES = {  # folder: (photo, line1, line2, sub, ar_line, box)
    "2026-11-stories-03": (P("acampar", "41-02"), "Fireplace or", "sea view?", "Tell us and we'll send you a place", "شومينيه أو منظر عالبحر هالويكند؟",
                           ("Fireplace or sea view?", "Comment or DM FIREPLACE or SEA")),
    "2026-11-stories-07": (P("acampar", "42-02"), "Where in Lebanon", "is this?", "Faraya, Batroun or Jounieh? Reply with your guess", "وين بلبنان هيدا المكان؟",
                           ("Guess the area", "Reply FARAYA, BATROUN or JOUNIEH")),
    "2026-11-stories-08": (P("acampar", "42-02"), "It's Faraya,", "45 min from Beirut", "Which area should we explore next?", "فاريا، ٤٥ دقيقة عن بيروت",
                           ("Where next?", "Reply NORTH, BEKAA or SOUTH")),
    "2026-11-stories-10": (P("legrey", "48-05"), "How many", "are you?", "Send your group size, we'll send options", "قدّيش عددكن؟ ابعتولنا",
                           ("Send your group size", "and we'll send you options")),
    "2026-11-stories-14": (P("gray", "55-07"), "Do I pay", "to enquire?", "No. Send your dates on WhatsApp, nothing to pay yet", "لا، ابعتوا تواريخكن عالواتساب، بلا ما تدفعوا شي هلّق",
                           ("Nothing to pay yet", "Link in bio")),
    "2026-11-stories-15": (P("royal", "54-01"), "A new Lebanese escape", "every Thursday", "Follow so you don't miss the next one", "كل خميس هروب جديد بلبنان",
                           ("Cosy or city next?", "Reply COSY or CITY")),
}
for folder, (ph, l1, l2, sub, ar_line, box) in STORIES.items():
    os.makedirs(f"{ROOT}/posts/{folder}", exist_ok=True)
    story(ph, f"{ROOT}/posts/{folder}/story.jpg", l1, l2, sub, ar_line, badge="Weekendna", box=box)

# Discovery Reel (Mon 16 Nov): region-led, one owner's photos (Acampar), no collaborator tag
D = f"{ROOT}/posts/2026-11-discovery-faraya"; os.makedirs(D, exist_ok=True)
S = lambda n, mv, text, sec=3.0, **k: dict(photo=f"photos/acampar/42-{n:02d}.webp", seconds=sec, move=mv, text=text, **k)
shots = [S(1, "zoom_in", {"type": "hook", "en": "Wait… this is Lebanon?", "ar": "استنى… هيدا بلبنان؟"}, fy=0.5),
         S(2, "pan_right", {"type": "title", "name": "Faraya", "ar": "فاريا، ٤٥ دقيقة عن بيروت", "pill": "45 min from Beirut"}),
         S(2, "zoom_in", {"type": "fact", "en": "A fireplace and a mountain view", "ar": "شومينيه ومنظر عالجبل"}, fx=0.7),
         S(4, "pan_left", {"type": "fact", "en": "Wooden bungalows near the ski slopes", "ar": "بنغلوهات خشب قريبة من التلج"}),
         S(5, "zoom_out", {"type": "fact", "en": "For 2 to 6 guests", "ar": "من شخصين لـ٦ أشخاص"}),
         S(1, "zoom_out", {"type": "end", "name": "Faraya", "price": "From $80 / night", "ar": "ابعتوا تواريخكن عالواتساب"}, sec=4.0)]
json.dump({"music": "music/warm-acoustic-atlasaudio.mp3", "musicStart": 40, "bpm": 100, "shots": shots}, open(f"{D}/reel-remotion.json", "w"), ensure_ascii=False, indent=1)
print("ok")
