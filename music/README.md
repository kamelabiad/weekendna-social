# Reel music (encrypted)

Kamel's royalty-free tracks (Pixabay / Mixkit licences: free for commercial use inside our videos, but the bare files
may not be shared publicly). This repo is public, so they are stored encrypted. The key is in the scheduled tasks'
instructions as MUSIC_KEY (never commit or print it).

Decrypt (into a temp folder, never into the repo):
    mkdir -p /tmp/music && for f in music/*.mp3.enc; do openssl enc -d -aes-256-cbc -pbkdf2 -pass pass:"$MUSIC_KEY" -in "$f" -out "/tmp/music/$(basename "$f" .enc)"; done
Then reference the track in the post's reel.json for tools/make_reel.py (add_music.py only for a fallback slideshow Reel).

| Track | Mood | Use for | Start |
|---|---|---|---|
| calm-acoustic-andriig.mp3 | soft acoustic guitar | mountain / nature guesthouses, quiet places | 0 |
| warm-acoustic-atlasaudio.mp3 | warm, brighter acoustic | huts, cabins, chalets, beach guesthouses | 0 or 40 |
| oud-alexmorgan.mp3 | Arabic oud | traditional Lebanese houses, heritage places | 12 (quiet intro before) |
| upbeat-gear-mixkit.mp3 | upbeat, energetic | resorts, pools, clubs, day use | 0 (energy drops after ~28s) |
| lounge-aurec.mp3 | chill lounge | hotels, upscale places | 0 |

Rotate so two Reels in a row don't use the same track; when reusing a track, use a different --start so it sounds fresh.
Kamel may add more tracks: encrypt with the same key and add a row here.
