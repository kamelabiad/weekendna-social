"""DRAFT for Kamel's approval (7 Nov 2026), not in posts/log.json: Casa Verde Guest House (listing 60, new client), 5-slide on-brand carousel.
Facts (api.weekendna.com, 7 Nov 2026): Bcharre & the Cedars, Deluxe double room, 2 bedrooms, up to 4 guests, from $120 a night, fireplace, ski nearby,
100 min from Beirut as shown, power all day, generator included. No day-use content. Photos: reels/public/photos/casaverde.
Usage: export WK_WORK=$HOME/wk-work && python3 tools/examples/make_casa_verde.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from brand import *
ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
OUT = os.path.join(ROOT, "posts", "2026-11-casa-verde"); os.makedirs(OUT, exist_ok=True)
P = lambda n: Image.open(f"{ROOT}/reels/public/photos/casaverde/60-{n}.webp").convert("RGB")
N = 5
def slide(i, photo, kicker, l1, l2, foot, cy=0.5):
    img = shade(cover(photo, W, H, cy=cy), 700, 225, 1.5); d = ImageDraw.Draw(img)
    logo(d, M, 60, WHITE, 40)
    pill(d, M, 905, kicker, jak(700, 22))
    d.text((M, 975), l1, font=jak(800, 76), fill=WHITE); d.text((M, 1065), l2, font=jak(800, 76), fill=WHITE)
    d.text((M, 1190), foot, font=jak(500, 27), fill=(235, 235, 235)); dots(d, N, i)
    img.save(f"{OUT}/casaverde-{i+1}.jpg", quality=94)
slide(0, P("03"), "New on Weekendna", "Lights on,", "mountain air.", "Casa Verde Guest House  ·  from $120 a night", cy=0.6)
slide(1, P("06"), "Fireplace  ·  wood ceilings", "Warm wood,", "room to gather.", "Up to 4 guests  ·  2 bedrooms", cy=0.45)
slide(2, P("01"), "Your own garden", "A garden for", "slow afternoons.", "Bcharre & the Cedars  ·  near the slopes")
slide(3, P("11"), "Power all day", "Cosy inside,", "mountain outside.", "Generator included  ·  fireplace", cy=0.5)
img = Image.new("RGB", (W, H), RED); d = ImageDraw.Draw(img)
logo(d, M, 60, WHITE, 40, accent=WHITE)
img.paste(cover(P("04"), W - 2 * M, 520, cy=0.55), (M, 160))
d.text((M, 735), "Save this for", font=jak(800, 76), fill=WHITE); d.text((M, 825), "your next weekend.", font=jak(800, 76), fill=WHITE)
d.text((M, 960), "Casa Verde  ·  from $120 a night", font=jak(700, 32), fill=WHITE)
d.text((M, 1010), "Up to 4 guests  ·  Bcharre & the Cedars", font=jak(500, 28), fill=(255, 225, 229))
d.text((M, 1080), "Request your dates on WhatsApp, nothing to pay yet.", font=jak(500, 26), fill=(255, 225, 229))
d.text((M, 1120), "weekendna.com  ·  link in bio", font=jak(500, 26), fill=(255, 225, 229))
button(d, 1200, "Follow @weekendna.lb", jak(800, 32), bg=WHITE, fg=RED); dots(d, N, 4)
img.save(f"{OUT}/casaverde-5.jpg", quality=94)
open(f"{OUT}/caption.txt", "w", encoding="utf-8").write("""Lights on, mountain air.
New on Weekendna: Casa Verde Guest House in Bcharre & the Cedars, near the slopes. A cosy stay with a fireplace, wood ceilings and its own garden, for up to 4 guests, with power all day and a generator included. From $120 a night.

\U0001F516 Save this for your next weekend, or send it to your weekend partner.

Request your dates on WhatsApp, nothing to pay yet: weekendna.com (link in bio) \U0001F4C5
\U0001F449 Follow @weekendna.lb so you don't miss the next one \U0001F3E1

#Weekendna #Bcharre #Cedars #LebanonChalets #Lebanon #WinterInLebanon
""")
