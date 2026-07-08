from PIL import Image, ImageDraw, ImageFont
W,H = 1080,1350
CREAM="#f5f1e8"; INK="#26241f"; MUTED="#8a8478"; ACCENT="#2f6b4f"; GOLD="#c9a24b"; RED="#b5483e"
SER = lambda s: ImageFont.truetype("/tmp/CormorantG-Bold.ttf", s)
SERI= lambda s: ImageFont.truetype("/tmp/CormorantG-SemiItalic.ttf", s)
MONO= lambda s: ImageFont.truetype("/tmp/SpaceMono.ttf", s)
MONOB=lambda s: ImageFont.truetype("/tmp/SpaceMono-Bold.ttf", s)

def base():
    img = Image.new("RGB",(W,H),CREAM)
    d = ImageDraw.Draw(img,"RGBA")
    # thin frame like an almanac page
    d.rectangle([36,36,W-36,H-36], outline=INK, width=3)
    d.rectangle([48,48,W-48,H-48], outline=INK, width=1)
    return img,d

def footer(d, tag):
    d.text((W/2, H-120), "The Almanac", font=SER(56), fill=INK, anchor="mm")
    d.text((W/2, H-76), tag, font=MONO(24), fill=MUTED, anchor="mm")

def ctext(d,y,txt,font,fill=INK):
    d.text((W/2,y),txt,font=font,fill=fill,anchor="mm")

def grid(d, x, y, cell, n, fills=None, nums=None):
    for r in range(n):
        for c in range(n):
            x0,y0 = x+c*cell, y+r*cell
            f = fills.get((r,c)) if fills else None
            if f: d.rectangle([x0,y0,x0+cell,y0+cell], fill=f)
            d.rectangle([x0,y0,x0+cell,y0+cell], outline=INK, width=2)
            if nums and (r,c) in nums:
                d.text((x0+cell/2,y0+cell/2), str(nums[(r,c)]), font=MONOB(int(cell*.42)), fill=INK, anchor="mm")

# ---- 1. brain rot detox (anti-scroll split)
img,d = base()
d.text((W/2,120),"C-01 · HOOK: GUILT / SELF-IMPROVEMENT",font=MONO(22),fill=MUTED,anchor="mm")
ctext(d,300,"brain rot,",SERI(120),MUTED)
ctext(d,430,"meet brain time.",SER(120))
# doomscroll phone vs puzzle
px,py,pw,ph = 180,560,290,480
d.rounded_rectangle([px,py,px+pw,py+ph],radius=36,outline=MUTED,width=4)
for i in range(6):
    d.rounded_rectangle([px+30,py+40+i*70,px+pw-30,py+80+i*70],radius=10,fill=(138,132,120,70))
d.line([px+40,py+ph-60,px+pw-40,py+60],fill=RED,width=8)
qx = 610
grid(d, qx, 600, 100, 4, fills={(0,0):"#dfe8db",(0,1):"#dfe8db",(1,0):"#dfe8db",(1,1):"#dfe8db"}, nums={(0,0):4,(2,3):2,(3,1):3})
d.text((px+pw/2, py+ph+50), "2 hrs · nothing", font=MONO(26), fill=RED, anchor="mm")
d.text((qx+200, 600+400+50), "5 min · sharper", font=MONO(26), fill=ACCENT, anchor="mm")
footer(d,"a daily ritual for your brain")
img.save("creatives/c01_brainrot.png")

# ---- 2. five minutes zero regrets
img,d = base()
d.text((W/2,120),"C-02 · HOOK: TIME REFRAME",font=MONO(22),fill=MUTED,anchor="mm")
ctext(d,420,"5 minutes.",SER(170))
ctext(d,580,"0 regrets.",SER(170))
ctext(d,760,"the only feed that feeds you back",SERI(58),MUTED)
grid(d, W/2-150, 860, 100, 3, fills={(1,1):"#dfe8db"}, nums={(0,0):2,(1,1):1,(2,2):3})
footer(d,"smart puzzles · no noise")
img.save("creatives/c02_fivemin.png")

# ---- 3. NYT replacement
img,d = base()
d.text((W/2,120),"C-03 · HOOK: HABIT TRANSFER (PUZZLE PEOPLE)",font=MONO(22),fill=MUTED,anchor="mm")
ctext(d,380,"finished the morning",SER(96))
ctext(d,480,"crossword by 9am?",SER(96))
ctext(d,650,"your brain is just warming up.",SERI(64),ACCENT)
grid(d, W/2-200, 780, 100, 4, nums={(0,0):3,(1,2):4,(3,0):2,(2,3):4})
footer(d,"10 puzzle types · new every day")
img.save("creatives/c03_nyt.png")

