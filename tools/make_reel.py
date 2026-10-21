"""Proper 9:16 Reel from listing photos: full-screen shots cut on the music's beat, varied camera moves,
quick transitions, animated text (hook, name, facts) and an end card. Replaces the old slideshow reel.mp4.

Usage: source tools/setup.sh; python3 tools/make_reel.py posts/<folder>/reel.json
reel.json (kept in the post folder):
{
  "music": "/tmp/music/calm-acoustic-andriig.mp3", "start": 0,      # decrypted track (see music/README.md)
  "bpm": 123,                                                         # tempo of the track (estimate with tools/bpm.py)
  "photos_dir": "/tmp/ghosta-src",                                    # downloaded listing photos (not committed)
  "shots": [                                                          # in order; first = hook, last = end card
    {"photo": "14.webp", "beats": 5, "move": "zoom_in", "text": {"type": "hook", "en": "...", "ar": "..."}},
    {"photo": "20.webp", "beats": 3, "move": "pan_left", "text": {"type": "title", "name": "...", "pill": "..."}},
    {"photo": "17.webp", "beats": 3, "move": "pan_right", "text": {"type": "fact", "en": "...", "ar": "..."}},
    {"photo": "26.webp", "beats": 6, "move": "zoom_out", "text": {"type": "end", "price": "From $220/night"}}
  ]
}
moves: zoom_in, zoom_out, pan_left, pan_right, pan_up, pan_down. Optional "fx"/"fy" (0-1) = point of interest.
Transitions alternate: whip (fast slide with motion blur), cut-with-punch-zoom, and a short crossfade into the end card.
"""
import json, math, os, subprocess, sys, tempfile
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from brand import *

spec = json.load(open(sys.argv[1]))
FOLDER = os.path.dirname(os.path.abspath(sys.argv[1]))
RW, RH, FPS = 1080, 1920, 30
BEAT = 60 / spec["bpm"]
shots = spec["shots"]

def ease(t): return 0.5 - 0.5 * math.cos(math.pi * min(1, max(0, t)))
def ease_out(t): t = min(1, max(0, t)); return 1 - (1 - t) ** 3
def back_out(t):
    t = min(1, max(0, t)); c = 1.4
    return 1 + (c + 1) * (t - 1) ** 3 + c * (t - 1) ** 2

# ---------- photos: pre-scale so that the 9:16 frame covers them with room to move ----------
def trim_bars(im):
    """Remove black letterbox/pillarbox bars that some owners' photos have."""
    a = np.asarray(im.convert("L")).astype(int)
    rows = np.where(a.mean(1) > 14)[0]; cols = np.where(a.mean(0) > 14)[0]
    if len(rows) and len(cols): im = im.crop((cols[0], rows[0], cols[-1] + 1, rows[-1] + 1))
    return im

def load(s):
    im = trim_bars(Image.open(os.path.join(spec["photos_dir"], s["photo"])).convert("RGB"))
    small = s.get("frame", max(RW / im.width, RH / im.height) > 2.3)  # would need >2.3x upscale: show framed instead
    s["_frame"] = small
    if small:
        return im.filter(ImageFilter.UnsharpMask(radius=1.2, percent=50, threshold=2))
    k = 1.18 * max(RW / im.width, RH / im.height)
    im = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
    return im.filter(ImageFilter.UnsharpMask(radius=2, percent=70, threshold=2))
imgs = [load(s) for s in shots]

