# Weekendna Instagram playbook

How @weekendna.lb posts are made and scheduled. Written for the weekly scheduled task, which starts with no memory of earlier chats.

## The rules (from Kamel)
- **Cadence:** one post every 2 days at **5pm UK time** (Europe/London; mind the BST/GMT change).
- **Nothing goes live without Kamel's OK.** Send him previews; schedule only after he replies OK. He can change, hold or reorder any post.
- **New listings go first.** Then owners who have never been posted. Then second-round posts for owners posted longest ago.
- **Skip:** owners listed in `posts/log.json` → `skip_for_now`.
- **Collaborators:** add the owner as collaborator and tag them on slide 1 whenever they have Instagram. Only use a handle Kamel gave or confirmed. Verify it first (see below). Never guess.
- **Captions:** English, then Arabic in **Lebanese dialect**, then hashtags. Only state facts that are on the listing (no invented distances, prices or features). If the listing has no price, leave price out.
- **Never message owners/clients directly.** Draft any message for Kamel to send himself.

## Where things are
- Listings: collect `/en/stay/<slug>-<id>` links from `https://weekendna.com/en/search`, every `/en/regions/<region>` page (linked from the homepage) **and** `sitemap.xml`. The sitemap lags behind (new listings were missing from it), so never rely on it alone. One owner can have several listings (see the "All their places" / `/en/hosts/...` link on a listing): combine them into one post. Each page has JSON-LD (name, description, amenities, occupancy) and photos at `/uploads/listings/<id>/<hash>-1600.webp` (also -800, -400). Price and host name are in the page text.
- Log of every post: `posts/log.json`. **Read it first, update it after every change.**
- Post files: `posts/<yyyy-mm>-<name>/` with `<prefix>-1.jpg…` and `caption.txt`. Images are served publicly from `https://raw.githubusercontent.com/kamelabiad/weekendna-social/main/posts/...`, which is how Instagram fetches them.
- Design: `tools/brand.py` (colours, fonts, logo, helpers). Examples of finished carousels: `tools/examples/make_*.py`. Run `source tools/setup.sh` first to fetch fonts.
- Publishing: `tools/ig_publish.sh <folder> <n-slides> [handle]` for carousels and `tools/ig_publish_reel.sh <folder> <video> [handle]` for Reels. Both need `IG_TOKEN` set. Add the folder→file-prefix mapping in the `case` line of `ig_publish.sh` for new folders.

## Brand
- Colours: red `#e0263b`, ink `#222`, soft pink `#fdedef`, dark `#1a181c`. Fonts: Plus Jakarta Sans (text), Outfit (logo "weekend"), IBM Plex Sans Arabic (Arabic + "نا" in red).
- Carousels are 1080×1350 (4:5), usually 3–4 slides: (1) best photo full-bleed with name, region pill, one-line hook in English + Arabic; (2) photo + 4 key facts with red bullets; (3) optional extra photo; (4) CTA with price if known, Arabic line, button "weekendna.com · link in bio".
- Low-resolution photos (under ~800px): don't use full-bleed. Use framed/grid layouts (see `make_batch.py` Faraya and `make_majestic.py`).
- Always render a preview and look at it before sending: check text doesn't cover the main subject and Arabic renders (no empty boxes, avoid "·" inside Arabic text).

## Instagram API (Instagram Login, app "Weekendna Poster", account id 17841412894685016)
- Base: `https://graph.instagram.com/v21.0`. Token in `IG_TOKEN` (long-lived, ~60 days; refresh with `GET /refresh_access_token?grant_type=ig_refresh_token&access_token=…` — weekly is fine).
- Verify a handle: create an **unpublished** container `POST /{ig-id}/media` with `image_url=<any repo image>` and `collaborators=["handle"]`. An id back means the account exists; error 2207018 means invalid or private. Unpublished containers expire on their own.
- Not available: reading DMs (app is in development mode), looking up other accounts (business_discovery), adding Instagram music, editing collaborators after posting.

## Scheduling
- Use `send_later` (one-shot, into the same chat) for each approved post at 5pm UK, with a message telling that future turn exactly which command to run. Update `posts/log.json` and push.
