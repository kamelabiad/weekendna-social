"""Put one of Kamel's music tracks on a post's reel.mp4, replacing its (silent) audio track.

Usage: python3 tools/add_music.py <post-folder> <track.mp3> [--start SECONDS]
  e.g. python3 tools/add_music.py 2026-10-ghosta-guest-house music/andriig-acoustic-music-604001.mp3
Tracks are Kamel's royalty-free files (Pixabay / Mixkit), kept in his Google Drive folder "Weekendna music" (NOT in this
public repo: the licences don't allow sharing the bare files). See PLAYBOOK.md "Reel music" for which track fits which place.
The video is copied untouched; the music starts at --start (default 0), fades in briefly and fades out over the last 1.5s,
and is loudness-normalised to -16 LUFS. Record the track in posts/log.json as "music".
"""
import os, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
a = sys.argv[1:]
folder, track = a[0], a[1]
start = float(a[a.index("--start") + 1]) if "--start" in a else 0.0
reel = os.path.join(HERE, "..", "posts", folder, "reel.mp4")
dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", reel]).decode())
out = os.path.join(tempfile.mkdtemp(), "reel.mp4")
af = f"afade=t=in:d=0.4,afade=t=out:st={dur - 1.5:.2f}:d=1.5,loudnorm=I=-16:TP=-1.5:LRA=11"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", reel, "-ss", str(start), "-t", f"{dur:.2f}", "-i", track,
                "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-af", af, "-ar", "44100", "-ac", "2",
                "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", out], check=True)
os.replace(out, reel)
print(f"music {os.path.basename(track)} (from {start:g}s) added to", reel)
