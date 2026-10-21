"""Owner kit for one post: a 9:16 story image (Instagram story / WhatsApp status) and a 9:16 Reel video from the carousel slides.

Usage: python3 tools/make_kit.py <post-folder> <listing-url-path> "<Owner name>" "<hook EN>" "<hook AR>" <hero-photo> [more photos...]
  e.g. python3 tools/make_kit.py 2026-11-acampar /en/stay/acampar-studio-bungalow-faraya-mzaar-39 "Acampar" \
         "Cosy wooden bungalows in Faraya" "بنغلوهات خشب دافية بفاريا" photo1.webp photo2.webp
Writes story.jpg and reel.mp4 into posts/<post-folder>/ (reel uses that folder's carousel slides <prefix>-N.jpg).
Needs ffmpeg and the fonts from tools/setup.sh.
"""
import glob, os, subprocess, sys, tempfile
sys.path.insert(0, os.path.dirname(__file__))
from brand import *

folder, path, name, hook_en, hook_ar, *photos = sys.argv[1:]
POST = os.path.join(os.path.dirname(__file__), "..", "posts", folder)
SW, SH = 1080, 1920

# ---------- Story (also fine as a WhatsApp status) ----------
img = Image.new("RGB", (SW, SH), (12, 12, 14))
src = Image.open(photos[0]).convert("RGB")
r = max(SW / src.width, SH / src.height); hero = src.resize((round(src.width * r), round(src.height * r)), Image.LANCZOS)
hero = hero.crop(((hero.width - SW) // 2, (hero.height - SH) // 2, (hero.width + SW) // 2, (hero.height + SH) // 2))
if src.width >= 900:
    img.paste(hero, (0, 0))
else:
    # Small photo: blurred background plus the photo in a rounded frame, so it isn't stretched and blurry.
    img = Image.blend(hero.filter(ImageFilter.GaussianBlur(36)), Image.new("RGB", (SW, SH), (12, 12, 14)), 0.4)
    fw = SW - 2 * 90; fh = min(860, round(src.height * fw / src.width)); fw = min(fw, round(src.width * fh / src.height))
    card = src.resize((fw, fh), Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=1.2, percent=60, threshold=2))
    m = Image.new("L", (fw, fh), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, fw, fh), radius=36, fill=255)
    img.paste(card, ((SW - fw) // 2, 260 + (860 - fh) // 2), m)
g = Image.new("L", (1, SH))
for y in range(SH):
    t = y / (SH - 1); g.putpixel((0, y), int(150 * (1 - t / 0.25)) if t < 0.25 else int(235 * ((t - 0.45) / 0.55) ** 1.3) if t > 0.45 else 0)
img.paste(Image.new("RGB", (SW, SH), (12, 12, 14)), (0, 0), g.resize((SW, SH)))
d = ImageDraw.Draw(img)
logo(d, 72, 150, size=56)
d.text((72, 1150), "Now on Weekendna", font=jak(700, 40), fill=(255, 255, 255))
d.text((72, 1210), name, font=jak(800, 104 if len(name) < 14 else 76), fill=WHITE)
d.text((72, 1350), hook_en, font=jak(500, 40), fill=WHITE)
w = d.textlength(hook_ar, font=ar(700, 44), direction="rtl"); d.text((SW - 72 - w, 1420), hook_ar, font=ar(700, 44), fill=WHITE, direction="rtl")
t = "Book on WhatsApp"; f = jak(800, 40); ta = "احجزو عالواتساب"; fa = ar(700, 40)
bw = d.textlength(t, font=f); aw = d.textlength(ta, font=fa, direction="rtl"); gap = 28; tw = bw + gap + aw
d.rounded_rectangle(((SW - tw) / 2 - 48, 1556, (SW + tw) / 2 + 48, 1652), radius=48, fill=RED)
d.text(((SW - tw) / 2, 1578), t, font=f, fill=WHITE)
d.text(((SW - tw) / 2 + bw + gap, 1566), ta, font=fa, fill=WHITE, direction="rtl")
u = "weekendna.com · link in bio"; fu = jak(500, 32); uw = d.textlength(u, font=fu)
d.text(((SW - uw) / 2, 1690), u, font=fu, fill=(235, 235, 235))
img.save(os.path.join(POST, "story.jpg"), quality=92)

# ---------- Reel: each carousel slide on a blurred 9:16 background, slow zoom, ~3s each ----------
slides = sorted(glob.glob(os.path.join(POST, "*-[0-9].jpg")))
tmp = tempfile.mkdtemp()
for i, s in enumerate(slides):
    im = Image.open(s).convert("RGB")
    bg = im.resize((SW, round(im.height * SW / im.width))).resize((SW, SH)).filter(ImageFilter.GaussianBlur(40))
    bg = Image.blend(bg, Image.new("RGB", (SW, SH), (12, 12, 14)), 0.35)
    bg.paste(im, (0, (SH - im.height) // 2))
    bg.save(f"{tmp}/f{i}.png")
parts = []
for i in range(len(slides)):
    out = f"{tmp}/c{i}.mp4"; parts.append(out)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", f"{tmp}/f{i}.png", "-vf",
        "scale=1188:2112,zoompan=z='min(1+0.0012*on,1.1)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=90:s=1080x1920:fps=30,format=yuv420p",
        "-frames:v", "90", "-c:v", "libx264", "-preset", "medium", "-crf", "20", out], check=True)
lst = f"{tmp}/list.txt"; open(lst, "w").write("".join(f"file '{p}'\n" for p in parts))
# A silent audio track for now; run tools/add_music.py <folder> <mood> afterwards to put original music on it.
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
    "-shortest", "-c:v", "copy", "-c:a", "aac", "-b:a", "96k", "-movflags", "+faststart", os.path.join(POST, "reel.mp4")], check=True)
print("story.jpg and reel.mp4 written to", POST)
