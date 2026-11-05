#!/usr/bin/env python3
"""Produce an animated, music-backed Weekendna review Reel from real Acampar listing images."""
import io, math, re, subprocess, urllib.request, wave, struct, random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT=Path("output/acampar"); OUT.mkdir(parents=True,exist_ok=True)
BASE="https://weekendna.com"
UA={"User-Agent":"Mozilla/5.0 (Weekendna editorial production)"}
def get(url):
    return urllib.request.urlopen(urllib.request.Request(url,headers=UA),timeout=35).read()
photos=[]
for lid,slug in [(42,"acampar-faraya-two-bedroom-bungalow-faraya-mzaar-42"),(39,"acampar-faraya-studio-bungalow-faraya-mzaar-39"),(40,"acampar-faraya-studio-bungalow-faraya-mzaar-40"),(41,"acampar-faraya-one-bedroom-bungalow-faraya-mzaar-41")]:
    html=get(f"{BASE}/en/stay/{slug}").decode("utf8","ignore")
    paths=list(dict.fromkeys(re.findall(rf"/uploads/listings/{lid}/[a-zA-Z0-9_-]+-1600[.]webp",html)))
    for path in paths[:5]:
        try:
            raw=get(BASE+path); im=Image.open(io.BytesIO(raw)); im.verify()
            photos.append((lid,path,raw))
        except Exception as e: print("Skipping",path,e)
if len(photos)<8: raise RuntimeError("Need at least eight genuine listing images")
(OUT/"sources.txt").write_text("\n".join(BASE+p for _,p,_ in photos))
W,H=720,1280; fps=30; shot_s=3.1
fontpath="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
def font(n): return ImageFont.truetype(fontpath,n)
shots=[
("","",42),
("","",39),
("","",40),
("","",41),
("","",42),
("","",39),
("","",40),
("A LITTLE ESCAPE","FROM EVERYTHING",41)]
used=set()
for i,(heading,sub,lid) in enumerate(shots):
    candidates=[p for p in photos if p[0]==lid and p[1] not in used]
    if not candidates: candidates=[p for p in photos if p[1] not in used]
    item=candidates[0]; used.add(item[1])
    im=Image.open(io.BytesIO(item[2])).convert("RGB")
    # Overscan for fluid pan/zoom; never synthesize property imagery
    tw,th=820,1460
    scale=max(tw/im.width,th/im.height)
    im=im.resize((math.ceil(im.width*scale),math.ceil(im.height*scale)),Image.Resampling.LANCZOS)
    x=(im.width-tw)//2;y=(im.height-th)//2
    im=im.crop((x,y,x+tw,y+th))
    im.save(OUT/f"photo{i:02d}.jpg",quality=93)
    overlay=Image.new("RGBA",(W,H),(0,0,0,0))
    d=ImageDraw.Draw(overlay)
    # subtle editorial gradients
    for yy in range(0,310,3): d.rectangle((0,yy,W,yy+3),fill=(0,0,0,int(115*(1-yy/310))))
    for yy in range(730,H,3): d.rectangle((0,yy,W,yy+3),fill=(0,0,0,int(170*(yy-730)/(H-730))))
    if i == 0 or i == len(shots)-1: d.text((44,65),"W E E K E N D N A",font=font(20),fill="white")
    if heading: d.rounded_rectangle((44,904,126,908),radius=2,fill="#e0263b")
    if heading: d.text((44,936),heading,font=font(30),fill="white",stroke_width=1,stroke_fill="#202020")
    if sub: d.text((44,997),sub,font=font(27),fill="white",stroke_width=1,stroke_fill="#202020")
    if i == len(shots)-1: d.text((44,1180),"ACAMPAR FARAYA  /  @WEEKENDNA.LB",font=font(16),fill="white")
    overlay.save(OUT/f"overlay{i:02d}.png")
    # animated crop plus title overlay, gentle fade on entry/exit
    n=int(shot_s*fps)
    zoom="min(1.10,1+0.0009*on)" if i%2==0 else "max(1.0,1.10-0.0009*on)"
    vf=f"[0:v]zoompan=z='{zoom}':x='(iw-iw/zoom)/2+sin(on/30)*10':y='(ih-ih/zoom)/2':d={n}:s={W}x{H}:fps={fps},format=yuv420p[bg];[bg][1:v]overlay=0:0:format=auto,format=yuv420p,fade=t=in:st=0:d=0.25,fade=t=out:st={shot_s-0.25}:d=0.25[v]"
    subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-loop","1","-i",str(OUT/f"photo{i:02d}.jpg"),"-loop","1","-i",str(OUT/f"overlay{i:02d}.png"),"-filter_complex",vf,"-map","[v]","-t",str(shot_s),"-c:v","libx264","-preset","veryfast","-crf","22","-pix_fmt","yuv420p",str(OUT/f"clip{i:02d}.mp4")],check=True)
# Original instrumental soundtrack generated in code: no third-party recordings or copyright claims
sr=22050;duration=shot_s*len(shots); bpm=112
notes=[(220,277.18,329.63),(174.61,220,261.63),(196,246.94,293.66),(164.81,207.65,246.94)]
random.seed(8)
with wave.open(str(OUT/"original-music.wav"),"wb") as wav:
    wav.setnchannels(1);wav.setsampwidth(2);wav.setframerate(sr)
    block=[]
    for k in range(int(duration*sr)):
        t=k/sr;beat=t*bpm/60;bar=int(beat//4)%4; chord=notes[bar]
        pad=sum(math.sin(2*math.pi*f*t)*0.08 for f in chord)
        pulse=math.exp(-((beat%1)*8))*math.sin(2*math.pi*65*t)*0.13
        hihat=(random.random()*2-1)*0.018*math.exp(-((beat*2)%1)*20)
        lead=math.sin(2*math.pi*chord[int(beat*2)%3]*2*t)*0.045*math.exp(-((beat*2)%1)*5)
        env=min(1,t/0.6,max(0,(duration-t)/0.8))
        v=max(-1,min(1,(pad+pulse+hihat+lead)*env))
        block.append(struct.pack("<h",int(v*26000)))
        if len(block)>=4096: wav.writeframes(b"".join(block));block=[]
    if block:wav.writeframes(b"".join(block))
concat=OUT/"concat.txt";concat.write_text("".join(f"file 'clip{i:02d}.mp4'\n" for i in range(len(shots))))
subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-f","concat","-safe","0","-i",str(concat),"-i",str(OUT/"original-music.wav"),"-map","0:v","-map","1:a","-c:v","copy","-c:a","aac","-b:a","160k","-shortest","-movflags","+faststart",str(OUT/"acampar-review.mp4")],check=True)
print("READY",OUT/"acampar-review.mp4")
