# Weekendna Instagram playbook

How @weekendna.lb posts are made and scheduled. Written for the weekly scheduled task, which starts with no memory of earlier chats.

## Strategy (Oct 2026)
- The problem is reach, not content: ~11 followers, 1 website click in 2 weeks. Posts alone don't bring guests.
- Many owners are also on booking.com / their own sites, so guests can book them elsewhere. Weekendna wins where booking.com is weak: **places not on booking.com** (Instagram/WhatsApp-only chalets, villas, huts), **day-use pools and wedding venues**, and the Lebanese way of booking (**WhatsApp, pay at the place, Arabic, no card**). Owners pay **0% commission** (founding owners free for 12 months).
- So: prioritise owners not on booking.com and day-use/wedding listings; lead captions with WhatsApp booking/day use; every post gets a **Reel** (reaches non-followers) and a **story kit** the owner shares to *their* audience; weekly Facebook-group post for Kamel.

## Automation
- `posts/log.json` is the schedule. The daily task (4:52pm UK) runs `tools/publish_due.py`, which publishes what's due: feed post + Weekendna story on `date`, the Reel version on `reel_date`. No per-post scheduled tasks.
- The weekly task (Sunday) plans and prepares the next week and adds it to the log. Kamel can reply to change/hold; otherwise it goes out.
- Each post folder: slides `<prefix>-N.jpg`, `caption.txt`, `story.jpg` + `reel.mp4` (from `tools/make_kit.py`), `whatsapp.txt` (message Kamel forwards to the owner).
- **Reels (Remotion, Kamel approved Oct 2026):** build every Reel with the Remotion template in `reels/` (see `reels/README.md`). `tools/make_reel.py` is only the fallback if the Remotion render fails; the make_kit.py slideshow only when a listing has no usable photos. Steps:
  1. `cd reels && npm install` (first time in a session). Download the listing's `-1600.webp` photos into `reels/public/photos/<name>/` (photo hashes are in `https://api.weekendna.com/api/v1/listings/<slug>` → `photos`; `python3 tools/reel_prep.py photos <dir> <ids>` also works) and make a contact sheet; look at it and at the photos you pick. Photos and music are gitignored there; never commit them.
  2. Decrypt the music into `reels/public/music/` (see `music/README.md`), pick a track for the place (rotate; don't repeat the previous Reel's track), and get its tempo with `python3 tools/reel_prep.py bpm reels/public/music/<track>.mp3` (under ~90 is usually half-time: double it).
  3. Write `posts/<folder>/reel-remotion.json` (example: `posts/2026-10-majestic-byblos/reel-remotion.json`): `"music": "music/<track>.mp3"`, `musicStart`, `bpm`, 6–8 shots. Shot 1 = `hook` (best photo; caption's first line, EN + Lebanese AR), 2 = `title` (name, Arabic name, area pill), then `room` shots (one per room/unit: name, short fact, price) or `fact` shots, last = `end` (name, "From $X / night", Arabic booking line). The end card always shows "Follow @weekendna.lb". Time cuts on the beat: shot seconds = beats × 60/bpm + 0.3 (hook/shots 4 beats, end 6). Vary moves; `framed: true` for photos under ~1000px.
  4. Render stills first and look at every one (text readable, subject not covered, Arabic renders):
     `npx remotion still src/index.ts ListingReel /tmp/still.jpg --frame=<N> --props=../posts/<folder>/reel-remotion.json` (one frame inside each shot), then render:
     `npx remotion render src/index.ts ListingReel ../posts/<folder>/reel.mp4 --props=../posts/<folder>/reel-remotion.json --crf=20`.
     In the cloud workspace add `--browser-executable=/opt/pw-browsers/chromium-1194/chrome-linux/chrome --chrome-mode=chrome-for-testing` (Remotion's own browser download is blocked).
  - Arabic on-screen text: no "$" (write دولار), no Latin words; only facts from the listing.
  - Set `"music": "<track> [@start]"` in the log. Don't use generated music (Kamel found it too poor).
- **Follow ask:** every caption ends its English block with "Follow @weekendna.lb for a new place every week 🏡" and its Arabic block with "تابعونا عـ@weekendna.lb، كل أسبوع محل جديد 🏡" (after the booking line, before hashtags).

## The rules (from Kamel)
- **Cadence (from Oct 2026):** a carousel every 2 days and **a Reel every day**, at **5pm UK time** (Europe/London; mind the BST/GMT change). On the days between carousels, the Reel is that carousel's Reel version (`reel_date`). On carousel days, add a standalone Reel post (`type: "reel"`, `video: "reel.mp4"`, its own folder, caption and reel-remotion.json): a roundup of 3–5 places on one theme (day-use pools, under $100, a region, sea view, mountain/fireplace) or a fresh angle on a place posted 3+ weeks ago. Roundups get saved and shared most.
- **Instagram is fully automated.** Kamel gets the week's plan and previews; he can reply to change, hold or reorder, otherwise posts go out on schedule.
- **New listings go first.** Then owners who have never been posted. Then second-round posts for owners posted longest ago.
- **Skip:** owners listed in `posts/log.json` → `skip_for_now`.
- **Collaborators:** add the owner as collaborator and tag them on slide 1 whenever they have Instagram. Only use a handle Kamel gave or confirmed (or that is already in posts/log.json). Don't verify handles through the API; for a new owner, ask Kamel for their Instagram username. Never guess.
- **Captions:** English, then Arabic in **Lebanese dialect**, then hashtags. Only state facts that are on the listing (no invented distances, prices or features). If the listing has no price, leave price out.
- **Never message owners/clients directly.** Draft any message for Kamel to send himself.

## Where things are
- Listings: collect `/en/stay/<slug>-<id>` links from `https://weekendna.com/en/search`, every `/en/regions/<region>` page (linked from the homepage) **and** `sitemap.xml`. The sitemap lags behind (new listings were missing from it), so never rely on it alone. One owner can have several listings (see the "All their places" / `/en/hosts/...` link on a listing): combine them into one post. Each page has JSON-LD (name, description, amenities, occupancy) and photos at `/uploads/listings/<id>/<hash>-1600.webp` (also -800, -400). Price and host name are in the page text.
- Log of every post: `posts/log.json`. **Read it first, update it after every change.**
- Post files: `posts/<yyyy-mm>-<name>/` with `<prefix>-1.jpg…` and `caption.txt`. Images are served publicly from `https://raw.githubusercontent.com/kamelabiad/weekendna-social/main/posts/...`, which is how Instagram fetches them.
- Design: `tools/brand.py` (colours, fonts, logo, helpers). Examples of finished carousels: `tools/examples/make_*.py`. Run `source tools/setup.sh` first to fetch fonts.
- Publishing: `tools/publish_due.py` (daily, from the log). `--dry-run` and `--date YYYY-MM-DD` to test.

## Brand
- Colours: red `#e0263b`, ink `#222`, soft pink `#fdedef`, dark `#1a181c`. Fonts: Plus Jakarta Sans (text), Outfit (logo "weekend"), IBM Plex Sans Arabic (Arabic + "نا" in red).
- Carousels are 1080×1350 (4:5), usually 3–4 slides: (1) best photo full-bleed with name, region pill, one-line hook in English + Arabic; (2) photo + 4 key facts with red bullets; (3) optional extra photo; (4) CTA with price if known, Arabic line, button "weekendna.com · link in bio".
- Low-resolution photos (under ~800px): don't use full-bleed. Use framed/grid layouts (see `make_batch.py` Faraya and `make_majestic.py`).
- Always render a preview and look at it before sending: check text doesn't cover the main subject and Arabic renders (no empty boxes, avoid "·" inside Arabic text).

## Instagram API (Instagram Login, app "Weekendna Poster", account id 17841412894685016)
- Base: `https://graph.instagram.com/v21.0`. Token in `IG_TOKEN` (long-lived, ~60 days; refresh with `GET /refresh_access_token?grant_type=ig_refresh_token&access_token=…` — weekly is fine).
- **API safety (Oct 2026):** Meta locked the developer account once for "unusual activity" (Kamel had to confirm it). Keep API use to what publishing needs: no test/unpublished containers, no handle checks, no polling loops, no retries beyond one. Refresh the token only in the weekly task (once a week), never in the daily one. If any call returns "API access blocked" (code 200) or a checkpoint/confirmation error, stop all API calls at once and tell Kamel; don't retry.
- Views and reach: one call, `GET /me/media?fields=caption,timestamp,like_count,comments_count,insights.metric(views,reach)&limit=30` (weekly task only).
- Stories: `media_type=STORIES` + `image_url` (no collaborators). Reels: `media_type=REELS` + `video_url`, `share_to_feed=false` for Reel versions of carousels.
- Not available: reading DMs (app is in development mode), looking up other accounts (business_discovery), adding Instagram music, editing collaborators after posting.

## Scheduling
- Add the post to `posts/log.json` (status/story_status/reel_status "scheduled", date, reel_date) and push. The daily task publishes it. Don't create separate scheduled tasks.
