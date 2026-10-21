"""Put original background music (tools/make_music.py) on a post's reel.mp4, replacing its audio track.

Usage: python3 tools/add_music.py <post-folder> <mood> [--seed N]
  e.g. python3 tools/add_music.py 2026-10-ghosta-guest-house calm
Moods: calm, cozy, oud, upbeat, lounge, summer (see make_music.py). Record the mood in posts/log.json as "music".
The video is copied untouched; the music is loudness-normalised (-16 LUFS) and fades out at the end.
"""
import os, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
a = sys.argv[1:]
folder, mood = a[0], a[1]
seed = a[a.index("--seed") + 1] if "--seed" in a else str(sum(map(ord, folder)) % 1000)  # stable per post, different between posts
reel = os.path.join(HERE, "..", "posts", folder, "reel.mp4")
dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "format=duration",
                                     "-of", "default=nw=1:nk=1", reel]).decode().strip())
tmp = tempfile.mkdtemp()
wav = os.path.join(tmp, "music.wav"); out = os.path.join(tmp, "reel.mp4")
subprocess.run([sys.executable, os.path.join(HERE, "make_music.py"), mood, f"{dur:.2f}", wav, "--seed", seed], check=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", reel, "-i", wav, "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy",
                "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "44100", "-c:a", "aac", "-b:a", "160k", "-shortest",
                "-movflags", "+faststart", out], check=True)
os.replace(out, reel)
print(f"music ({mood}) added to", reel)
