from PIL import Image, ImageDraw, ImageFont
import math

W,H,FPS = 1080,1920,30
CREAM=(245,241,232); INK=(38,36,31); MUTED=(138,132,120); GREEN=(47,107,79); RED=(181,72,62); LINE=(217,210,194); PAPER=(250,248,242)
SER = lambda s: ImageFont.truetype("/tmp/CormorantG-Bold.ttf", s)
SERI= lambda s: ImageFont.truetype("/tmp/CormorantG-SemiItalic.ttf", s)
MONO= lambda s: ImageFont.truetype("/tmp/SpaceMono.ttf", s)
MONOB= lambda s: ImageFont.truetype("/tmp/SpaceMono-Bold.ttf", s)

CELL=220; BX=(W-3*CELL)//2; BY=760
LAYOUT=[["C","S","C"],["C","S","C"],["C","S","C"]]
BASE={"S":[0,2],"C":[0,1]}
D=[(-1,0),(0,1),(1,0),(0,-1)]
def conns(rots,r,c): return [(d+rots[r][c])%4 for d in BASE[LAYOUT[r][c]]]
def flow(rots):
    live=set(); out=False
    if 3 in conns(rots,1,0):
        live.add((1,0)); q=[(1,0)]
        while q:
            r,c=q.pop(0)
            for d in conns(rots,r,c):
                if r==1 and c==2 and d==1: out=True; continue
                nr,nc=r+D[d][0],c+D[d][1]
                if 0<=nr<3 and 0<=nc<3 and (nr,nc) not in live and (d+2)%4 in conns(rots,nr,nc):
                    live.add((nr,nc)); q.append((nr,nc))
    return live,out

