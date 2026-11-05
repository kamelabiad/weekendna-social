#!/usr/bin/env python3
"""Build a review-only Acampar Reel from verified Weekendna public images."""
import os, re, urllib.request, io, math, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

OUT=Path("output/acampar"); OUT.mkdir(parents=True,exist_ok=True)
BASE="https://weekendna.com"
UA={"User-Agent":"Mozilla/5.0 (Weekendna social production)"}
def get(url):
    return urllib.request.urlopen(urllib.request.Request(url,headers=UA),timeout=35).read()
photos=[]
for lid in (39,40,41,42):
    slug={39:"acampar-faraya-studio-bungalow-faraya-mzaar-39",40:"acampar-faraya-studio-bungalow-faraya-mzaar-40",41:"acampar-faraya-one-bedroom-bungalow-faraya-mzaar-41",42:"acampar-faraya-two-bedroom-bungalow-faraya-mzaar-42"}[lid]
    html=get(f"{BASE}/en/stay/{slug}").decode("utf8","ignore")
    paths=list(dict.fromkeys(re.findall(rf"/uploads/listings/{lid}/[a-zA-Z0-9_-]+-1600\\.webp",html)))
    print(lid,len(paths),"images")
    for path in paths:
        try:
            raw=get(BASE+path)
            im=Image.open(io.BytesIO(raw)); im.verify()
            photos.append((lid,path,raw))
        except Exception as e: print("Skipped",path,e)
if len(photos)<2:
    raise RuntimeError("Insufficient VERIFIED Acampar images; refusing to make a fake Reel")
(OUT/"sources.txt").write_text("\n".join(p for _,p,_ in photos))
W,H=1080,1920
fontpath="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
def font(sz):return ImageFont.truetype(fontpath,sz)
texts=[("Cold outside.","Cosy inside."),("ACAMPAR FARAYA","Your mountain escape"),("A slower weekend","starts here."),("Real places.","Real escapes."),("Found on Weekendna","Follow @weekendna.lb")]
for i,(a,b) in enumerate(texts):
    lid,path,raw=photos[i%len(photos)]
    im=Image.open(io.BytesIO(raw)).convert("RGB")
    scale=max(W/im.width,H/im.height); im=im.resize((math.ceil(im.width*scale),math.ceil(im.height*scale)),Image.Resampling.LANCZOS)
    x=(im.width-W)//2;y=(im.height-H)//2
    im=im.crop((x,y,x+W,y+H))
    from PIL import ImageFilter
    overlay=Image.new("RGBA",(W,H),(0,0,0,0))
    d=ImageDraw.Draw(overlay)
    d.rectangle((0,0,W,290),fill=(0,0,0,105))
    d.rectangle((0,1170,W,H),fill=(0,0,0,155))
    d.text((72,120),"W E E K E N D N A",font=font(38),fill="white")
    d.rounded_rectangle((72,1260,970,1280),radius=8,fill="#e0263b")
    d.text((72,1360),a,font=font(66),fill="white",stroke_width=1)
    d.text((72,1460),b,font=font(58),fill="white")
    d.text((72,1740),"ACAMPAR FARAYA  •  LEBANON",font=font(28),fill="white")
    im=Image.alpha_composite(im.convert("RGBA"),overlay).convert("RGB")
    im.save(OUT/f"frame{i:02d}.jpg",quality=94)
subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-framerate","1/4","-i",str(OUT/"frame%02d.jpg"),"-vf","fps=30,format=yuv420p","-c:v","libx264","-preset","medium","-movflags","+faststart",str(OUT/"acampar-review.mp4")],check=True)
print("READY",OUT/"acampar-review.mp4")
