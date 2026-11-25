# ASLNS Â· @ft.aslns Â· 2026. See LICENSE.txt.
# Space pause, R restart, S screenshot, Esc quit.
import math
from pathlib import Path
import sys
import time
import numpy as np
import pygame

MODE = 'BUTTERFLY-HEART'
TITLE = 'Butterfly Heart - ASLNS'
LOOP = 18.0
W, H = 1080, 960
CW, CH, COLS, ROWS = 8, 10, 135, 80
MONO = 'consolas,dejavusansmono,couriernew,monospace'
RAMP = ' .,:;+*ox%#@'
NAME = 'Your name'

def heart(a, scale=1, center=(135, 95)):
    return (center[0] + scale * 16 * math.sin(a) ** 3,
            center[1] - scale * (13*math.cos(a)-5*math.cos(2*a)-2*math.cos(3*a)-math.cos(4*a)))

def ellipse(surf, color, center, size, angle=0):
    points = [(center[0]+math.cos(a)*size[0]*math.cos(angle)-math.sin(a)*size[1]*math.sin(angle),
               center[1]+math.cos(a)*size[0]*math.sin(angle)+math.sin(a)*size[1]*math.cos(angle))
              for a in np.linspace(0, math.tau, 38, endpoint=False)]
    pygame.draw.polygon(surf, color, points)

def butterfly(surf, center, t, color, size=1, mirror=1):
    x,y=center
    flap=.35+.65*abs(math.sin(t*6.2))
    for side in (-1,1):
        ellipse(surf,color,(x+side*9*size*flap,y-5*size),(12*size*flap,10*size),side*-.45)
        ellipse(surf,tuple(int(c*.75) for c in color),(x+side*7*size*flap,y+6*size),(9*size*flap,8*size),side*.5)
        pygame.draw.line(surf,(255,225,240),(x,y),(x+side*15*size*flap,y-10*size),1)
        pygame.draw.line(surf,(255,210,240),(x,y-9*size),(x+side*4*size,y-14*size),1)
    ellipse(surf,(255,231,245),(x,y),(1.6*size,9*size))

def star(surf,x,y,shine,color):
    brightness=max(0.08,shine)
    color=tuple(int(c*brightness) for c in color)
    pygame.draw.line(surf,color,(x-1,y),(x+1,y))
    pygame.draw.line(surf,color,(x,y-1),(x,y+1))

def flower(surf,x,y,size,kind,t,index):
    opening=min(1,max(.03,(t-1-index*.45)/4))
    sway=math.sin(t*.6+index)*2
    x+=sway
    for side in (-1,1):
        ellipse(surf,(59,169,100),(x+side*12,y+size+13),(13,4),side*-.55)
    if kind=='rose':
        for j in range(17):
            a=j*2.39996+t*.03
            r=math.sqrt(j/17)*size*.65*opening
            ellipse(surf,((245,61,107) if j%2 else (255,115,153)),
                    (x+math.cos(a)*r,y+math.sin(a)*r),(size*.37*opening,size*.23*opening),a)
        ellipse(surf,(255,173,190),(x,y),(size*.16,size*.13))
    else:
        count=12 if kind=='white' else 9
        color=(245,243,228) if kind=='white' else (245,140,207)
        for j in range(count):
            a=j*math.tau/count
            r=size*.65*opening
            ellipse(surf,color,(x+math.cos(a)*r,y+math.sin(a)*r),
                    (size*.55*opening,size*.19*opening),a)
        ellipse(surf,(255,197,72),(x,y),(size*.28,size*.28))

def cat(surf,x,y,color,flip,t):
    ellipse(surf,color,(x,y-17),(13,28))
    ellipse(surf,color,(x+flip*2,y-47),(16,14))
    pygame.draw.polygon(surf,color,[(x-12,y-51),(x-13,y-71),(x-2,y-58)])
    pygame.draw.polygon(surf,color,[(x+3,y-58),(x+14,y-70),(x+14,y-49)])
    # A small curled tail rests beside each cat.
    pts=[(x+flip*(10+16*math.sin(a)),y-1-8*(1-math.cos(a))) for a in np.linspace(0,4.5,60)]
    pygame.draw.lines(surf,color,False,pts,5)
    eye=(55,35,57)
    for side in (-1,1):
        pygame.draw.line(surf,eye,(x+flip*2+side*5-2,y-47),(x+flip*2+side*5+2,y-46),1)
    pygame.draw.line(surf,(225,144,161),(x-3,y-40),(x+3,y-40),1)