def tile_glyph(t, color, angle):
    im = Image.new("RGBA",(CELL,CELL),(0,0,0,0))
    g = ImageDraw.Draw(im)
    wdt=34; m=CELL//2
    if t=="S": g.line([m,0,m,CELL],fill=color,width=wdt)
    else:
        g.line([m,0,m,m],fill=color,width=wdt)
        g.line([m,m,CELL,m],fill=color,width=wdt)
        g.ellipse([m-wdt//2,m-wdt//2,m+wdt//2,m+wdt//2],fill=color)
    return im.rotate(-angle, resample=Image.BICUBIC)

def center(r,c): return (BX+c*CELL+CELL//2, BY+r*CELL+CELL//2)
def ease(t): return 3*t*t-2*t*t*t

def draw_frame(rots, anim, live, cursor, ripple, texts, shake=0, endcard=0, tapcount=0):
    img = Image.new("RGB",(W,H),CREAM)
    d = ImageDraw.Draw(img,"RGBA")
    ox = int(math.sin(shake*2.4)*14*shake) if shake>0 else 0
    # frame border
    d.rectangle([40+ox,40,W-40+ox,H-40],outline=INK,width=4)
    d.rectangle([56+ox,56,W-56+ox,H-56],outline=INK,width=1)
    # kicker + headline
    d.text((W/2+ox,220),"THE ALMANAC · PIPES · DAILY",font=MONO(30),fill=MUTED,anchor="mm")
    for (y,txt,font,col) in texts:
        d.text((W/2+ox,y),txt,font=font,fill=col,anchor="mm")
    # board
    d.rectangle([BX-6+ox,BY-6,BX+3*CELL+6+ox,BY+3*CELL+6],outline=INK,width=5)
    for r in range(3):
        for c in range(3):
            x0,y0=BX+c*CELL+ox,BY+r*CELL
            d.rectangle([x0,y0,x0+CELL,y0+CELL],fill=PAPER,outline=LINE,width=2)
    # pipes
    for r in range(3):
        for c in range(3):
            t=LAYOUT[r][c]
            ang = rots[r][c]*90
            if anim and anim[0]==(r,c): ang = (rots[r][c]+anim[1]-1)*90 + anim[1]*0  # handled below
            col = GREEN if (r,c) in live else MUTED
            if anim and anim[0]==(r,c):
                base_rot = anim[2]; prog = anim[1]
                ang = (base_rot+ease(prog))*90
                col = MUTED
            glyph = tile_glyph(t, col, ang)
            img.paste(glyph,(BX+c*CELL+ox,BY+r*CELL),glyph)
    # grid lines on top
    for r in range(3):
        for c in range(3):
            x0,y0=BX+c*CELL+ox,BY+r*CELL
            d.rectangle([x0,y0,x0+CELL,y0+CELL],outline=LINE,width=2)
    d.rectangle([BX-6+ox,BY-6,BX+3*CELL+6+ox,BY+3*CELL+6],outline=INK,width=5)
    # IN / OUT
    iy = BY+CELL+CELL//2
    d.text((BX-70+ox,iy),"IN →",font=MONOB(30),fill=GREEN if live else MUTED,anchor="mm")
    d.text((BX+3*CELL+90+ox,iy),"→ OUT",font=MONOB(30),fill=MUTED,anchor="mm")
    d.text((W/2+ox,BY+3*CELL+90),"taps: %d"%tapcount,font=MONO(32),fill=MUTED,anchor="mm")
    # ripple
    if ripple:
        (rx,ry),p = ripple
        rad = 30+p*90
        a = int(160*(1-p))
        d.ellipse([rx-rad+ox,ry-rad,rx+rad+ox,ry+rad],outline=(47,107,79,a),width=8)
    # cursor
    if cursor:
        cx,cy = cursor
        d.ellipse([cx-34+ox,cy-34,cx+34+ox,cy+34],fill=(38,36,31,50))
        d.ellipse([cx-26+ox,cy-26,cx+26+ox,cy+26],fill=(250,248,242,235),outline=INK,width=5)
    # end card overlay
    if endcard>0:
        ov = Image.new("RGBA",(W,H),(245,241,232,int(255*min(endcard,1))))
        img.paste(ov,(0,0),ov)
        if endcard>=1:
            d = ImageDraw.Draw(img,"RGBA")
            d.rectangle([40,40,W-40,H-40],outline=INK,width=4)
            d.text((W/2,640),"one tap away.",font=SER(120),fill=INK,anchor="mm")
            d.text((W/2,790),"could you have finished it?",font=SERI(66),fill=(138,132,120),anchor="mm")
            d.rectangle([W/2-320,980,W/2+320,1120],fill=INK)
            d.text((W/2,1050),"PLAY TODAY'S PUZZLE",font=MONOB(40),fill=CREAM,anchor="mm")
            d.text((W/2,1330),"The Almanac",font=SER(84),fill=INK,anchor="mm")
            d.text((W/2,1420),"feel clever through play",font=SERI(46),fill=(138,132,120),anchor="mm")
    return img

# ---------- timeline ----------
rots=[[0,0,1],[2,1,3],[2,1,3]]   # start state; path targets: (1,0)3 (0,0)1 (0,1)1 (0,2)2 (1,2)0
taps=[  # (frame, tile)
 (75,(1,0)), (115,(0,0)), (155,(0,1)), (195,(0,2)), (262,(0,1))  # last one = the fatal mistake
]
ROT_FRAMES=9
frames=[]
tapcount=0
live=set()
cursor_path=[]  # computed per frame
HEAD=[(410,"just connect",SER(110),INK),(520,"the water.",SER(110),INK)]

def cursor_at(f):
    # waypoints: appear near board at 55, then tile centers at tap frames, wrong-turn drama before last tap
    pts=[(55,(W/2,BY+3*CELL+180))]
    for tf,(r,c) in taps[:4]: pts.append((tf,center(r,c)))
    pts.append((225,center(1,2)))          # heads toward the RIGHT tile...
    pts.append((248,(center(1,2)[0]-90,center(1,2)[1]-60)))
    pts.append((262,center(0,1)))          # ...then swerves and taps the wrong one
    pts.append((330,center(0,1)))
    if f<pts[0][0]: return None
    for i in range(len(pts)-1):
        f0,p0=pts[i]; f1,p1=pts[i+1]
        if f0<=f<=f1:
            t=ease((f-f0)/max(1,(f1-f0)))
            return (p0[0]+(p1[0]-p0[0])*t, p0[1]+(p1[1]-p0[1])*t)
    return pts[-1][1]

anim=None; ripple=None
pending=None
for f in range(470):
    texts=list(HEAD)
    shake=0; endcard=0
    # tap triggers
    for tf,(r,c) in taps:
        if f==tf:
            anim=[(r,c),0.0,rots[r][c]]
            ripple=[center(r,c),0.0]
            tapcount+=1
    if anim:
        anim[1]+=1.0/ROT_FRAMES
        if anim[1]>=1.0:
            (r,c)=anim[0]; rots[r][c]=(rots[r][c]+1)%4; anim=None
            live,_=flow(rots)
    if ripple:
        ripple[1]+=1.0/12
        if ripple[1]>=1: ripple=None
    if not anim:
        live,_=flow(rots)
    # narrative texts
    if 208<=f<262: texts.append((640,"one. tile. left.",SERI(72),GREEN))
    if 271<=f<340:
        texts.append((640,"NO. not that one.",SERI(76),RED))
        if f<295: shake=max(0,1-(f-271)/24)
    if f>=340: endcard=min(1,(f-340)/18)
    img = draw_frame(rots,anim,live,cursor_at(f),tuple(ripple) if ripple else None,texts,shake,endcard,tapcount)
    img.save("/tmp/adframes/f%04d.png"%f)
print("frames done, final live:",len(live))
