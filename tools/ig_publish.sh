#!/bin/bash
# usage: ig_publish.sh <post-folder-name> <n-slides> [collaborator-username]
set -e
T="${IG_TOKEN:?set IG_TOKEN}"
U=17841412894685016; DIR=$1; N=$2; COL=$3
B=https://raw.githubusercontent.com/kamelabiad/weekendna-social/main/posts/$DIR
NAME=$(echo $DIR | sed -E 's/^[0-9]{4}-[0-9]{2}-//')
case $NAME in ghosta-guest-house) PRE=ghosta;; domaine-du-karst) PRE=karst;; bayt-baabdat) PRE=baabdat;; faraya-village-club) PRE=faraya;; majestic-byblos) PRE=majestic;; gracias-guesthouse) PRE=gracias;; *) PRE=$NAME;; esac
curl -sS -m 30 -o /tmp/cap.txt "$B/caption.txt"
IDS=""
for i in $(seq 1 $N); do
  if [ $i = 1 ] && [ -n "$COL" ]; then TAG=(--data-urlencode "user_tags=[{\"username\":\"$COL\",\"x\":0.5,\"y\":0.45}]"); else TAG=(); fi
  ID=$(curl -sS -m 60 -X POST "https://graph.instagram.com/v21.0/$U/media" --data-urlencode "image_url=$B/$PRE-$i.jpg" -d is_carousel_item=true "${TAG[@]}" -d "access_token=$T" | python3 -c "import sys,json;d=json.load(sys.stdin);print(d['id']) if 'id' in d else sys.exit(str(d))")
  IDS="$IDS,$ID"
done
if [ -n "$COL" ]; then C=(--data-urlencode "collaborators=[\"$COL\"]"); else C=(); fi
P=$(curl -sS -m 60 -X POST "https://graph.instagram.com/v21.0/$U/media" -d media_type=CAROUSEL -d "children=${IDS#,}" --data-urlencode "caption@/tmp/cap.txt" "${C[@]}" -d "access_token=$T" | python3 -c "import sys,json;d=json.load(sys.stdin);print(d['id']) if 'id' in d else sys.exit(str(d))")
for k in $(seq 1 12); do curl -sS -m 30 "https://graph.instagram.com/v21.0/$P?fields=status_code&access_token=$T" | grep -q FINISHED && break; sleep 5; done
M=$(curl -sS -m 60 -X POST "https://graph.instagram.com/v21.0/$U/media_publish" -d creation_id=$P -d "access_token=$T" | python3 -c "import sys,json;d=json.load(sys.stdin);print(d['id']) if 'id' in d else sys.exit(str(d))")
curl -sS -m 30 "https://graph.instagram.com/v21.0/$M?fields=permalink&access_token=$T"; echo
curl -sS -m 30 "https://graph.instagram.com/refresh_access_token?grant_type=ig_refresh_token&access_token=$T" >/dev/null || true