def scene(t):
    surf=pygame.Surface((270,216))
    # Stable stars with independent twinkles; no random flickering between frames.
    for i in range(70):
        x=(i*79+17)%266+2; y=(i*47+23)%207+3
        shine=.12+.45*max(0,math.sin(t*1.2+i*2.7))**7
        star(surf,x,y,shine,(163,160,221))
    if MODE=='BUTTERFLY-HEART':
        reveal=min(1,max(0,(t-1)/5))
        for j in range(int(350*reveal)):
            a=j/350*math.tau
            x,y=heart(a,5.4,(135,102))
            star(surf,x,y,.45+.45*math.sin(j*.35-t*2)**2,(255,105,179))
        a=t*.65
        for index,(offset,color) in enumerate(((0,(255,157,204)),(math.pi,(171,156,255)))):
            target=heart(a+offset,5.4,(135,102))
            start=(30+210*index,120)
            u=min(1,t/4)
            pos=(start[0]*(1-u)+target[0]*u,start[1]*(1-u)+target[1]*u)
            butterfly(surf,pos,t+index,color,1.12)
    elif MODE=='BLOOMING-BOUQUET':
        blooms=[(95,103,18,'white'),(168,99,20,'white'),(112,73,25,'pink'),(151,64,25,'rose'),(133,102,29,'rose')]
        growth=min(1,t/4)
        for index,(x,y,size,kind) in enumerate(blooms):
            end=(135+(x-135)*growth,184+(y-184)*growth)
            pygame.draw.line(surf,(55,155,88),(135,186),end,2)
        pygame.draw.polygon(surf,(92,66,126),[(94,130),(176,130),(145,196),(127,196)])
        pygame.draw.polygon(surf,(147,105,169),[(94,130),(133,155),(127,196)])
        for index,(x,y,size,kind) in enumerate(blooms):
            if t>1+index*.45: flower(surf,x,y,size,kind,t,index)
        for side in (-1,1):
            ellipse(surf,(255,133,170),(135+side*12,172),(14,7),side*.35)
            pygame.draw.line(surf,(255,170,193),(135,174),(135+side*12,195),3)
        ellipse(surf,(255,194,210),(135,172),(5,5))
    elif MODE=='MOONLIGHT-CATS':
        pygame.draw.line(surf,(94,107,153),(25,188),(245,188),2)
        moon=[heart(a,3.0,(135,58)) for a in np.linspace(0,math.tau,200)]
        pygame.draw.polygon(surf,(255,218,156),moon)
        cut=[heart(a,2.55,(143,52)) for a in np.linspace(0,math.tau,200)]
        pygame.draw.polygon(surf,(0,0,0),cut)
        cat(surf,119,184,(192,169,226),-1,t)
        cat(surf,147,184,(249,209,183),1,t)
        for j in range(4):
            phase=(t*.15+j*.27)%1
            x=126+math.sin(t+j*2)*10
            points=[heart(a,.18+phase*.2,(x,123-phase*22)) for a in np.linspace(0,math.tau,30)]
            pygame.draw.polygon(surf,tuple(int(c*(1-phase)) for c in (255,131,174)),points)
    else:
        beat=1+.045*math.sin(t*3.6)+.018*math.sin(t*7.2)
        for j in range(7):
            scale=(5.1+j*.09)*beat
            color=(255-int(j*16),87-int(j*6),151-int(j*9))
            pts=[heart(a,scale,(135,103)) for a in np.linspace(0,math.tau,250)]
            pygame.draw.lines(surf,color,True,pts,1)
        for i in range(45):
            phase=(i/45+t*.035)%1
            a=i*2.39996
            x,y=heart(a,5.5+phase*2,(135,103))
            star(surf,x,y,(1-phase)*.8,(255,146,191))
    return surf

