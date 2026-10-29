"""Add Weekendna's follow overlays to a finished Reel: a small "Follow @weekendna.lb" tag in the first 2.5s and a full red end card
(name, price, big Follow button) over the last ~2.5s. Audio is untouched.

Usage: python3 tools/add_follow_card.py <post-folder> "<Name>" "<from $X / night>"   (reads posts/<folder>/reel-remotion.mp4 or reel.mp4, writes reel.mp4)
Run `source tools/setup.sh` first for the fonts. Arabic text never contains the Latin handle (renders as empty boxes).
"""
import os, subprocess, sys, tempfile
sys.path.insert(0, os.path.dirname(__file__))
from brand import *
folder, name, price = sys.argv[1:4]
POST = os.path.join(os.path.dirname(__file__), "..", "posts", folder)
src = os.path.join(POST, "reel-remotion.mp4")
if not os.path.exists(src): src = os.path.join(POST, "reel.mp4")
dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src]).strip())
SW, SH = 1080, 1920
tmp = tempfile.mkdtemp()
im = Image.new("RGB", (SW, SH), RED); d = ImageDraw.Draw(im); logo(d, M, 150, accent=INK, size=64)
fn = jak(800, 84 if len(name) < 20 else 64); w = d.textlength(name, font=fn); d.text(((SW - w) / 2, 640), name, font=fn, fill=WHITE)
fp = jak(800, 56); w = d.textlength(price, font=fp); d.text(((SW - w) / 2, 760), price, font=fp, fill=WHITE)
f = jak(800, 64); t = "Follow @weekendna.lb"; w = d.textlength(t, font=f)
d.rounded_rectangle(((SW - w) / 2 - 60, 930, (SW + w) / 2 + 60, 1060), radius=65, fill=WHITE); d.text(((SW - w) / 2, 955), t, font=f, fill=RED)
f2 = jak(700, 44); t2 = "A new place to escape to every week"; w2 = d.textlength(t2, font=f2); d.text(((SW - w2) / 2, 1130), t2, font=f2, fill=WHITE)
f3 = ar(700, 52); t3 = "تابعونا، كل أسبوع محل جديد"; w3 = d.textlength(t3, font=f3, direction="rtl"); d.text(((SW - w3) / 2, 1210), t3, font=f3, fill=WHITE, direction="rtl")
im.save(f"{tmp}/end.png")
tg = Image.new("RGBA", (SW, SH), (0, 0, 0, 0)); d = ImageDraw.Draw(tg)
f = jak(800, 38); w = d.textlength(t, font=jak(800, 38))
d.rounded_rectangle((SW - w - 110, 230, SW - 50, 306), radius=38, fill=(224, 38, 59, 235)); d.text((SW - w - 80, 246), t, font=f, fill=WHITE)
tg.save(f"{tmp}/tag.png")
out = os.path.join(POST, "reel.mp4")
tmpout = f"{tmp}/out.mp4"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-loop", "1", "-i", f"{tmp}/end.png", "-loop", "1", "-i", f"{tmp}/tag.png", "-filter_complex",
    f"[0:v][2:v]overlay=enable='between(t,0.2,2.6)'[a];[a][1:v]overlay=enable='gte(t,{dur - 2.6:.2f})',format=yuv420p[v]", "-map", "[v]", "-map", "0:a",
    "-t", f"{dur:.2f}", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-c:a", "copy", "-movflags", "+faststart", tmpout], check=True)
os.replace(tmpout, out) if os.path.dirname(tmpout) == os.path.dirname(out) else __import__("shutil").move(tmpout, out)
print("wrote", out)
