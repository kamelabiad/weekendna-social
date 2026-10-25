# Remotion Reel template

Builds a 9:16 Instagram Reel (1080×1920, 30fps) from a listing's photos and a small JSON file, in Weekendna's brand
(fonts, red, logo). An alternative to `tools/make_reel.py`.

## One-time setup
    cd reels && npm install

## Make a Reel
1. Put the listing's photos in `reels/public/photos/<name>/` (download `-1600.webp` from
   `https://api.weekendna.com/uploads/listings/<id>/<hash>-1600.webp`; hashes are in `/api/v1/listings/<slug>` → `photos`).
   Photos are not committed.
2. Write `posts/<folder>/reel-remotion.json` (see `posts/2026-10-majestic-byblos/reel-remotion.json`):
   - shot types: `hook` (en + ar), `title` (name, ar, pill), `room` (name, en, ar, price), `fact` (en, ar), `end` (name, price, ar)
   - `seconds`, `move` (zoom_in/out, pan_left/right/up/down), optional `fx`/`fy` focus, `framed: true` for small photos (under ~1000px)
   - optional `"music": "music/<track>.mp3"` (decrypted copy in `reels/public/music/`, never committed) and `"musicStart"`
   - Arabic text: write دولار instead of $, no Latin words. Only facts from the listing.
3. Preview: `npx remotion studio src/index.ts --props=../posts/<folder>/reel-remotion.json`
4. Render:
       npx remotion render src/index.ts ListingReel ../posts/<folder>/reel-remotion.mp4 --props=../posts/<folder>/reel-remotion.json --crf=20
   In the cloud workspace add
   `--browser-executable=/opt/pw-browsers/chromium-1243/chrome-linux64/chrome --chrome-mode=chrome-for-testing`
   (Remotion's own browser download is blocked there).

Licence: Remotion is free for individuals and companies of up to 3 people.