_bg_cache = {}
def framed(i, t):
    """Low-resolution photo: sharp rounded card over a blurred copy of itself, slow zoom + drift."""
    im, s = imgs[i], shots[i]
    if i not in _bg_cache:
        bg = im.copy(); r = max(RW / bg.width, RH / bg.height)
        bg = bg.resize((round(bg.width * r * 1.15), round(bg.height * r * 1.15))).filter(ImageFilter.GaussianBlur(45))
        bg = Image.blend(bg, Image.new("RGB", bg.size, (10, 10, 12)), 0.35)
        cw = RW - 2 * 64; ch = round(im.height * cw / im.width)
        if ch > 950: ch = 950; cw = round(im.width * ch / im.height)
        card = im.resize((cw, ch), Image.LANCZOS)
        _bg_cache[i] = (bg, card)
    bg, card = _bg_cache[i]; e = ease(t)
    ox = (bg.width - RW) / 2 + (bg.width - RW) * 0.3 * (e - 0.5); oy = (bg.height - RH) / 2
    f = bg.crop((int(ox), int(oy), int(ox) + RW, int(oy) + RH))
    z = 1.0 + 0.06 * e; cw, ch = round(card.width * z), round(card.height * z)
    c = card.resize((cw, ch), Image.BILINEAR)
    m = Image.new("L", (cw, ch), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, cw - 1, ch - 1), radius=40, fill=255)
    cx, cy = (RW - cw) // 2, int(760 - ch / 2) if ch < 900 else 150
    sh = Image.new("L", (RW, RH), 0); ImageDraw.Draw(sh).rounded_rectangle((cx + 10, cy + 24, cx + cw + 10, cy + ch + 24), radius=44, fill=150)
    f.paste((0, 0, 0), (0, 0), sh.filter(ImageFilter.GaussianBlur(26)))
    f.paste(c, (cx, cy), m)
    return f

def camera(i, t):
    """Frame of shot i at progress t (0-1) of its own duration, as an RGB image."""
    im, s = imgs[i], shots[i]
    if s.get("_frame"): return framed(i, t)
    mv = s.get("move", "zoom_in"); fx, fy = s.get("fx", 0.5), s.get("fy", 0.5)
    e = ease(t) if mv.startswith("pan") else t
    base = max(RW / im.width, RH / im.height)          # scale where the frame just covers the photo
    z = {"zoom_in": 1.0 + 0.14 * e, "zoom_out": 1.14 - 0.14 * e}.get(mv, 1.06)
    sc = base * z                                        # photo px -> frame px
    vw, vh = RW / sc, RH / sc                            # visible window in photo px
    mx, my = im.width - vw, im.height - vh
    x, y = fx * mx, fy * my
    if mv == "pan_left": x = mx * (0.85 - 0.7 * e)
    if mv == "pan_right": x = mx * (0.15 + 0.7 * e)
    if mv == "pan_up": y = my * (0.85 - 0.7 * e)
    if mv == "pan_down": y = my * (0.15 + 0.7 * e)
    return im.transform((RW, RH), Image.AFFINE, (1 / sc, 0, x, 0, 1 / sc, y), resample=Image.BICUBIC)

# ---------- shading so white text always reads ----------
def grad_mask(h, a0, a1, k=1.5):
    g = np.linspace(0, 1, h) ** k; return Image.fromarray((a0 + (a1 - a0) * g).astype("uint8")[:, None].repeat(RW, 1))
DARK = Image.new("RGB", (RW, RH), (10, 10, 12))
TOP = grad_mask(420, 150, 0, 0.8); BOT = grad_mask(1150, 0, 235, 1.0)
def shade_frame(f, strong=False):
    f.paste(DARK.crop((0, 0, RW, 420)), (0, 0), TOP)
    f.paste(DARK.crop((0, 0, RW, 1150)), (0, RH - 1150), BOT)
    if strong: f = Image.blend(f, DARK, 0.35)
    return f

# ---------- text animation ----------
SAFE_B = 1500  # keep text above Instagram's caption/buttons area
def fade_text(layer, xy, text, font, t, delay=0.0, dur=0.35, fill=WHITE, rtl=False, rise=40, shadow=True):
    p = ease_out((t - delay) / dur)
    if p <= 0: return
    x, y = xy; y += rise * (1 - p); a = int(255 * p)
    d = ImageDraw.Draw(layer)
    kw = {"direction": "rtl"} if rtl else {}
    if shadow: d.text((x + 2, y + 3), text, font=font, fill=(0, 0, 0, int(a * 0.45)), **kw)
    d.text((x, y), text, font=font, fill=fill[:3] + (a,), **kw)

def tw(text, font, rtl=False):
    return ImageDraw.Draw(Image.new("L", (1, 1))).textlength(text, font=font, direction="rtl" if rtl else None)

