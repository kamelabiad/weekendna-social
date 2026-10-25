"""Publishes everything in posts/log.json that is due today (UK date): the feed post (carousel or Reel), the Weekendna story,
and the Reel version of a carousel on its reel_date. Marks each item published in the log as soon as it is live.

Usage: IG_TOKEN=... python3 tools/publish_due.py [--date YYYY-MM-DD] [--dry-run]
Images and videos must already be pushed to GitHub (they are fetched from raw.githubusercontent.com by Instagram).
Prints a short report (one line per item) at the end; exit code 1 if anything failed.
"""
import datetime, glob, json, os, sys, time, urllib.parse, urllib.request
from zoneinfo import ZoneInfo

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
LOG = os.path.join(ROOT, "posts", "log.json")
RAW = "https://raw.githubusercontent.com/kamelabiad/weekendna-social/main/posts"
API = "https://graph.instagram.com/v21.0"
IG = "17841412894685016"
TOKEN = os.environ.get("IG_TOKEN") or sys.exit("set IG_TOKEN")
args = sys.argv[1:]
DRY = "--dry-run" in args
TODAY = args[args.index("--date") + 1] if "--date" in args else datetime.datetime.now(ZoneInfo("Europe/London")).date().isoformat()

def call(path, data=None, method=None):
    url = f"{API}/{path}"
    if data is None:
        url += ("&" if "?" in url else "?") + "access_token=" + urllib.parse.quote(TOKEN)
        req = urllib.request.Request(url, method=method or "GET")
    else:
        req = urllib.request.Request(url, data=urllib.parse.urlencode({**data, "access_token": TOKEN}).encode(), method="POST")
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        raise RuntimeError(json.load(e).get("error", {}).get("message", str(e)))

def wait_ready(cid, tries=60):
    for _ in range(tries):
        s = call(f"{cid}?fields=status_code").get("status_code")
        if s == "FINISHED": return
        if s in ("ERROR", "EXPIRED"): raise RuntimeError(f"Instagram could not process the media ({s})")
        time.sleep(6)
    raise RuntimeError("Instagram took too long to process the media")

def publish(cid):
    wait_ready(cid)
    mid = call(f"{IG}/media_publish", {"creation_id": cid})["id"]
    return call(f"{mid}?fields=permalink")["permalink"]

def already_posted(caption, product):
    """True when one of the last posts of the same kind (FEED or REELS) has the same caption start
    (guards against double posting after a crash). A carousel's Reel shares its caption, so the kind matters."""
    head = caption.strip()[:80]
    recent = call(f"{IG}/media?fields=caption,media_product_type&limit=10").get("data", [])
    return any((m.get("caption") or "").strip()[:80] == head and m.get("media_product_type") == product for m in recent)

def caption_of(folder):
    with open(os.path.join(ROOT, "posts", folder, "caption.txt"), encoding="utf-8") as f: return f.read().strip()

def carousel(folder, collab):
    slides = sorted(os.path.basename(p) for p in glob.glob(os.path.join(ROOT, "posts", folder, "*-[0-9].jpg")))
    if not 2 <= len(slides) <= 10: raise RuntimeError(f"{len(slides)} slides in {folder}")
    cap = caption_of(folder)
    if already_posted(cap, "FEED"): return "already on Instagram"
    kids = []
    for i, s in enumerate(slides):
        d = {"image_url": f"{RAW}/{folder}/{s}", "is_carousel_item": "true"}
        if i == 0 and collab: d["user_tags"] = json.dumps([{"username": collab, "x": 0.5, "y": 0.45}])
        kids.append(call(f"{IG}/media", d)["id"])
    d = {"media_type": "CAROUSEL", "children": ",".join(kids), "caption": cap}
    if collab: d["collaborators"] = json.dumps([collab])
    return publish(call(f"{IG}/media", d)["id"])

def reel(folder, video, collab, caption, to_feed):
    if already_posted(caption, "REELS"): return "already on Instagram"
    d = {"media_type": "REELS", "video_url": f"{RAW}/{folder}/{video}", "caption": caption, "share_to_feed": "true" if to_feed else "false",
         "thumb_offset": "1000"}  # cover = frame at 1.0s: Remotion Reels start on a black frame 0, which made black previews
    if collab: d["collaborators"] = json.dumps([collab])
    return publish(call(f"{IG}/media", d)["id"])

def story(folder):
    return publish(call(f"{IG}/media", {"media_type": "STORIES", "image_url": f"{RAW}/{folder}/story.jpg"})["id"])

def save(log):
    with open(LOG, "w", encoding="utf-8") as f: json.dump(log, f, indent=2, ensure_ascii=False); f.write("\n")

log = json.load(open(LOG, encoding="utf-8"))
report, failed = [], False
for p in log["posts"]:
    folder, collab = p.get("folder"), p.get("instagram")
    jobs = []
    if p.get("date") == TODAY and p.get("status") == "scheduled":
        jobs.append(("post", lambda: reel(folder, p["video"], collab, caption_of(folder), True) if p.get("type") == "reel" else carousel(folder, collab)))
    if p.get("date") == TODAY and p.get("story_status") == "scheduled":
        jobs.append(("story", lambda: story(folder)))
    if p.get("reel_date") == TODAY and p.get("reel_status") == "scheduled":
        jobs.append(("reel", lambda: reel(folder, "reel.mp4", collab, caption_of(folder), False)))
    for kind, job in jobs:
        name = f"{p['owner']} ({kind})"
        if DRY: report.append(f"WOULD PUBLISH {name}"); continue
        try:
            link = job()
            key = {"post": "status", "story": "story_status", "reel": "reel_status"}[kind]
            p[key] = "published"
            if kind == "post": p["permalink"] = link
            if kind == "reel": p["reel_permalink"] = link
            save(log)
            report.append(f"OK {name}: {link}")
        except Exception as e:
            failed = True
            report.append(f"FAILED {name}: {e}")
if not report: report.append(f"Nothing due on {TODAY}.")
print("\n".join(report))
sys.exit(1 if failed else 0)
