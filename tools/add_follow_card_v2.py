"""Weekendna-as-hero overlays for a finished Reel (30 Oct 2026 design): a big red "Found on Weekendna" tag from 0.2s, and a red end card
(headline, benefit line, white "Comment <KEYWORD>" card, big Follow button, "New places every week"). Audio untouched.

Usage: python3 tools/add_follow_card_v2.py <post-folder> "<Place>" <KEYWORD> "<benefit line EN>" "<benefit line AR>" "<footer line AR hook>"
  e.g. python3 tools/add_follow_card_v2.py 2026-10-majestic-byblos Byblos BYBLOS "Sea views + private balcony, from \\$130" "ويكندكن بجبيل بيبلش من هون"
Reads posts/<folder>/reel-remotion.mp4 (or reel.mp4), writes reel.mp4. Run `source tools/setup.sh` first. Arabic text must not contain Latin letters."""
import os, subprocess, sys, tempfile
sys.path.insert(0, os.path.dirname(__file__))
from brand import *
folder, place, kw, benefit, benefit_ar = sys.argv[1:6]
POST = os.path.join(os.path.dirname(__file__), "..", "posts", folder)
src = os.path.join(POST, "reel-remotion.mp4")
if not os.path.exists(src): src = os.path.join(POST, "reel.mp4")
dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src]).strip())
SW, SH = 1080, 1920; tmp = tempfile.mkdtemp(); END = 3.2
def sc(d, y, t, f, fill, rtl=False):
    w = d.textlength(t, font=f, direction="rtl" if rtl else None); d.text(((SW - w) / 2, y), t, font=f, fill=fill, direction="rtl" if rtl else None)
im = Image.new("RGB", (SW, SH), RED); d = ImageDraw.Draw(im); logo(d, M, 150, accent=INK, size=64)
pf = jak(700, 40); pt = "Found on Weekendna"; pw = d.textlength(pt, font=pf); pill(d, int((SW - pw) / 2 - 28), 290, pt, pf, fg=RED, bg=WHITE, pad=(28, 14))
sc(d, 410, f"Your {place}", jak(800, 110), WHITE); sc(d, 540, "weekend starts here", jak(800, 84), WHITE)
sc(d, 680, benefit, jak(500, 40), WHITE); sc(d, 750, benefit_ar, ar(700, 46), WHITE, rtl=True)
d.rounded_rectangle((80, 870, SW - 80, 1190), radius=44, fill=WHITE)
sc(d, 900, "Want this place?", jak(800, 54), RED)
sc(d, 990, f"Comment {kw} and we'll", jak(800, 52), INK); sc(d, 1055, "check availability for you", jak(800, 52), INK)
sc(d, 1128, "بدك هالمكان؟ اكتبلنا بالتعليق وبنتأكدلك", ar(600, 34), (90, 90, 90), rtl=True)
f = jak(800, 62); t = "Follow @weekendna.lb"; w = d.textlength(t, font=f)
d.rounded_rectangle(((SW - w) / 2 - 64, 1250, (SW + w) / 2 + 64, 1390), radius=70, fill=INK)
bb = f.getbbox(t); d.text(((SW - w) / 2, 1250 + (140 - (bb[3] - bb[1])) / 2 - bb[1]), t, font=f, fill=WHITE)
sc(d, 1440, "New places every week", jak(800, 64), WHITE); sc(d, 1530, "تابعونا، كل أسبوع محل جديد", ar(700, 46), WHITE, rtl=True)
sc(d, 1680, "Request your dates on WhatsApp · nothing to pay yet · link in bio", jak(500, 28), (255, 228, 230))
im.save(f"{tmp}/end.png")
tg = Image.new("RGBA", (SW, SH), (0, 0, 0, 0)); d = ImageDraw.Draw(tg)
f = jak(800, 44); w = d.textlength(pt, font=f)
d.rounded_rectangle((M, 240, M + w + 64, 330), radius=45, fill=(224, 38, 59, 245)); d.text((M + 32, 262), pt, font=f, fill=WHITE)
tg.save(f"{tmp}/tag.png")
out = os.path.join(POST, "reel.mp4"); tmpout = f"{tmp}/out.mp4"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-loop", "1", "-i", f"{tmp}/end.png", "-loop", "1", "-i", f"{tmp}/tag.png", "-filter_complex",
    f"[0:v][2:v]overlay=enable='between(t,0.2,{dur - END:.2f})'[a];[a][1:v]overlay=enable='gte(t,{dur - END:.2f})',format=yuv420p[v]", "-map", "[v]", "-map", "0:a",
    "-t", f"{dur:.2f}", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-c:a", "copy", "-movflags", "+faststart", tmpout], check=True)
__import__("shutil").move(tmpout, out); print("wrote", out, "dur", dur)