def wrap(text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        if tw((cur + " " + w).strip(), font) <= maxw: cur = (cur + " " + w).strip()
        else: lines.append(cur); cur = w
    return lines + [cur]

def draw_text(frame, s, t_sec, dur):
    tx = s.get("text")
    layer = Image.new("RGBA", (RW, RH), (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    if not tx: return frame
    ty = tx["type"]
    if ty == "hook":
        logo(d, M, 150, size=48)
        f = jak(800, 92); lines = wrap(tx["en"], f, RW - 2 * M); y = SAFE_B - 210 - 104 * len(lines)
        for k, ln in enumerate(lines): fade_text(layer, (M, y + 104 * k), ln, f, t_sec, delay=0.15 + 0.12 * k)
        fa = ar(700, 54); fade_text(layer, (RW - M - tw(tx["ar"], fa, True), y + 104 * len(lines) + 28), tx["ar"], fa, t_sec, delay=0.55, rtl=True)
    elif ty == "title":
        fp = jak(700, 36); pt = tx["pill"]; pw = tw(pt, fp) + 48
        p = back_out(t_sec / 0.4)
        if p > 0:
            ImageDraw.Draw(layer).rounded_rectangle((M, SAFE_B - 300, M + pw * p, SAFE_B - 236), radius=34, fill=RED + (255,))
            if p > 0.8: fade_text(layer, (M + 24, SAFE_B - 290), pt, fp, t_sec, delay=0.25, dur=0.2, rise=0, shadow=False)
        f = jak(800, 104 if len(tx["name"]) < 16 else 84)
        for k, ln in enumerate(wrap(tx["name"], f, RW - 2 * M)):
            fade_text(layer, (M, SAFE_B - 210 + 110 * k), ln, f, t_sec, delay=0.2 + 0.1 * k)
    elif ty == "fact":
        f = jak(800, 70); lines = wrap(tx["en"], f, RW - 2 * M); y = SAFE_B - 120 - 84 * len(lines)
        # red accent bar grows in
        p = ease_out(t_sec / 0.3); ImageDraw.Draw(layer).rectangle((M, y - 34, M + 90 * p, y - 24), fill=RED + (255,))
        for k, ln in enumerate(lines): fade_text(layer, (M, y + 84 * k), ln, f, t_sec, delay=0.1 + 0.1 * k)
        if tx.get("ar"):
            fa = ar(700, 50); fade_text(layer, (RW - M - tw(tx["ar"], fa, True), y + 84 * len(lines) + 20), tx["ar"], fa, t_sec, delay=0.35, rtl=True)
    elif ty == "end":
        p = ease_out(t_sec / 0.5)
        logo(ImageDraw.Draw(layer), (RW - tw("weekend", out(700, 96)) - 60) / 2, 560 - 30 * (1 - p), size=96)
        if p < 1:  # fade the logo in
            a = layer.getchannel("A").point(lambda v: int(v * p)); layer.putalpha(a)
        fn = jak(800, 64); nm = tx.get("name", "")
        if nm: fade_text(layer, ((RW - tw(nm, fn)) / 2, 760), nm, fn, t_sec, delay=0.2)
        if tx.get("price"):
            fpz = jak(600, 48); fade_text(layer, ((RW - tw(tx["price"], fpz)) / 2, 850), tx["price"], fpz, t_sec, delay=0.35)
        # WhatsApp button pops in
        b = back_out((t_sec - 0.6) / 0.45)
        if b > 0:
            t1, t2 = "Book on WhatsApp", "احجزو عالواتساب"; f1, f2 = jak(800, 46), ar(700, 46)
            w = tw(t1, f1) + 30 + tw(t2, f2, True); bw, bh = (w + 110) * b, 110 * b; cx, cy = RW / 2, 1080
            ImageDraw.Draw(layer).rounded_rectangle((cx - bw / 2, cy - bh / 2, cx + bw / 2, cy + bh / 2), radius=int(55 * b), fill=RED + (255,))
            if b > 0.9:
                d2 = ImageDraw.Draw(layer); x0 = cx - w / 2
                d2.text((x0, cy - 30), t1, font=f1, fill=WHITE); d2.text((x0 + tw(t1, f1) + 30, cy - 42), t2, font=f2, fill=WHITE, direction="rtl")
        fu = jak(600, 40); u = "weekendna.com · link in bio"
        fade_text(layer, ((RW - tw(u, fu)) / 2, 1190), u, fu, t_sec, delay=1.0)
    out_ = frame.convert("RGBA"); out_.alpha_composite(layer); return out_.convert("RGB")

# ---------- timeline ----------
durs = [s["beats"] * BEAT for s in shots]
starts = np.concatenate([[0], np.cumsum(durs)])
total = starts[-1]
TR = 0.22  # transition length (s), centred on the cut so the cut lands on the beat

def shot_frame(i, t_abs):
    t_local = t_abs - starts[i]
    tt = (t_local + TR) / (durs[i] + 2 * TR)   # motion runs through the transitions too
    f = camera(i, tt)
    f = shade_frame(f, strong=shots[i].get("text", {}).get("type") == "end")
    return draw_text(f, shots[i], t_local, durs[i])

def whip(a, b, p, direction):
    """Fast horizontal slide with motion blur between frames a and b (p 0-1)."""
    e = ease(p); off = int(RW * e) * direction
    canvas = Image.new("RGB", (RW, RH))
    canvas.paste(a, (-off, 0)); canvas.paste(b, (RW * direction - off, 0))
    blur = int(40 * math.sin(math.pi * p))
    if blur > 2:
        arr = np.asarray(canvas).astype(np.float32); k = blur
        cs = np.cumsum(np.pad(arr, ((0, 0), (k, k), (0, 0)), mode="edge"), axis=1)
        arr = (cs[:, 2 * k:] - cs[:, :-2 * k]) / (2 * k)
        canvas = Image.fromarray(arr[:, :RW].clip(0, 255).astype("uint8"))
    return canvas

def render():
    tmp = tempfile.mkdtemp(); video = os.path.join(tmp, "v.mp4")
    ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{RW}x{RH}", "-r", str(FPS), "-i", "-",
                           "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p", video], stdin=subprocess.PIPE)
    n = int(round(total * FPS))
    for k in range(n):
        t = k / FPS
        i = min(len(shots) - 1, int(np.searchsorted(starts, t, side="right") - 1))
        frame = None
        # inside a transition window around a cut?
        for c in range(1, len(shots)):
            if abs(t - starts[c]) < TR / 2 + 1e-9 and c < len(shots):
                p = (t - (starts[c] - TR / 2)) / TR
                a, b = shot_frame(c - 1, t), shot_frame(c, t)
                last = c == len(shots) - 1
                if last: frame = Image.blend(a, b, ease(p))                         # soft into the end card
                elif c % 2 == 1: frame = whip(a, b, p, 1 if (c // 2) % 2 == 0 else -1)
                else:                                                                 # cut with a punch zoom on b
                    frame = b if p >= 0.5 else a
                    if p >= 0.5:
                        z = 1 + 0.06 * (1 - ease_out((p - 0.5) * 2))
                        cw, ch = RW / z, RH / z
                        frame = frame.crop(((RW - cw) / 2, (RH - ch) / 2, (RW + cw) / 2, (RH + ch) / 2)).resize((RW, RH), Image.BILINEAR)
                break
        if frame is None: frame = shot_frame(i, t)
        if k < 6: frame = Image.blend(Image.new("RGB", (RW, RH)), frame, k / 6)       # fade in from black
        ff.stdin.write(frame.tobytes())
        if k % 60 == 0: print(f"frame {k}/{n}", flush=True)
    ff.stdin.close(); ff.wait()
    out = os.path.join(FOLDER, "reel.mp4")
    af = f"afade=t=in:d=0.3,afade=t=out:st={total - 1.2:.2f}:d=1.2,loudnorm=I=-16:TP=-1.5:LRA=11"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", video, "-ss", str(spec.get("start", 0)), "-t", f"{total:.2f}", "-i", spec["music"],
                    "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-af", af, "-ar", "44100", "-ac", "2", "-c:a", "aac", "-b:a", "160k",
                    "-shortest", "-movflags", "+faststart", out], check=True)
    print(f"reel.mp4 written ({total:.1f}s, {len(shots)} shots)")

if __name__ == "__main__":
    if "--still" in sys.argv:  # preview stills at the middle of each shot
        for i in range(len(shots)):
            shot_frame(i, starts[i] + durs[i] * 0.8).save(os.path.join(tempfile.gettempdir(), f"still{i}.jpg"), quality=85)
        print("stills in", tempfile.gettempdir())
    else:
        render()
