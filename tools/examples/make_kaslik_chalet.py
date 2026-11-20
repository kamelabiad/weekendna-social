"""Chaleh 70 m2, Kaslik & Jounieh (listing 62, new client, owner Michel K., collab handle dj_michka): 5-slide carousel + story. Built 20 Nov 2026.
Facts (api.weekendna.com, 20 Nov 2026): 70 m2, 1 bedroom, up to 3 guests, $65 a night, sea view balcony over the bay of Jounieh, mountain view
from the living room, air conditioning, heating, 24/7 electricity, elevator, parking, washing machine, 40 min from Beirut as shown.
Photos: reels/public/photos/kaslik. No beach content (November)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from brand import *
ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
OUT = os.path.join(ROOT, "posts", "2026-11-kaslik-chalet"); os.makedirs(OUT, exist_ok=True)
P = lambda n: Image.open(f"{ROOT}/reels/public/photos/kaslik/62-{n}.webp").convert("RGB")
N = 5
def slide(i, photo, kicker, l1, l2, foot, cy=0.5):
    img = shade(cover(photo, W, H, cy=cy), 700, 225, 1.5); d = ImageDraw.Draw(img)
    logo(d, M, 60, WHITE, 40)
    pill(d, M, 905, kicker, jak(700, 22))
    d.text((M, 975), l1, font=jak(800, 76), fill=WHITE); d.text((M, 1065), l2, font=jak(800, 76), fill=WHITE)
    d.text((M, 1190), foot, font=jak(500, 27), fill=(235, 235, 235)); dots(d, N, i)
    img.save(f"{OUT}/kaslik-{i+1}.jpg", quality=94)
slide(0, P("11"), "New on Weekendna", "Sea and mountain,", "one view.", "Chalet in Kaslik & Jounieh  ·  from $65 a night", cy=0.5)
slide(1, P("01"), "70 m²  ·  fully furnished", "Room to settle", "in for the weekend.", "Up to 3 guests  ·  1 bedroom")
slide(2, P("09"), "Heating  ·  air conditioning", "Warm nights,", "calm mornings.", "A quiet bedroom for couples or small families", cy=0.55)
slide(3, P("12"), "Balcony view", "The bay of Jounieh", "from your balcony.", "24/7 electricity  ·  elevator  ·  parking", cy=0.5)
img = Image.new("RGB", (W, H), RED); d = ImageDraw.Draw(img)
logo(d, M, 60, WHITE, 40, accent=WHITE)
img.paste(cover(P("10"), W - 2 * M, 520, cy=0.5), (M, 160))
d.text((M, 735), "Save this for", font=jak(800, 76), fill=WHITE); d.text((M, 825), "your next weekend.", font=jak(800, 76), fill=WHITE)
d.text((M, 960), "Kaslik chalet  ·  from $65 a night", font=jak(700, 32), fill=WHITE)
d.text((M, 1010), "Up to 3 guests  ·  Kaslik & Jounieh", font=jak(500, 28), fill=(255, 225, 229))
d.text((M, 1080), "Request your dates on WhatsApp, nothing to pay yet.", font=jak(500, 26), fill=(255, 225, 229))
d.text((M, 1120), "weekendna.com  ·  link in bio", font=jak(500, 26), fill=(255, 225, 229))
button(d, 1200, "Follow @weekendna.lb", jak(800, 32), bg=WHITE, fg=RED); dots(d, N, 4)
img.save(f"{OUT}/kaslik-5.jpg", quality=94)
# story 1080x1920
S = Image.new("RGB", (1080, 1920), RED); sd = ImageDraw.Draw(S)
S.paste(cover(P("11"), 1080, 1100, cy=0.5), (0, 0))
logo(sd, M, 70, WHITE, 44)
pill(sd, M, 1180, "New on Weekendna", jak(700, 26))
sd.text((M, 1260), "Sea and mountain,", font=jak(800, 84), fill=WHITE); sd.text((M, 1360), "one view.", font=jak(800, 84), fill=WHITE)
sd.text((M, 1490), "Kaslik chalet  ·  from $65 a night", font=jak(700, 34), fill=WHITE)
sd.text((M, 1545), "Up to 3 guests  ·  Kaslik & Jounieh", font=jak(500, 28), fill=(255, 225, 229))
button(sd, 1700, "Follow @weekendna.lb", jak(800, 34), bg=WHITE, fg=RED)
S.save(f"{OUT}/story.jpg", quality=94)
open(f"{OUT}/caption.txt", "w", encoding="utf-8").write("""Sea and mountain, one view.
New on Weekendna: a 70 m² chalet in Kaslik & Jounieh with a balcony over the bay and mountain views from the living room. Heating and air conditioning, 24/7 electricity, parking, for up to 3 guests. From $65 a night.

\U0001F516 Save this for your next weekend by the sea.

Request your dates on WhatsApp, nothing to pay yet: weekendna.com (link in bio)

#Weekendna #Kaslik #Jounieh #LebanonGetaways #WeekendInLebanon #WinterInLebanon
""")
open(f"{OUT}/whatsapp.txt", "w", encoding="utf-8").write("""DRAFT for Kamel to forward (nothing is sent by Claude):
Hi! This is Kamel from Weekendna. We're featuring your Kaslik chalet for free on our Instagram, @weekendna.lb, on Tuesday evening as a collab post with @dj_michka. When the invitation appears in your Instagram notifications, please tap Accept. It uses the photos from your Weekendna listing. Thank you!
""")