class Canvas:
    def __init__(self):
        font=pygame.font.SysFont(MONO,11)
        atlas=[]
        for char in RAMP:
            s=pygame.Surface((CW,CH)); glyph=font.render(char,True,'white')
            s.blit(glyph,((CW-glyph.get_width())//2,(CH-glyph.get_height())//2))
            atlas.append(pygame.surfarray.array3d(s)[:,:,0].T)
        self.atlas=np.stack(atlas)

    def draw(self,t):
        source=pygame.transform.smoothscale(scene(t),(COLS,ROWS))
        color=pygame.surfarray.array3d(source).transpose(1,0,2).astype(np.float32)
        value=color.max(axis=2)
        indices=np.where(value>4,np.clip((value/255*8+3).astype(int),1,len(RAMP)-1),0)
        mask=self.atlas[indices].transpose(0,2,1,3).reshape(ROWS*CH,COLS*CW).astype(np.float32)/255
        tint=np.repeat(np.repeat(np.clip(color*1.7,0,255),CH,axis=0),CW,axis=1)
        pixels=(tint*mask[:,:,None]).astype(np.uint8)
        return pygame.surfarray.make_surface(pixels.transpose(1,0,2))

def main():
    global NAME
    pygame.init()
    info=pygame.display.Info()
    scale=min(1,.85*info.current_h/H,.95*info.current_w/W)
    window=pygame.display.set_mode((int(W*scale),int(H*scale)))
    pygame.display.set_caption(TITLE)
    screen=pygame.Surface((W,H))
    font=pygame.font.SysFont(MONO,18)
    namefont=pygame.font.SysFont('segoeui,dejavusans,arial',52)
    clock=pygame.time.Clock(); canvas=Canvas()
    t,paused,editing=0.,False,False
    field=pygame.Rect(190,850,700,52)
    art=canvas.draw(t)
    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit(); return
            if event.type==pygame.MOUSEBUTTONDOWN and MODE=='NAME-HEART':
                editing=field.collidepoint(event.pos[0]/scale,event.pos[1]/scale)
                if editing: pygame.key.start_text_input()
                else: pygame.key.stop_text_input()
            if event.type==pygame.TEXTINPUT and editing:
                if NAME=='Your name': NAME=''
                NAME=(NAME+''.join(c for c in event.text if c.isprintable()))[:24]
            if event.type==pygame.KEYDOWN:
                if editing:
                    if event.key==pygame.K_BACKSPACE: NAME=NAME[:-1]
                    elif event.key in (pygame.K_RETURN,pygame.K_ESCAPE): editing=False; pygame.key.stop_text_input()
                elif event.key==pygame.K_ESCAPE: pygame.quit(); return
                elif event.key==pygame.K_SPACE: paused=not paused
                elif event.key==pygame.K_r: t=0.
                elif event.key==pygame.K_s:
                    pygame.image.save(screen,str(Path(__file__).with_name(f'{MODE.lower()}_{int(time.time())}.png')))
        dt=clock.tick(30)/1000
        if not paused: t+=min(dt,1/15); t%=LOOP; art=canvas.draw(t)
        screen.fill((0,0,0)); screen.blit(art,(0,35))
        glow=pygame.transform.smoothscale(art,(135,100))
        if hasattr(pygame.transform,'gaussian_blur'): glow=pygame.transform.gaussian_blur(glow,2)
        glow=pygame.transform.smoothscale(glow,(W,800)); glow.fill((75,75,75),special_flags=pygame.BLEND_MULT)
        screen.blit(glow,(0,35),special_flags=pygame.BLEND_ADD)
        if MODE=='NAME-HEART':
            label=namefont.render(NAME or 'Your name',True,(255,211,233))
            if label.get_width()>590:
                label=pygame.transform.smoothscale(label,(590,int(label.get_height()*590/label.get_width())))
            screen.blit(label,(W//2-label.get_width()//2,385))
            pygame.draw.rect(screen,(20,15,26),field,border_radius=10)
            pygame.draw.rect(screen,(255,134,183) if editing else (100,76,109),field,2,border_radius=10)
            value=font.render((NAME or 'Click here and type a name')+('|' if editing and int(t*2)%2 else ''),True,(245,215,235))
            screen.blit(value,(field.x+18,field.y+16))
        else:
            caption={'BUTTERFLY-HEART':'two little wings, one lovely feeling',
                     'BLOOMING-BOUQUET':'a little bouquet, just because',
                     'MOONLIGHT-CATS':'the nicest place is next to you'}[MODE]
            text=font.render(caption,True,(214,168,202)); screen.blit(text,(W//2-text.get_width()//2,867))
        screen.blit(font.render('@ft.aslns Â· 2026',True,(120,110,135)),(50,918))
        timer=font.render(f't {t:05.2f}s',True,(220,143,184)); screen.blit(timer,(W-170,918))
        window.blit(pygame.transform.smoothscale(screen,window.get_size()),(0,0))
        pygame.display.flip()

if __name__=='__main__':
    sys.exit(main())