# ---- 4. streak
img,d = base()
d.text((W/2,120),"C-04 · HOOK: STREAK / LOSS AVERSION",font=MONO(22),fill=MUTED,anchor="mm")
ctext(d,340,"day 47.",SER(200),ACCENT)
ctext(d,500,"you wouldn't dare stop now.",SERI(64))
# dot calendar
for r in range(4):
    for c in range(12):
        x0,y0 = 180+c*62, 640+r*62
        idx = r*12+c
        col = ACCENT if idx<47 else "#d9d2c2"
        d.ellipse([x0,y0,x0+38,y0+38], fill=col)
d.text((W/2, 950), "one small win, every single day", font=MONO(28), fill=MUTED, anchor="mm")
footer(d,"don't break the chain")
img.save("creatives/c04_streak.png")

# ---- 5. ego bait / challenge
img,d = base()
d.text((W/2,120),"C-05 · HOOK: CHALLENGE / EGO BAIT",font=MONO(22),fill=MUTED,anchor="mm")
ctext(d,320,"92% of players",SER(110))
ctext(d,430,"quit this on expert.",SER(110))
ctext(d,560,"you're different, right?",SERI(62),RED)
grid(d, W/2-250, 660, 100, 5, nums={(0,1):6,(1,4):4,(2,2):5,(4,0):4,(3,3):6})
footer(d,"expert mode is waiting")
img.save("creatives/c05_expert.png")

# ---- 6. calm
img,d = base()
d.text((W/2,120),"C-06 · HOOK: CALM / ANTI-NOISE",font=MONO(22),fill=MUTED,anchor="mm")
ctext(d,400,"no ads screaming.",SER(92))
ctext(d,500,"no lives. no timers.",SER(92))
ctext(d,600,"just you and the puzzle.",SER(92))
ctext(d,770,"the quietest game on your phone",SERI(56),MUTED)
d.line([W/2-320,860,W/2+320,860],fill=GOLD,width=3)
grid(d, W/2-150, 910, 100, 3, fills={(0,0):"#efe9da",(1,1):"#efe9da",(2,2):"#efe9da"})
footer(d,"minimalist by design")
img.save("creatives/c06_calm.png")

# ---- 7. coffee ritual
img,d = base()
d.text((W/2,120),"C-07 · HOOK: MORNING RITUAL",font=MONO(22),fill=MUTED,anchor="mm")
ctext(d,360,"coffee.",SER(130),MUTED)
ctext(d,490,"almanac.",SER(130),ACCENT)
ctext(d,620,"then the world.",SER(130))
# coffee cup
cx,cy=W/2-60,800
d.ellipse([cx-90,cy,cx+90,cy+60],outline=INK,width=5)
d.rectangle([cx-90,cy+30,cx+90,cy+140],fill=CREAM)
d.line([cx-90,cy+30,cx-80,cy+150],fill=INK,width=5)
d.line([cx+90,cy+30,cx+80,cy+150],fill=INK,width=5)
d.arc([cx-70,cy+140,cx+70,cy+180],0,180,fill=INK,width=5)
d.arc([cx+80,cy+45,cx+150,cy+115],270,90,fill=INK,width=5)
for i,ox in enumerate([-30,0,30]):
    d.arc([cx+ox-12,cy-70,cx+ox+12,cy-20],90,270,fill=MUTED,width=4)
footer(d,"tomorrow's puzzle drops at midnight")
img.save("creatives/c07_coffee.png")

# ---- 8. feel clever (brand)
img,d = base()
d.text((W/2,120),"C-08 · HOOK: IDENTITY / BRAND",font=MONO(22),fill=MUTED,anchor="mm")
ctext(d,420,"that little rush",SER(110))
ctext(d,530,"when it clicks.",SER(110))
# solved grid with check
grid(d, W/2-200, 660, 100, 4, fills={(r,c):"#dfe8db" for r in range(4) for c in range(4)})
d.line([W/2-70,860,W/2-10,930],fill=ACCENT,width=14)
d.line([W/2-10,930,W/2+110,760],fill=ACCENT,width=14)
ctext(d,1130,"feel clever through play",SERI(60),ACCENT)
img.save("creatives/c08_clever.png")
print("8 creatives saved")
