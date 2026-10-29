"""Check a post's prices against the live weekendna.com listings before it is published.

Usage: python3 tools/verify_post.py <post-folder>        (exit 1 and print the problems if any price in the caption or Reel text is not on the listing)
Reads listing_ids from posts/log.json, fetches each listing from api.weekendna.com and compares every dollar amount in caption.txt and
reel-remotion.json (Arabic digits and "دولار" too) with that owner's listing prices (nightly, weekend, day use, monthly) and with
"per person" amounts (nightly price / max guests, rounded). Posts without listing_ids (brand posts) are skipped.
Also prints each listing's facts so a human can compare the text by eye.
"""
import json, os, re, sys, urllib.request
API = "https://api.weekendna.com/api/v1"
ROOT = os.path.join(os.path.dirname(__file__), "..")
def get(path):
    with urllib.request.urlopen(urllib.request.Request(f"{API}/{path}", headers={"User-Agent": "weekendna-verify"}), timeout=30) as r:
        return json.load(r)
def check(folder, quiet=False):
    log = json.load(open(os.path.join(ROOT, "posts", "log.json"), encoding="utf-8"))
    post = next((p for p in log["posts"] if p.get("folder") == folder), None)
    if not post or not post.get("listing_ids"): return []
    items = get("listings?limit=200")["items"]; slugs = {i["id"]: i["slug"] for i in items}
    allowed, facts = set(), []
    for lid in post["listing_ids"]:
        if lid not in slugs: return [f"listing {lid} not found on the site"]
        d = get(f"listings/{slugs[lid]}")
        guests = d.get("maxGuests") or 0
        for k in ("basePricePerNight", "weekendPrice", "dayUsePrice", "monthlyPrice"):
            if d.get(k): allowed.add(round(d[k]))
        if d.get("basePricePerNight") and guests >= 2: allowed.add(round(d["basePricePerNight"] / guests))
        if d.get("weekendPrice") and guests >= 2: allowed.add(round(d["weekendPrice"] / guests))
        facts.append(f"{d.get('roomName') or d['title']}: ${d.get('basePricePerNight')}/night, weekend {d.get('weekendPrice')}, day use {d.get('dayUsePrice')}, max {guests}, {d.get('bedrooms')} bedrooms, " + ", ".join(a["name"] for a in d.get("amenities", [])))
    # other rooms of the same host also appear in room-reveal Reels
    hosts = {(i["title"], i["region"]["slug"]) for i in items if i["id"] in post["listing_ids"]}
    for i in items:
        if (i["title"], i["region"]["slug"]) in hosts and i["id"] not in post["listing_ids"]:
            if i.get("priceFrom"): allowed.add(round(i["priceFrom"]))
            if i.get("dayUsePrice"): allowed.add(round(i["dayUsePrice"]))
    text = ""
    for fn in ("caption.txt", "reel-remotion.json"):
        fp = os.path.join(ROOT, "posts", folder, fn)
        if os.path.exists(fp): text += open(fp, encoding="utf-8").read() + "\n"
    text = text.translate(str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789"))
    found = {int(x) for x in re.findall(r"\$\s?(\d[\d,]*)", text.replace(",", ""))} | {int(x) for x in re.findall(r"(\d+)\s?\$", text)} | {int(x) for x in re.findall(r"(\d+)\s*دولار", text)}
    bad = sorted(found - allowed)
    if not quiet: print("\n".join(facts)); print("amounts in text:", sorted(found), "| allowed:", sorted(allowed))
    return [f"${b} appears in the post but is not a price on the listing(s)" for b in bad]
if __name__ == "__main__":
    probs = check(sys.argv[1])
    print("\n".join(probs) if probs else "OK: all amounts match the site")
    sys.exit(1 if probs else 0)
