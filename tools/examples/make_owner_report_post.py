"""Online presence report carousel for owners (English only). All figures are INVENTED and labelled SAMPLE: no real owner's data is shown.
Writes posts/2026-11-owner-report/report-1..7.jpg (1080x1350), story.jpg (1080x1920), caption.txt.
What the report covers (Kamel, 3 Nov 2026): price consistency across the web, Google reviews grouped by theme, website check, other online presence.
Usage: source tools/setup.sh && python3 tools/examples/make_owner_report_post.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from brand import *

POST = os.path.join(os.path.dirname(__file__), "..", "..", "posts", "2026-11-owner-report")
os.makedirs(POST, exist_ok=True)
DARK = (26, 24, 28); GREEN = (37, 160, 90); AMBER = (232, 150, 20); GREY = (130, 130, 135); LIGHT = (238, 238, 240)
N = 7


def wrap(d, text, font, maxw):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw: cur = t
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines


def para(d, x, y, text, font, fill, maxw, lh):
    for ln in wrap(d, text, font, maxw):
        d.text((x, y), ln, font=font, fill=fill); y += lh
    return y


def save(img, n): img.save(os.path.join(POST, f"report-{n}.jpg"), quality=92)


def base(bg, logo_color=WHITE, accent=None, tagbg=RED, tagfg=WHITE):
    img = Image.new("RGB", (W, H), bg); d = ImageDraw.Draw(img)
    logo(d, M, 64, color=logo_color, accent=accent)
    f = jak(700, 26); t = "FOR OWNERS"; w1 = d.textlength(t, font=f); x0 = W - M - w1 - 44
    d.rounded_rectangle((x0, 58, W - M, 112), radius=27, fill=tagbg); d.text((x0 + 22, 70), t, font=f, fill=tagfg)
    return img, d


def sample(d, y=430, x=M):
    t = "SAMPLE · NOT A REAL PLACE"; f = jak(700, 20); w = d.textlength(t, font=f)
    d.rounded_rectangle((x, y, x + w + 40, y + 44), radius=22, fill=INK); d.text((x + 20, y + 11), t, font=f, fill=WHITE)


def chip(d, x, y, text, bg, fg=WHITE, f=None):
    f = f or jak(800, 24); w = d.textlength(text, font=f)
    d.rounded_rectangle((x, y, x + w + 36, y + 46), radius=23, fill=bg); d.text((x + 18, y + 10), text, font=f, fill=fg)
    return x + w + 36


def title(d, a, b, colb=RED, cola=INK, y=170):
    d.text((M, y), a, font=jak(800, 72), fill=cola); d.text((M, y + 86), b, font=jak(800, 72), fill=colb)


# ---------- 1. Hook ----------
img, d = base(DARK)
y = 260
y = para(d, M, y, "Is your place easy to trust online?", jak(800, 90), WHITE, W - 2 * M, 112)
y += 30
y = para(d, M, y, "We check how guests see you across the web and send you a private report.", jak(500, 42), (210, 210, 215), W - 2 * M, 60)
d.rounded_rectangle((M, 900, W - M, 904), radius=2, fill=RED)
for i, t in enumerate(["Your prices, compared across the web", "Your Google reviews, grouped", "Your website, checked", "Your other online presence"]):
    d.ellipse((M, 950 + i * 62 + 12, M + 18, 950 + i * 62 + 30), fill=RED)
    d.text((M + 40, 950 + i * 62), t, font=jak(700, 36), fill=WHITE)
d.text((M, H - 100), "Swipe  >", font=jak(700, 34), fill=(190, 190, 195))
dots(d, N, 0); save(img, 1)

# ---------- 2. Price consistency ----------
img, d = base(SOFT, logo_color=INK)
d.text((M, 150), "CHECK 1/4", font=jak(800, 34), fill=RED)
title(d, "Are your prices", "the same everywhere?", y=205)
sample(d, 400)
d.rounded_rectangle((M, 470, W - M, 1000), radius=36, fill=WHITE)
d.text((M + 40, 495), "Same dates, same room", font=jak(700, 30), fill=GREY)
rows = [("Your website", "$120", GREEN, "Match"), ("Booking site A", "$120", GREEN, "Match"), ("Booking site B", "$135", AMBER, "Differs"), ("Travel site C", "Not listed", GREY, "Missing")]
yy = 560
for name, price, col, status in rows:
    d.rounded_rectangle((M + 30, yy, W - M - 30, yy + 90), radius=24, fill=SOFT)
    d.text((M + 60, yy + 26), name, font=jak(700, 32), fill=INK)
    d.text((M + 480, yy + 26), price, font=jak(800, 32), fill=INK)
    chip(d, W - M - 30 - 30 - d.textlength(status, font=jak(800, 24)) - 36, yy + 22, status, col)
    yy += 108
para(d, M, 1045, "We compare your prices on your website and the booking sites, and flag where they don't match. Guests lose trust when numbers differ.", jak(500, 34), INK, W - 2 * M, 48)
dots(d, N, 1, color=RED); save(img, 2)

# ---------- 3. Google reviews grouped ----------
img, d = base(WHITE, logo_color=INK)
d.text((M, 150), "CHECK 2/4", font=jak(800, 34), fill=RED)
title(d, "Your Google reviews,", "grouped by theme", y=205)
sample(d, 400)
d.rounded_rectangle((M, 470, W - M, 1000), radius=36, fill=SOFT)
d.text((M + 40, 495), "4.2", font=jak(800, 80), fill=INK)
d.text((M + 230, 510), "Google rating", font=jak(700, 30), fill=INK)
d.text((M + 230, 553), "example, 180 reviews", font=jak(500, 26), fill=GREY)
themes = [("Cleanliness", 0.86, GREEN, "Praised"), ("View", 0.74, GREEN, "Praised"), ("Host and staff", 0.62, GREEN, "Praised"), ("Parking", 0.34, AMBER, "Mixed"), ("Wi-Fi", 0.22, RED, "Complaints")]
yy = 640
for name, frac, col, lab in themes:
    d.text((M + 40, yy), name, font=jak(700, 28), fill=INK)
    d.text((W - M - 40 - d.textlength(lab, font=jak(700, 26)), yy + 2), lab, font=jak(700, 26), fill=col)
    d.rounded_rectangle((M + 40, yy + 42, W - M - 40, yy + 58), radius=8, fill=LIGHT)
    d.rounded_rectangle((M + 40, yy + 42, M + 40 + (W - 2 * M - 80) * frac, yy + 58), radius=8, fill=col)
    yy += 72
para(d, M, 1045, "We read your Google reviews and group them: what guests love, and what keeps coming up as a problem.", jak(500, 34), INK, W - 2 * M, 48)
dots(d, N, 2, color=RED); save(img, 3)

# ---------- 4. Website check ----------
img, d = base(DARK)
d.text((M, 150), "CHECK 3/4", font=jak(800, 34), fill=RED)
title(d, "Is your website", "bringing in bookings?", cola=WHITE, y=205)
sample(d, 400, )
d.rounded_rectangle((M, 470, W - M, 1000), radius=36, fill=(40, 38, 44))
checks = [("Works well on a phone", True), ("Clear way to book or ask for dates", True), ("Prices shown", False), ("Contact details easy to find", True), ("Photos load fast", False)]
yy = 510
for t, ok in checks:
    col = GREEN if ok else RED
    d.ellipse((M + 40, yy, M + 40 + 56, yy + 56), fill=col)
    if ok: d.line([(M + 40 + 15, yy + 29), (M + 40 + 25, yy + 40), (M + 40 + 42, yy + 18)], fill=WHITE, width=7, joint="curve")
    else: d.text((M + 40 + 28 - d.textlength("!", font=jak(800, 32)) / 2, yy + 8), "!", font=jak(800, 32), fill=WHITE)
    d.text((M + 120, yy + 8), t, font=jak(700, 32), fill=WHITE)
    d.text((W - M - 40 - d.textlength("OK" if ok else "Fix", font=jak(800, 28)), yy + 10), "OK" if ok else "Fix", font=jak(800, 28), fill=col)
    yy += 94
para(d, M, 1045, "We look at your website the way a guest does, and list what to fix first.", jak(500, 36), WHITE, W - 2 * M, 52)
dots(d, N, 3); save(img, 4)

# ---------- 5. Other online presence ----------
img, d = base(SOFT, logo_color=INK)
d.text((M, 150), "CHECK 4/4", font=jak(800, 34), fill=RED)
title(d, "Everywhere else", "guests find you", y=205)
sample(d, 400)
d.rounded_rectangle((M, 470, W - M, 1000), radius=36, fill=WHITE)
places = [("Google Maps listing", "Complete", GREEN), ("Instagram", "Active", GREEN), ("Facebook page", "Out of date", AMBER), ("Booking sites", "2 found", GREEN), ("Travel and review sites", "Not found", GREY)]
yy = 505
for name, st, col in places:
    d.text((M + 40, yy + 12), name, font=jak(700, 32), fill=INK)
    chip(d, W - M - 40 - d.textlength(st, font=jak(800, 24)) - 36, yy + 6, st, col)
    d.rounded_rectangle((M + 40, yy + 78, W - M - 40, yy + 80), radius=1, fill=LIGHT)
    yy += 94
para(d, M, 1045, "Maps, social pages, booking sites and review sites: we check that your name, photos, phone number and details are right and match.", jak(500, 34), INK, W - 2 * M, 48)
dots(d, N, 4, color=RED); save(img, 5)

# ---------- 6. What you get ----------
img, d = base(WHITE, logo_color=INK)
title(d, "What you get", "in your report", y=170)
d.rounded_rectangle((M, 400, W - M, 920), radius=36, fill=SOFT)
items = [("1", "A private page for your place only", RED), ("2", "What to fix first, in order", RED), ("3", "Clear findings, no guesses", RED)]
yy = 440
for n, t, col in items:
    d.ellipse((M + 40, yy, M + 40 + 72, yy + 72), fill=col)
    d.text((M + 40 + 36 - d.textlength(n, font=jak(800, 40)) / 2, yy + 12), n, font=jak(800, 40), fill=WHITE)
    d.text((M + 140, yy + 16), t, font=jak(700, 34), fill=INK)
    yy += 150
para(d, M, 970, "A detailed monthly report is available if you want to keep track of your progress.", jak(500, 36), INK, W - 2 * M, 52)
para(d, M, 1120, "The pages in this post are a sample with example figures. Your report uses your own place.", jak(500, 28), GREY, W - 2 * M, 40)
dots(d, N, 5, color=RED); save(img, 6)

# ---------- 7. CTA ----------
img, d = base(RED, accent=INK, tagbg=WHITE, tagfg=RED)
y = 260
y = para(d, M, y, "Want to see how your place looks online?", jak(800, 84), WHITE, W - 2 * M, 104)
y += 30
y = para(d, M, y, "Message us and we'll prepare your report.", jak(600, 44), (255, 225, 228), W - 2 * M, 62)
d.rounded_rectangle((M, 820, W - M, 1000), radius=36, fill=WHITE)
d.text((M + 44, 850), "For owners on Weekendna", font=jak(800, 40), fill=INK)
d.text((M + 44, 912), "0% commission, free for the first 12 months", font=jak(600, 30), fill=RED)
button(d, 1120, "Message @weekendna.lb", bg=INK)
dots(d, N, 6); save(img, 7)

# ---------- Story ----------
SW, SH = 1080, 1920
img = Image.new("RGB", (SW, SH), RED); d = ImageDraw.Draw(img); logo(d, 72, 150, size=56, accent=INK)
y = 560
y = para(d, 72, y, "Is your place easy to trust online?", jak(800, 90), WHITE, SW - 144, 110)
y += 30
for t in ["Prices compared across the web", "Google reviews, grouped", "Website check", "Your other online presence"]:
    d.text((72, y), "•  " + t, font=jak(700, 42), fill=WHITE); y += 66
y += 20
d.text((72, y), "Owners: message us for your report", font=jak(600, 36), fill=(255, 225, 228))
d.rounded_rectangle((72, 1540, SW - 72, 1636), radius=48, fill=WHITE)
t = "Message us"; f = jak(800, 40); d.text(((SW - d.textlength(t, font=f)) / 2, 1562), t, font=f, fill=RED)
u = "@weekendna.lb"; fu = jak(600, 34); d.text(((SW - d.textlength(u, font=fu)) / 2, 1680), u, font=fu, fill=WHITE)
img.save(os.path.join(POST, "story.jpg"), quality=92)

cap = """Is your place easy to trust online? 🔍

For owners on Weekendna, we check how guests see your place across the web and send you a private report:

1️⃣ Prices: compared across your website and booking sites, with mismatches flagged
2️⃣ Google reviews: grouped by theme, so you see what guests love and what keeps coming up
3️⃣ Your website: checked the way a guest uses it, with a list of what to fix first
4️⃣ Everything else: Google Maps, social pages, booking and review sites

The pages in this post are a sample with example figures. A detailed monthly report is available too.

💬 Want your report? Message @weekendna.lb.

👉 Follow @weekendna.lb so you don't miss the next one 🏡

#weekendna #lebanon #chaletowners #lebanonhospitality #guesthouse #villalebanon
"""
open(os.path.join(POST, "caption.txt"), "w").write(cap)
print("ok")
