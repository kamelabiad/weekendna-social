"""Prepare a new-style Reel: download a listing's full-size photos and build a numbered contact sheet, and/or
estimate a music track's tempo.

Usage:
  python3 tools/reel_prep.py photos <dest-dir> <listing-id> [<listing-id> ...]
      -> <dest-dir>/<id>-NN.webp (page order) and <dest-dir>/sheet.jpg (look at it to choose shots)
  python3 tools/reel_prep.py bpm <track.mp3> [--start SECONDS]
      -> tempo in BPM for reel.json
Photos come from weekendna.com listing pages (/uploads/listings/<id>/<hash>-1600.webp). Keep them out of the repo.
"""
import glob, os, re, subprocess, sys, urllib.request
import numpy as np

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 weekendna-reels"})
    with urllib.request.urlopen(req, timeout=60) as r: return r.read()

def photos(dest, ids):
    from PIL import Image, ImageDraw
    os.makedirs(dest, exist_ok=True)
    search = get("https://weekendna.com/en/search").decode("utf-8", "ignore")
    for lid in ids:
        m = re.search(rf'/en/stay/[a-z0-9-]+-{lid}(?=["/?])', search)
        page_url = "https://weekendna.com" + (m.group(0) if m else f"/en/stay/x-{lid}")
        page = get(page_url).decode("utf-8", "ignore")
        urls = list(dict.fromkeys(re.findall(rf"/uploads/listings/{lid}/[a-z0-9]+-1600\.webp", page)))
        for k, u in enumerate(urls, 1):
            p = os.path.join(dest, f"{lid}-{k:02d}.webp")
            if not os.path.exists(p): open(p, "wb").write(get("https://weekendna.com" + u))
        print(f"listing {lid}: {len(urls)} photos ({page_url})")
    fs = sorted(glob.glob(os.path.join(dest, "*.webp")))
    W, H, cols = 300, 200, 8
    sheet = Image.new("RGB", (cols * W, ((len(fs) + cols - 1) // cols) * H), "white")
    for k, f in enumerate(fs):
        im = Image.open(f).convert("RGB"); size = im.size; im.thumbnail((W - 6, H - 26))
        x, y = (k % cols) * W, (k // cols) * H
        sheet.paste(im, (x + 3, y + 22))
        ImageDraw.Draw(sheet).text((x + 5, y + 4), f"{os.path.basename(f)[:-5]}  {size[0]}x{size[1]}", fill="red")
    sheet.save(os.path.join(dest, "sheet.jpg"), quality=85)
    print("contact sheet:", os.path.join(dest, "sheet.jpg"))

def bpm(track, start=0.0):
    raw = subprocess.check_output(["ffmpeg", "-v", "error", "-ss", str(start), "-t", "40", "-i", track, "-ac", "1", "-ar", "22050", "-f", "s16le", "-"])
    x = np.frombuffer(raw, "<i2") / 32767; hop = 512; fps = 22050 / hop
    fr = np.lib.stride_tricks.sliding_window_view(x, 1024)[::hop]
    S = np.abs(np.fft.rfft(fr * np.hanning(1024), axis=1))
    fl = np.maximum(0, np.diff(np.log1p(S), axis=0)).sum(1); fl -= fl.mean()
    ac = np.correlate(fl, fl, "full")[len(fl) - 1:]; lags = np.arange(len(ac)) / fps
    m = (lags > 0.33) & (lags < 1.0); beat = lags[m][np.argmax(ac[m])]
    print(f"{60 / beat:.0f}")

if __name__ == "__main__":
    a = sys.argv[1:]
    if a[0] == "photos": photos(a[1], a[2:])
    elif a[0] == "bpm": bpm(a[1], float(a[a.index("--start") + 1]) if "--start" in a else 0.0)
