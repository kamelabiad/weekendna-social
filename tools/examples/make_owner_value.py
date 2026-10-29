"""Brand post for OWNERS (not a listing): what Weekendna gives an owner, and the ask to put their own Weekendna link in their bio.
Writes posts/2026-10-owner-value/owner-1..5.jpg (1080x1350) and story.jpg (1080x1920).
Usage: source tools/setup.sh && python3 tools/examples/make_owner_value.py
Facts used (all from the product / Kamel, 29 Oct 2026): live calendar with prices, ready request on WhatsApp, owner confirms or declines and agrees the
deposit directly, 0% commission, free for 12 months then $25 per listing per month, first 10 places per region, each owner has a personal page link.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from brand import *

POST = os.path.join(os.path.dirname(__file__), "..", "..", "posts", "2026-10-owner-value")
os.makedirs(POST, exist_ok=True)
DARK = (26, 24, 28)
GREEN = (37, 160, 90)


def wrap(d, text, font, maxw, rtl=False):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font, direction="rtl" if rtl else None) <= maxw: cur = t
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines


def para(d, x, y, text, font, fill, maxw, lh, rtl=False, xr=None):
    """Draws wrapped text; LTR from x, RTL right-aligned to xr. Returns the y after the last line."""
    for ln in wrap(d, text, font, maxw, rtl):
        if rtl: rtext(d, xr, y, ln, font, fill)
        else: d.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y


def save(img, n): img.save(os.path.join(POST, f"owner-{n}.jpg"), quality=92)


def tag(d, text_en, text_ar, bg=RED, fg=WHITE):
    """Small top-right label so owners know the post is for them."""
    f = jak(700, 26); fa = ar(700, 28)
    t = text_en; ta = text_ar
    w1 = d.textlength(t, font=f); w2 = d.textlength(ta, font=fa, direction="rtl")
    tw = w1 + 18 + w2
    x0 = W - M - tw - 44
    d.rounded_rectangle((x0, 58, W - M, 112), radius=27, fill=bg)
    d.text((x0 + 22, 70), t, font=f, fill=fg)
    d.text((x0 + 22 + w1 + 18, 66), ta, font=fa, fill=fg, direction="rtl")


# ---------- 1. Hook ----------
img = Image.new("RGB", (W, H), DARK); d = ImageDraw.Draw(img); logo(d, M, 64)
tag(d, "FOR OWNERS", "لأصحاب المحلات")
y = 300
y = para(d, M, y, "Do guests have to message you for every date and price?", jak(800, 82), WHITE, W - 2 * M, 100)
y += 30
para(d, 0, y, "لازم كل ضيف يسألك عن كل تاريخ وكل سعر؟", ar(700, 48), (255, 205, 210), W - 2 * M, 80, rtl=True, xr=W - M)
d.rounded_rectangle((M, 1010, W - M, 1010 + 4), radius=2, fill=RED)
d.text((M, 1060), "Give your place its own booking page.", font=jak(700, 44), fill=WHITE)
rtext(d, W - M, 1140, "خلّي لمحلك صفحة حجز خاصة فيه", ar(700, 44), WHITE)
d.text((M, H - 100), "Swipe  >", font=jak(700, 34), fill=(190, 190, 195))
dots(d, 5, 0)
save(img, 1)

# ---------- 2. Live calendar with prices ----------
img = Image.new("RGB", (W, H), SOFT); d = ImageDraw.Draw(img); logo(d, M, 64, color=INK)
tag(d, "FOR OWNERS", "لأصحاب المحلات")
d.text((M, 190), "A live calendar", font=jak(800, 76), fill=INK)
d.text((M, 280), "with your prices", font=jak(800, 76), fill=RED)
# calendar card
cx0, cy0, cx1, cy1 = M, 395, W - M, 995
d.rounded_rectangle((cx0, cy0, cx1, cy1), radius=36, fill=WHITE)
d.text((cx0 + 40, cy0 + 34), "November", font=jak(800, 38), fill=INK)
days = ["M", "T", "W", "T", "F", "S", "S"]
colw = (cx1 - cx0 - 80) / 7
for i, ch in enumerate(days):
    d.text((cx0 + 40 + i * colw + colw / 2 - d.textlength(ch, font=jak(700, 26)) / 2, cy0 + 90), ch, font=jak(700, 26), fill=(130, 130, 135))
unavail = {3, 4, 5, 11, 12, 19, 20, 26}
sel = {14, 15, 16}
first_col = 6  # 1 Nov 2026 is a Sunday
for n in range(1, 31):
    idx = first_col + n - 1; r, c = divmod(idx, 7)
    x = cx0 + 40 + c * colw; y = cy0 + 135 + r * 74
    box = (x + 6, y, x + colw - 6, y + 66)
    f = jak(700, 30)
    if n in sel:
        d.rounded_rectangle(box, radius=18, fill=RED); col = WHITE
    elif n in unavail:
        d.rounded_rectangle(box, radius=18, fill=(238, 238, 240)); col = (170, 170, 175)
    else:
        col = INK
    s = str(n); d.text((x + colw / 2 - d.textlength(s, font=f) / 2, y + 15), s, font=f, fill=col)
# price chips
d.rounded_rectangle((M, 1025, M + 470, 1097), radius=36, fill=WHITE)
d.text((M + 30, 1043), "Weekday prices", font=jak(700, 32), fill=INK)
d.rounded_rectangle((M + 500, 1025, M + 500 + 440, 1097), radius=36, fill=WHITE)
d.text((M + 530, 1043), "Weekend prices", font=jak(700, 32), fill=INK)
para(d, M, 1128, "Guests pick their dates and see what your place costs, before they write to you.", jak(500, 34), INK, W - 2 * M, 48)
para(d, 0, 1236, "الضيف بيختار تواريخه وبيشوف الأسعار قبل ما يراسلك", ar(600, 34), INK, W - 2 * M, 54, rtl=True, xr=W - M)
dots(d, 5, 1, color=RED)
save(img, 2)

# ---------- 3. Ready request on WhatsApp ----------
img = Image.new("RGB", (W, H), WHITE); d = ImageDraw.Draw(img); logo(d, M, 64, color=INK)
tag(d, "FOR OWNERS", "لأصحاب المحلات")
d.text((M, 190), "A ready request", font=jak(800, 76), fill=INK)
d.text((M, 280), "on WhatsApp", font=jak(800, 76), fill=GREEN)
# chat mock
d.rounded_rectangle((M, 420, W - M, 940), radius=36, fill=(236, 245, 238))
d.text((M + 40, 450), "Example request", font=jak(700, 26), fill=(110, 130, 115))
bub = (M + 40, 500, W - M - 40, 900)
d.rounded_rectangle(bub, radius=28, fill=WHITE)
rows = [("Dates", "Fri 14 to Sun 16"), ("Guests", "4"), ("Guest", "Name + phone number")]
yy = 540
for k, v in rows:
    d.text((bub[0] + 36, yy), k, font=jak(600, 30), fill=(120, 120, 125))
    d.text((bub[0] + 250, yy), v, font=jak(700, 34), fill=INK)
    yy += 74
d.rounded_rectangle((bub[0] + 36, 780, bub[0] + 36 + 250, 780 + 74), radius=37, fill=GREEN)
d.text((bub[0] + 36 + 125 - d.textlength("Confirm", font=jak(800, 30)) / 2, 798), "Confirm", font=jak(800, 30), fill=WHITE)
d.rounded_rectangle((bub[0] + 310, 780, bub[0] + 310 + 250, 780 + 74), radius=37, fill=(238, 238, 240))
d.text((bub[0] + 310 + 125 - d.textlength("Decline", font=jak(800, 30)) / 2, 798), "Decline", font=jak(800, 30), fill=(90, 90, 95))
para(d, M, 990, "You get the dates, the guests and their number. You confirm or decline, and agree the deposit directly with the guest.", jak(500, 34), INK, W - 2 * M, 48)
para(d, 0, 1150, "بيوصلك التاريخ وعدد الضيوف ورقمن، إنت بتأكّد أو بترفض، وبتتفق معن عالعربون مباشرة", ar(600, 36), INK, W - 2 * M, 58, rtl=True, xr=W - M)
dots(d, 5, 2, color=RED)
save(img, 3)

# ---------- 4. 0% commission ----------
img = Image.new("RGB", (W, H), RED); d = ImageDraw.Draw(img); logo(d, M, 64, accent=INK)
tag(d, "FOR OWNERS", "لأصحاب المحلات", bg=WHITE, fg=RED)
f = jak(800, 300); s = "0%"; ctext(d, 190, s, f, WHITE)
ctext(d, 540, "commission", jak(800, 76), WHITE)
ctext(d, 650, "بدون أي عمولة", ar(700, 56), WHITE, rtl=True)
d.rounded_rectangle((M, 790, W - M, 1090), radius=36, fill=(255, 255, 255))
d.text((M + 44, 820), "Free for 12 months", font=jak(800, 46), fill=INK)
d.text((M + 44, 890), "Then $25 per listing per month", font=jak(700, 40), fill=INK)
d.text((M + 44, 950), "Still 0% commission", font=jak(700, 40), fill=RED)
d.text((M + 44, 1020), "Limited to the first 10 places in each region", font=jak(600, 30), fill=(110, 110, 115))
para(d, 0, 1130, "مجاناً لمدة سنة، وبعدها خمسة وعشرين دولار بالشهر لكل محل، ومن دون أي عمولة، محدود لأول عشرة أماكن بكل منطقة", ar(600, 34), WHITE, W - 2 * M, 54, rtl=True, xr=W - M)
dots(d, 5, 3, color=WHITE)
save(img, 4)

# ---------- 5. CTA: your own link in your bio ----------
img = Image.new("RGB", (W, H), DARK); d = ImageDraw.Draw(img); logo(d, M, 64)
tag(d, "FOR OWNERS", "لأصحاب المحلات")
y = 215
y = para(d, M, y, "Put your own Weekendna link in your bio", jak(800, 66), WHITE, W - 2 * M, 84)
y += 20
y = para(d, 0, y, "حطّوا لينك صفحتكن عالبايو", ar(700, 56), (255, 205, 210), W - 2 * M, 84, rtl=True, xr=W - M)
# bio mock
d.rounded_rectangle((M, 560, W - M, 800), radius=32, fill=(40, 38, 44))
d.ellipse((M + 36, 592, M + 36 + 100, 592 + 100), fill=RED)
d.text((M + 36 + 50 - d.textlength("W", font=jak(800, 44)) / 2, 616), "W", font=jak(800, 44), fill=WHITE)
d.text((M + 170, 600), "Your place", font=jak(800, 38), fill=WHITE)
d.text((M + 170, 650), "Chalets, villas, guesthouses", font=jak(500, 28), fill=(190, 190, 195))
d.text((M + 36, 728), "weekendna.com/your-own-page", font=jak(700, 32), fill=(130, 175, 255))
y = 850
y = para(d, M, y, "Message us and we'll send you your personal link. Guests land straight on your page, not on our homepage.", jak(500, 36), WHITE, W - 2 * M, 52)
y += 14
para(d, 0, y, "ابعتولنا رسالة وبنبعتلكن لينككن الخاص، والضيف بيوصل مباشرة عصفحة محلكن", ar(600, 36), WHITE, W - 2 * M, 58, rtl=True, xr=W - M)
button(d, 1190, "Message @weekendna.lb")
save(img, 5)

# ---------- Story (9:16) ----------
SW, SH = 1080, 1920
img = Image.new("RGB", (SW, SH), RED); d = ImageDraw.Draw(img); logo(d, 72, 150, size=56, accent=INK)
y = 640
y = para(d, 72, y, "Owners: put your own Weekendna link in your bio", jak(800, 88), WHITE, SW - 144, 108)
y += 30
y = para(d, 0, y, "حطّوا لينك صفحتكن عالبايو", ar(700, 60), WHITE, SW - 144, 90, rtl=True, xr=SW - 72)
y += 50
d.text((72, y), "0% commission · free for 12 months", font=jak(700, 42), fill=WHITE); y += 66
d.text((72, y), "Limited to the first 10 places per region", font=jak(500, 36), fill=(255, 225, 228))
d.rounded_rectangle((72, 1540, SW - 72, 1636), radius=48, fill=WHITE)
t = "Message us for your link"; f = jak(800, 40)
d.text(((SW - d.textlength(t, font=f)) / 2, 1562), t, font=f, fill=RED)
u = "@weekendna.lb"; fu = jak(600, 34); d.text(((SW - d.textlength(u, font=fu)) / 2, 1680), u, font=fu, fill=WHITE)
img.save(os.path.join(POST, "story.jpg"), quality=92)
print("ok")
