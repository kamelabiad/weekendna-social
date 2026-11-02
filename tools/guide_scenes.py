"""Rich illustrated scenes (SVG rendered with Chromium) for City Guides when no real photo exists. Drawn, not photographic: label as illustrations.
Usage: python3 tools/guide_scenes.py <outdir>  -> winter.png, ski.png, food.png, village.png (1080x780)."""
import random, sys, os
W, H = 1080, 780
GRAIN = '<filter id="g"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="3"/><feColorMatrix values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 .07 0"/></filter><filter id="b4"><feGaussianBlur stdDeviation="4"/></filter><filter id="b10"><feGaussianBlur stdDeviation="10"/></filter><filter id="b2"><feGaussianBlur stdDeviation="1.6"/></filter>'
def svg(body, defs=""): return f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><defs>{GRAIN}{defs}</defs>{body}<rect width="{W}" height="{H}" filter="url(#g)"/></svg>'
def pine(x, y, s, c="#173f3a", sn="#f4f8ff", lit=None):
    o = f'<rect x="{x-s*.04}" y="{y}" width="{s*.08}" height="{s*.2}" fill="#3d2a22"/>'
    for i in range(5):
        w = s * (1 - i * .17); yy = y - i * s * .42
        o += f'<polygon points="{x-w/2},{yy} {x+w/2},{yy} {x},{yy-s*.62}" fill="{c}"/><polygon points="{x-w*.34},{yy-s*.2} {x+w*.34},{yy-s*.2} {x},{yy-s*.62}" fill="{sn}" opacity=".9"/>'
    return o
def chalet(x, y, w, h, roof="#f6f9ff", wall="#7b5237", glow="#ffcf70"):
    o = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{wall}"/><polygon points="{x-8},{y} {x+w/2},{y-h*.7} {x+w+8},{y}" fill="{roof}"/><polygon points="{x-8},{y} {x+w/2},{y-h*.7} {x+w+8},{y}" fill="#c8d6ea" opacity=".35"/>'
    for i, fx in enumerate((.18, .58)): o += f'<rect x="{x+w*fx}" y="{y+h*.25}" width="{w*.22}" height="{h*.4}" fill="{glow}"/><rect x="{x+w*fx}" y="{y+h*.25}" width="{w*.22}" height="{h*.4}" fill="{glow}" filter="url(#b4)" opacity=".8"/>'
    return o
def flakes(n, seed=1, r=(1, 3.2)):
    random.seed(seed); return "".join(f'<circle cx="{random.randint(0,W)}" cy="{random.randint(0,H)}" r="{random.uniform(*r):.1f}" fill="#fff" opacity="{random.uniform(.35,.9):.2f}"/>' for _ in range(n))
def winter():
    d = '<linearGradient id="sk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#25316b"/><stop offset=".35" stop-color="#8a5a9c"/><stop offset=".6" stop-color="#f08a6a"/><stop offset=".78" stop-color="#ffc47a"/></linearGradient><radialGradient id="sun"><stop offset="0" stop-color="#fff4c9"/><stop offset=".35" stop-color="#ffd27a" stop-opacity=".8"/><stop offset="1" stop-color="#ff9a5a" stop-opacity="0"/></radialGradient><linearGradient id="m1" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#b9a7d6"/><stop offset="1" stop-color="#e7a9a0"/></linearGradient><linearGradient id="m2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e9ecf8"/><stop offset="1" stop-color="#9aa6d0"/></linearGradient><linearGradient id="sl" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff2e6"/><stop offset="1" stop-color="#9fb0d9"/></linearGradient>'
    b = f'<rect width="{W}" height="{H}" fill="url(#sk)"/><circle cx="760" cy="330" r="300" fill="url(#sun)"/><circle cx="760" cy="330" r="52" fill="#fff6d6"/>'
    b += '<polygon points="0,420 140,270 260,360 430,200 600,380 760,250 930,360 1080,280 1080,560 0,560" fill="url(#m1)" filter="url(#b2)"/>'
    b += '<polygon points="0,470 180,330 330,430 520,300 700,450 880,330 1080,470 1080,640 0,640" fill="url(#m2)"/><polygon points="520,300 560,360 520,350 490,380" fill="#fff"/><polygon points="180,330 215,385 180,375 150,400" fill="#fff"/>'
    b += '<polygon points="0,600 250,470 520,560 800,480 1080,590 1080,780 0,780" fill="url(#sl)"/>'
    random.seed(5)
    for x in range(-20, W + 40, 90): b += pine(x + random.randint(-15, 15), 640 + random.randint(0, 90), 110 + random.randint(0, 50), c="#143a3a")
    for x, y, w, h in ((150, 585, 70, 44), (300, 610, 84, 52), (830, 590, 76, 48), (960, 615, 70, 46)): b += chalet(x, y, w, h)
    b += '<line x1="0" y1="110" x2="1080" y2="260" stroke="#2a2430" stroke-width="3"/>'
    for fx in (.2, .5, .8): x = 1080 * fx; y = 110 + 150 * fx; b += f'<line x1="{x}" y1="{y}" x2="{x}" y2="{y+48}" stroke="#2a2430" stroke-width="3"/><rect x="{x-24}" y="{y+48}" width="48" height="26" rx="6" fill="#d8283c"/>'
    b += flakes(70, 2, (1, 2.4))
    return svg(b, d)
