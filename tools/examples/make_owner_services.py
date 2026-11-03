"""Owner services carousel: what Weekendna does for an owner's place, one service per slide, ending with the online presence report (SAMPLE, no real owner data).
Writes posts/2026-11-owner-services/services-1..7.jpg (1080x1350), story.jpg (1080x1920) and caption.txt.
Usage: source tools/setup.sh && python3 tools/examples/make_owner_services.py
Facts used (Kamel / product, to 3 Nov 2026): personal page with live calendar and prices, ready WhatsApp request the owner confirms or declines,
free monthly content kit (post + story + Reel), feature on @weekendna.lb with the owner as collaborator, online presence report, 0% commission,
free 12 months then $25 per listing per month, first 10 places per region. No price is stated for the detailed monthly report.
The report slide uses invented example numbers and is labelled SAMPLE.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from brand import *

POST = os.path.join(os.path.dirname(__file__), "..", "..", "posts", "2026-11-owner-services")
os.makedirs(POST, exist_ok=True)
DARK = (26, 24, 28)
GREEN = (37, 160, 90)
GREY = (130, 130, 135)
N = 7


def wrap(d, text, font, maxw, rtl=False):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font, direction="rtl" if rtl else None) <= maxw: cur = t
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines


def para(d, x, y, text, font, fill, maxw, lh, rtl=False, xr=None):
    for ln in wrap(d, text, font, maxw, rtl):
        if rtl: rtext(d, xr, y, ln, font, fill)
        else: d.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y


def save(img, n): img.save(os.path.join(POST, f"services-{n}.jpg"), quality=92)


def tag(d, text_en, text_ar=None, bg=RED, fg=WHITE):
    f = jak(700, 26); w1 = d.textlength(text_en, font=f)
    x0 = W - M - w1 - 44
    d.rounded_rectangle((x0, 58, W - M, 112), radius=27, fill=bg)
    d.text((x0 + 22, 70), text_en, font=f, fill=fg)


def step(d, n, color=RED):
    """Big service number so owners see 'one by one'."""
    s = f"{n}/6"; f = jak(800, 34)
    d.text((M, 150), "SERVICE " + s, font=f, fill=color)


def base(bg, logo_color=WHITE, accent=None):
    img = Image.new("RGB", (W, H), bg); d = ImageDraw.Draw(img)
    logo(d, M, 64, color=logo_color, accent=accent); tag(d, "FOR OWNERS")
    return img, d


# ---------- 1. Hook ----------
img, d = base(DARK)
y = 290
y = para(d, M, y, "6 things Weekendna does for your place", jak(800, 84), WHITE, W - 2 * M, 104)
y += 26
d.rounded_rectangle((M, 960, W - M, 964), radius=2, fill=RED)
d.text((M, 1010), "0% commission. Free for 12 months.", font=jak(700, 42), fill=WHITE)
d.text((M, H - 100), "Swipe  >", font=jak(700, 34), fill=(190, 190, 195))
dots(d, N, 0); save(img, 1)

# ---------- 2. Personal booking page + live calendar ----------
img, d = base(SOFT, logo_color=INK); step(d, 1)
d.text((M, 205), "Your own page", font=jak(800, 76), fill=INK)
d.text((M, 295), "with a live calendar", font=jak(800, 76), fill=RED)
cx0, cy0, cx1, cy1 = M, 410, W - M, 960
d.rounded_rectangle((cx0, cy0, cx1, cy1), radius=36, fill=WHITE)
d.text((cx0 + 40, cy0 + 30), "November", font=jak(800, 36), fill=INK)
colw = (cx1 - cx0 - 80) / 7
for i, ch in enumerate(["M", "T", "W", "T", "F", "S", "S"]):
    d.text((cx0 + 40 + i * colw + colw / 2 - d.textlength(ch, font=jak(700, 24)) / 2, cy0 + 82), ch, font=jak(700, 24), fill=GREY)
unavail = {3, 4, 5, 11, 12, 19, 20, 26}; sel = {13, 14, 15}
for n in range(1, 31):
    r, c = divmod(6 + n - 1, 7)
    x = cx0 + 40 + c * colw; y = cy0 + 122 + r * 68
    f = jak(700, 28)
    if n in sel: d.rounded_rectangle((x + 6, y, x + colw - 6, y + 60), radius=16, fill=RED); col = WHITE
    elif n in unavail: d.rounded_rectangle((x + 6, y, x + colw - 6, y + 60), radius=16, fill=(238, 238, 240)); col = (170, 170, 175)
    else: col = INK
    s = str(n); d.text((x + colw / 2 - d.textlength(s, font=f) / 2, y + 14), s, font=f, fill=col)
para(d, M, 1000, "Guests pick their dates and see your prices before they write to you. Your link goes in your Instagram bio.", jak(500, 34), INK, W - 2 * M, 48)
dots(d, N, 1, color=RED); save(img, 2)

# ---------- 3. Ready request on WhatsApp ----------
img, d = base(WHITE, logo_color=INK); step(d, 2, GREEN)
d.text((M, 205), "A ready request", font=jak(800, 76), fill=INK)
d.text((M, 295), "on WhatsApp", font=jak(800, 76), fill=GREEN)
d.rounded_rectangle((M, 430, W - M, 900), radius=36, fill=(236, 245, 238))
bub = (M + 40, 470, W - M - 40, 860)
d.rounded_rectangle(bub, radius=28, fill=WHITE)
yy = 505
for k, v in [("Dates", "Fri 13 to Sun 15"), ("Guests", "4"), ("Guest", "Name + phone number")]:
    d.text((bub[0] + 36, yy), k, font=jak(600, 30), fill=(120, 120, 125)); d.text((bub[0] + 250, yy), v, font=jak(700, 34), fill=INK); yy += 72
d.rounded_rectangle((bub[0] + 36, 745, bub[0] + 286, 819), radius=37, fill=GREEN)
d.text((bub[0] + 161 - d.textlength("Confirm", font=jak(800, 30)) / 2, 763), "Confirm", font=jak(800, 30), fill=WHITE)
d.rounded_rectangle((bub[0] + 310, 745, bub[0] + 560, 819), radius=37, fill=(238, 238, 240))
d.text((bub[0] + 435 - d.textlength("Decline", font=jak(800, 30)) / 2, 763), "Decline", font=jak(800, 30), fill=(90, 90, 95))
para(d, M, 950, "You get the dates, the number of guests and their number. You confirm or decline, and agree the deposit directly with the guest.", jak(500, 34), INK, W - 2 * M, 48)
dots(d, N, 2, color=RED); save(img, 3)

# ---------- 4. Free monthly content kit ----------
img, d = base(DARK); step(d, 3)
d.text((M, 205), "A free content kit", font=jak(800, 76), fill=WHITE)
d.text((M, 295), "every month", font=jak(800, 76), fill=RED)
items = [("Post", ""), ("Story", ""), ("Reel", "")]
x = M; bw = (W - 2 * M - 2 * 30) / 3
for en, a in items:
    d.rounded_rectangle((x, 450, x + bw, 760), radius=32, fill=(40, 38, 44))
    d.text((x + bw / 2 - d.textlength(en, font=jak(800, 48)) / 2, 580), en, font=jak(800, 48), fill=WHITE)
    x += bw + 30
para(d, M, 810, "Made from your listing, ready to share with your own followers. Something agencies charge for, included.", jak(500, 36), WHITE, W - 2 * M, 52)
dots(d, N, 3); save(img, 4)

# ---------- 5. Featured on @weekendna.lb ----------
img, d = base(RED, accent=INK); step(d, 4, WHITE)
d.text((M, 205), "Featured on", font=jak(800, 80), fill=WHITE)
d.text((M, 300), "@weekendna.lb", font=jak(800, 80), fill=INK)
d.rounded_rectangle((M, 450, W - M, 860), radius=36, fill=WHITE)
d.ellipse((M + 40, 490, M + 140, 590), fill=RED)
d.text((M + 90 - d.textlength("W", font=jak(800, 44)) / 2, 514), "W", font=jak(800, 44), fill=WHITE)
d.text((M + 170, 500), "weekendna.lb", font=jak(800, 36), fill=INK)
d.text((M + 170, 550), "with your place", font=jak(600, 30), fill=GREY)
d.rounded_rectangle((M + 40, 630, W - M - 40, 810), radius=24, fill=SOFT)
d.text((M + 70, 668), "Posted as a collab:", font=jak(700, 34), fill=INK)
d.text((M + 70, 724), "it reaches your followers too", font=jak(600, 34), fill=RED)
para(d, M, 905, "We feature your place and add you as a collaborator, so the post shows on your profile as well.", jak(500, 36), WHITE, W - 2 * M, 52)
dots(d, N, 4); save(img, 5)

# ---------- 6. Online presence report (SAMPLE) ----------
img, d = base(SOFT, logo_color=INK); step(d, 5)
d.text((M, 205), "Your online", font=jak(800, 76), fill=INK)
d.text((M, 295), "presence report", font=jak(800, 76), fill=RED)
d.rounded_rectangle((M, 410, W - M, 1010), radius=36, fill=WHITE)
d.rounded_rectangle((M + 36, 440, M + 36 + 330, 492), radius=26, fill=INK)
d.text((M + 36 + 165 - d.textlength("SAMPLE · NOT A REAL PLACE", font=jak(700, 20)) / 2, 454), "SAMPLE · NOT A REAL PLACE", font=jak(700, 20), fill=WHITE)
d.text((M + 40, 520), "4.2", font=jak(800, 100), fill=INK)
d.text((M + 240, 545), "Google rating", font=jak(700, 32), fill=INK)
d.text((M + 240, 590), "example figures", font=jak(500, 28), fill=GREY)
rows = [("What guests praise", "view, cleanliness, host"), ("What they mention", "parking, Wi-Fi"), ("Your website", "what to fix first")]
yy = 690
for k, v in rows:
    d.rounded_rectangle((M + 36, yy, W - M - 36, yy + 88), radius=24, fill=SOFT)
    d.text((M + 64, yy + 24), k, font=jak(700, 30), fill=INK)
    d.text((W - M - 64 - d.textlength(v, font=jak(600, 28)), yy + 26), v, font=jak(600, 28), fill=RED)
    yy += 102
para(d, M, 1050, "We compare your prices across the web, group your Google reviews and check your website. A detailed monthly report is available too.", jak(500, 33), INK, W - 2 * M, 46)
dots(d, N, 5, color=RED); save(img, 6)

# ---------- 7. Terms + CTA ----------
img, d = base(RED, accent=INK)
ctext(d, 190, "0%", jak(800, 230), WHITE)
ctext(d, 450, "commission", jak(800, 64), WHITE)
d.rounded_rectangle((M, 650, W - M, 960), radius=36, fill=WHITE)
d.text((M + 44, 680), "Free for 12 months", font=jak(800, 46), fill=INK)
d.text((M + 44, 750), "Then $25 per listing per month", font=jak(700, 38), fill=INK)
d.text((M + 44, 810), "Still 0% commission", font=jak(700, 38), fill=RED)
d.text((M + 44, 880), "Limited to the first 10 places in each region", font=jak(600, 28), fill=(110, 110, 115))
button(d, 1170, "Message @weekendna.lb", bg=INK)
dots(d, N, 6); save(img, 7)

# ---------- Story (9:16) ----------
SW, SH = 1080, 1920
img = Image.new("RGB", (SW, SH), RED); d = ImageDraw.Draw(img); logo(d, 72, 150, size=56, accent=INK)
y = 560
y = para(d, 72, y, "Owners: 6 things we do for your place", jak(800, 88), WHITE, SW - 144, 108)
y += 20
y += 40
for t in ["Your own page + live calendar", "Ready WhatsApp requests", "Free monthly content kit", "Featured on @weekendna.lb", "Online presence report", "0% commission"]:
    d.text((72, y), "•  " + t, font=jak(700, 40), fill=WHITE); y += 62
d.rounded_rectangle((72, 1540, SW - 72, 1636), radius=48, fill=WHITE)
t = "Message us to join"; f = jak(800, 40)
d.text(((SW - d.textlength(t, font=f)) / 2, 1562), t, font=f, fill=RED)
u = "@weekendna.lb"; fu = jak(600, 34); d.text(((SW - d.textlength(u, font=fu)) / 2, 1680), u, font=fu, fill=WHITE)
img.save(os.path.join(POST, "story.jpg"), quality=92)

# ---------- Caption ----------
cap = """Own a chalet, villa or guesthouse in Lebanon? Here is what Weekendna does for your place 🏡

1️⃣ Your own page with a live calendar and your prices
2️⃣ A ready request on WhatsApp: you confirm or decline
3️⃣ A free content kit every month: post, story and Reel
4️⃣ Featured on @weekendna.lb with you as collaborator
5️⃣ An online presence report: we compare your prices across the web, group your Google reviews and check your website (the one in the post is a sample)
6️⃣ 0% commission, free for 12 months, then $25 per listing per month. Limited to the first 10 places in each region.

💬 Want your place on Weekendna? Message @weekendna.lb.

👉 Follow @weekendna.lb so you don't miss the next one 🏡

#weekendna #lebanon #lebanonchalets #lebanonhospitality #chaletowners #villalebanon #guesthouse
"""
open(os.path.join(POST, "caption.txt"), "w").write(cap)
print("ok")
