"""Turn a post folder's story.jpg into story.mp4 with music, so the story plays with sound (Kamel, 8 Nov 2026:
"having them with music is nicer"). The Instagram API cannot add Instagram music, so the track is baked into the video.

Usage: python3 tools/make_story_video.py <post-folder> <decrypted-track.mp3> [--start SECONDS] [--seconds 12]
  e.g. python3 tools/make_story_video.py 2026-11-stories-10 /tmp/music/calm-acoustic-andriig.mp3 --start 0
Decrypt the tracks first (music/README.md); never commit the mp3s. Then set "story_video": "story.mp4" and
"story_music": "<track> [@start]" on the log item. The image gets a slow, gentle zoom (text stays readable),
the music fades in/out and is loudness-normalised to -16 LUFS. Output: 1080x1920, 30 fps, H.264 + AAC (Instagram specs).
"""
import os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
a = sys.argv[1:]
folder, track = a[0], a[1]
start = float(a[a.index("--start") + 1]) if "--start" in a else 0.0
secs = float(a[a.index("--seconds") + 1]) if "--seconds" in a else 12.0
d = os.path.join(HERE, "..", "posts", folder)
img, out = os.path.join(d, "story.jpg"), os.path.join(d, "story.mp4")
frames = int(secs * 30)
# render the zoom at 2x then downscale: avoids zoompan's jitter on slow zooms
vf = (f"scale=2160:3840,zoompan=z='1+0.02*on/{frames}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s=2160x3840:fps=30,"
      f"scale=1080:1920:flags=lanczos,fade=t=in:d=0.3,format=yuv420p")
af = f"afade=t=in:d=0.5,afade=t=out:st={secs - 1.5:.2f}:d=1.5,loudnorm=I=-16:TP=-1.5:LRA=11"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", img, "-ss", str(start), "-t", f"{secs:.2f}", "-i", track,
                "-filter_complex", f"[0:v]{vf}[v];[1:a]{af}[a]", "-map", "[v]", "-map", "[a]", "-t", f"{secs:.2f}",
                "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-r", "30", "-c:a", "aac", "-b:a", "160k",
                "-ar", "44100", "-ac", "2", "-movflags", "+faststart", out], check=True)
print("story video with", os.path.basename(track), f"(from {start:g}s, {secs:g}s) ->", out)