def ski():
    d = '<linearGradient id="sk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1d6fd1"/><stop offset=".7" stop-color="#8fc8ff"/><stop offset="1" stop-color="#e6f3ff"/></linearGradient><linearGradient id="sl" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#bcd2f0"/></linearGradient><radialGradient id="fl"><stop offset="0" stop-color="#fff" stop-opacity=".95"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>'
    b = f'<rect width="{W}" height="{H}" fill="url(#sk)"/><circle cx="170" cy="120" r="220" fill="url(#fl)"/>'
    b += '<polygon points="0,380 200,230 380,340 600,190 800,330 1080,220 1080,520 0,520" fill="#dfeaf8"/><polygon points="600,190 650,260 610,250 570,290" fill="#fff"/><polygon points="0,440 260,330 520,430 840,320 1080,420 1080,600 0,600" fill="#f4f8ff"/>'
    b += '<polygon points="0,780 0,520 1080,360 1080,780" fill="url(#sl)"/><polygon points="0,780 1080,780 1080,520 0,700" fill="#d8e6f8" opacity=".6"/>'
    random.seed(8)
    for x in (30, 130, 960, 1040): b += pine(x, 470 + random.randint(-10, 20), 120, c="#1c5a52")
    b += '<line x1="0" y1="90" x2="1080" y2="40" stroke="#26303f" stroke-width="3"/><rect x="740" y="40" width="4" height="40" fill="#26303f"/><rect x="718" y="78" width="48" height="26" rx="6" fill="#e0314a"/>'
    def skier(x, y, s, jacket, pants="#1f2a44"):
        return (f'<g transform="translate({x},{y}) scale({s})"><ellipse cx="0" cy="82" rx="90" ry="10" fill="#9db4d8" opacity=".5"/><line x1="-80" y1="76" x2="70" y2="58" stroke="#16202f" stroke-width="7" stroke-linecap="round"/>'
                f'<polygon points="-26,0 22,-6 32,50 -14,56" fill="{jacket}"/><polygon points="-14,56 32,50 36,76 -4,80" fill="{pants}"/><circle cx="2" cy="-22" r="17" fill="#f2c9a6"/><path d="M-16,-26 Q2,-50 20,-26 Z" fill="#fafafa"/><rect x="-12" y="-28" width="26" height="9" rx="4" fill="#223"/>'
                f'<line x1="26" y1="10" x2="84" y2="62" stroke="#16202f" stroke-width="4"/><line x1="-24" y1="10" x2="-70" y2="62" stroke="#16202f" stroke-width="4"/></g>')
    b += skier(560, 560, 1.55, "#e12d3f") + skier(300, 470, .85, "#1c66d9") + skier(860, 440, .7, "#f2b81c")
    for i in range(30): random.seed(i); b += f'<circle cx="{480+random.randint(-90,40)}" cy="{640+random.randint(-30,40)}" r="{random.uniform(2,6):.1f}" fill="#fff" opacity=".8"/>'
    return svg(b, d)
