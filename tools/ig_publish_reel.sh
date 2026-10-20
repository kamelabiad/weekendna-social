#!/bin/bash
# usage: ig_publish_reel.sh <post-folder> <video-file-name> [collaborator]
set -e
T="${IG_TOKEN:?set IG_TOKEN}"
U=17841412894685016; B=https://raw.githubusercontent.com/kamelabiad/weekendna-social/main/posts/$1; COL=$3
curl -sS -m 30 -o /tmp/cap.txt "$B/caption.txt"
if [ -n "$COL" ]; then C=(--data-urlencode "collaborators=[\"$COL\"]"); else C=(); fi
P=$(curl -sS -m 60 -X POST "https://graph.instagram.com/v21.0/$U/media" -d media_type=REELS --data-urlencode "video_url=$B/$2" -d share_to_feed=true --data-urlencode "caption@/tmp/cap.txt" "${C[@]}" -d "access_token=$T" | python3 -c "import sys,json;d=json.load(sys.stdin);print(d['id']) if 'id' in d else sys.exit(str(d))")
for k in $(seq 1 40); do s=$(curl -sS -m 30 "https://graph.instagram.com/v21.0/$P?fields=status_code&access_token=$T"); echo "$s" | grep -q FINISHED && break; echo "$s" | grep -q ERROR && { echo "$s"; exit 1; }; sleep 6; done
M=$(curl -sS -m 60 -X POST "https://graph.instagram.com/v21.0/$U/media_publish" -d creation_id=$P -d "access_token=$T" | python3 -c "import sys,json;d=json.load(sys.stdin);print(d['id']) if 'id' in d else sys.exit(str(d))")
curl -sS -m 30 "https://graph.instagram.com/v21.0/$M?fields=permalink&access_token=$T"; echo