def food():
    d = '<linearGradient id="wall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3a2418"/><stop offset="1" stop-color="#6b4429"/></linearGradient><linearGradient id="tb" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8a5a35"/><stop offset="1" stop-color="#5e3a22"/></linearGradient><linearGradient id="win" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7fb6f0"/><stop offset="1" stop-color="#eaf4ff"/></linearGradient><radialGradient id="warm"><stop offset="0" stop-color="#ffcf80" stop-opacity=".75"/><stop offset="1" stop-color="#ffcf80" stop-opacity="0"/></radialGradient>'
    b = f'<rect width="{W}" height="{H}" fill="url(#wall)"/><rect x="90" y="60" width="520" height="330" fill="url(#win)"/>'
    b += '<polygon points="90,300 220,190 330,260 430,170 610,300 610,390 90,390" fill="#f4f8ff"/><polygon points="90,340 250,260 400,330 520,250 610,330 610,390 90,390" fill="#dbe7f7"/>'
    b += pine(170, 372, 60, "#1b4a44") + pine(520, 376, 70, "#1b4a44") + flakes(40, 6, (1, 2.4)).replace(f'cx="', 'cx="') 
    b += '<rect x="80" y="50" width="540" height="12" fill="#2a1a10"/><rect x="80" y="390" width="540" height="14" fill="#2a1a10"/><rect x="80" y="50" width="12" height="354" fill="#2a1a10"/><rect x="608" y="50" width="12" height="354" fill="#2a1a10"/><rect x="344" y="50" width="10" height="354" fill="#2a1a10"/>'
    b += '<circle cx="820" cy="130" r="150" fill="url(#warm)"/><line x1="820" y1="0" x2="820" y2="90" stroke="#1a110b" stroke-width="3"/><path d="M780,150 Q820,70 860,150 Z" fill="#c8703a"/><ellipse cx="820" cy="150" rx="40" ry="8" fill="#ffe3a0"/>'
    for i in range(14): random.seed(i); b += f'<circle cx="{random.randint(640,1060)}" cy="{random.randint(40,330)}" r="{random.randint(8,26)}" fill="#ffcf80" opacity="{random.uniform(.12,.3):.2f}" filter="url(#b4)"/>'
    b += '<polygon points="0,420 1080,380 1080,780 0,780" fill="url(#tb)"/>'
    for y in (470, 540, 620, 710): b += f'<line x1="0" y1="{y}" x2="1080" y2="{y-30}" stroke="#4a2c18" stroke-width="3" opacity=".6"/>'
    def plate(cx, cy, rx, ry, fill, extra=""): return f'<ellipse cx="{cx+10}" cy="{cy+14}" rx="{rx+8}" ry="{ry+6}" fill="#2a170c" opacity=".55"/><ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#fbf9f4"/><ellipse cx="{cx}" cy="{cy}" rx="{rx*.82}" ry="{ry*.82}" fill="{fill}"/>{extra}'
    b += plate(300, 560, 220, 70, "#f0e0b0", '<ellipse cx="300" cy="560" rx="120" ry="34" fill="none" stroke="#e1b84a" stroke-width="8"/><ellipse cx="300" cy="560" rx="52" ry="16" fill="#e8d49a"/>' + "".join(f'<circle cx="{300+random.randint(-100,100)}" cy="{560+random.randint(-26,26)}" r="4" fill="#b8402a"/>' for _ in range(24)))
    random.seed(2); b += plate(690, 520, 190, 56, "#7cb04e", "".join(f'<ellipse cx="{690+random.randint(-150,150)}" cy="{520+random.randint(-38,38)}" rx="6" ry="4" fill="{random.choice(["#3f8a3a","#a6d36a","#d8392c","#f1ecc8"])}"/>' for _ in range(220)))
    b += '<ellipse cx="560" cy="690" rx="200" ry="52" fill="#c89458"/><ellipse cx="560" cy="684" rx="170" ry="40" fill="#e8bd80"/><path d="M420,684 Q560,630 700,684" fill="none" stroke="#c08a4e" stroke-width="6"/>'
    b += plate(900, 640, 150, 44, "#fbf9f4", '<rect x="780" y="618" width="200" height="12" rx="6" fill="#7a3a22"/><rect x="790" y="640" width="190" height="12" rx="6" fill="#8a4326"/><rect x="800" y="660" width="170" height="10" rx="5" fill="#6e3220"/>')
    b += '<ellipse cx="960" cy="470" rx="62" ry="16" fill="#f5f2ec"/><path d="M920,380 L1000,380 L990,470 L930,470 Z" fill="#b8581c" opacity=".92"/><path d="M920,380 L1000,380 L998,396 L922,396 Z" fill="#f6b25a" opacity=".6"/><path d="M950,350 q-12,-26 6,-46 q-10,-26 8,-44" fill="none" stroke="#fff" stroke-width="5" opacity=".55" filter="url(#b2)"/>'
    return svg(b, d)
def village():
    d = '<linearGradient id="sk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7aa8e0"/><stop offset="1" stop-color="#ffd9b0"/></linearGradient><linearGradient id="st" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#eaf0fb"/><stop offset="1" stop-color="#a9b8d8"/></linearGradient><pattern id="stone" width="34" height="22" patternUnits="userSpaceOnUse"><rect width="34" height="22" fill="#b8a68c"/><rect x="1" y="1" width="15" height="9" rx="2" fill="#c6b69c"/><rect x="18" y="1" width="15" height="9" rx="2" fill="#aa987e"/><rect x="9" y="12" width="15" height="9" rx="2" fill="#bfae94"/></pattern>'
    b = f'<rect width="{W}" height="{H}" fill="url(#sk)"/><polygon points="0,330 200,170 380,290 560,140 760,280 1080,180 1080,420 0,420" fill="#e8eefb"/><polygon points="560,140 600,210 560,200 530,240" fill="#fff"/><polygon points="0,380 300,290 640,370 1080,300 1080,480 0,480" fill="#d6e1f5"/>'
    def house(x, y, w, h, flip=0):
        o = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#stone)"/><rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#000" opacity=".12"/><polygon points="{x-12},{y+2} {x+w/2},{y-h*.45} {x+w+12},{y+2}" fill="#b4533a"/><polygon points="{x-12},{y+2} {x+w/2},{y-h*.45} {x+w+12},{y+2}" fill="#fff" opacity=".0"/><polygon points="{x-14},{y+4} {x+w/2},{y-h*.47} {x+w/2},{y-h*.38} {x-6},{y+10}" fill="#f8fbff"/>'
        for fx in (.14, .6): o += f'<path d="M{x+w*fx},{y+h*.55} v-{h*.25} a{w*.1},{w*.1} 0 0 1 {w*.2},0 v{h*.25} Z" fill="#ffc86a"/><path d="M{x+w*fx},{y+h*.55} v-{h*.25} a{w*.1},{w*.1} 0 0 1 {w*.2},0 v{h*.25} Z" fill="#ffc86a" filter="url(#b4)" opacity=".8"/>'
        return o + f'<path d="M{x+w*.38},{y+h} v-{h*.3} a{w*.12},{w*.12} 0 0 1 {w*.24},0 v{h*.3} Z" fill="#4a2e20"/>'
    b += house(30, 330, 250, 190) + house(840, 300, 220, 220) + house(380, 380, 170, 130) + house(590, 370, 190, 140)
    b += '<polygon points="0,780 0,540 1080,540 1080,780" fill="url(#st)"/><polygon points="430,540 650,540 1080,780 0,780" fill="#f6f9ff" opacity=".7"/><polygon points="470,540 610,540 760,780 330,780" fill="#dfe6f4" opacity=".8"/>'
    for x in (150, 940): b += f'<rect x="{x}" y="430" width="6" height="140" fill="#2a2a32"/><circle cx="{x+3}" cy="424" r="14" fill="#ffd27a"/><circle cx="{x+3}" cy="424" r="34" fill="#ffd27a" opacity=".4" filter="url(#b4)"/>'
    random.seed(11)
    for x in (320, 760): b += pine(x, 548, 100, "#17433d")
    b += flakes(120, 9, (1.2, 3.6))
    return svg(b, d)
if __name__ == "__main__":
    from playwright.sync_api import sync_playwright
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    with sync_playwright() as p:
        br = p.chromium.launch(); pg = br.new_page(viewport={"width": W, "height": H})
        for n, f in (("winter", winter), ("ski", ski), ("food", food), ("village", village)):
            pg.set_content(f'<body style="margin:0">{f()}</body>'); pg.screenshot(path=f"{out}/{n}.png"); print(n)
        br.close()
