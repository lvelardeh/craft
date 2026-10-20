"""Motor Otto: ilustración original con paleta y composición inspiradas en la referencia.
Ejecutar desde cualquier directorio: python otto/render_estilo.py
Requiere Pillow, numpy, FFmpeg; entrada narracion.mp3.
"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageFilter
import math,subprocess,numpy as np
P=Path(__file__).parent
W,H,FPS,D=1280,720,24,25.5
PURPLE='#390a49'; YELLOW='#f5ef32'; DARK='#401049'
font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
fonts={n:ImageFont.truetype(font,n) for n in [15,16,18,20,22,24,26,28,38]}
def txt(d,xy,s,n=20,c=DARK):d.text(xy,s,font=fonts[n],fill=c)
def tag(d,xy,s,n=20):
 box=d.textbbox((0,0),s,font=fonts[n]);w=box[2]+20;h=box[3]-box[1]+14
 d.rectangle((xy[0],xy[1],xy[0]+w,xy[1]+h),fill=YELLOW);txt(d,(xy[0]+10,xy[1]+3),s,n)
 return w,h
def smooth(x):return (1-math.cos(math.pi*max(0,min(1,x))))/2
# Reference palette: cyan field, mint light and yellow annotation cards.
yy,xx=np.mgrid[0:H,0:W];g=np.exp(-(((xx-510)/490)**2+((yy-555)/210)**2)*1.5)
bg=np.zeros((H,W,3));top=np.array([28,172,214]);bottom=np.array([57,197,180]);bg[:]=top+(bottom-top)*yy[:,:,None]/H
bg+=g[:,:,None]*np.array([51,49,-30]);BACKGROUND=Image.fromarray(np.uint8(np.clip(bg,0,255)))
scenes=[(5.09,6.26,8.78,'Admisión','Válvula de admisión'),(9.31,10.45,12.51,'Compresión','Mezcla comprimida'),(13.07,16.05,18.41,'Combustión y expansión','Bujía'),(19.01,20.02,22.30,'Escape','Válvula de escape')]
def engine(a,s,t,intro=False):
 im=Image.new('RGBA',(W,H));d=ImageDraw.Draw(im)
 # Projected extrusion: front section and rear casing.
 d.polygon([(378,222),(434,176),(676,176),(732,222),(732,539),(676,584),(378,584)],fill='#551265')
 d.polygon([(676,176),(732,222),(732,539),(676,584)],fill='#280632')
 d.polygon([(378,222),(434,176),(676,176),(620,222)],fill='#7c438e')
 # Cooling fins, casting ribs, top cover and fasteners.
 for y in range(235,485,25):
  d.polygon([(363,y),(378,y-12),(378,y+5),(363,y+17)],fill='#5c246b')
  d.polygon([(677,y-12),(746,y-48),(746,y-36),(677,y+1)],fill='#4c165a')
 d.rounded_rectangle((355,182,692,226),8,fill='#4b115b');d.polygon([(355,182),(411,145),(747,145),(692,182)],fill='#89599c');d.polygon([(692,182),(747,145),(747,190),(692,226)],fill='#51145f')
 for x in [377,670]:
  d.ellipse((x-7,196,x+7,210),fill='#c4abd3');d.ellipse((x-3,200,x+3,206),fill='#573164')
 # Intake and exhaust runners.
 d.rounded_rectangle((285,205,420,251),16,fill='#4b155d');d.rectangle((300,217,425,237),fill='#9774ac')
 d.ellipse((278,205,310,251),fill='#2c083b');d.ellipse((284,213,304,244),fill='#6b437f')
 d.rounded_rectangle((636,205,765,251),16,fill='#4b155d');d.rectangle((650,217,755,237),fill='#9774ac')
 d.ellipse((749,205,779,251),fill='#32103e');d.ellipse((755,213,773,244),fill='#886098')
 # Visible cutaway chamber.
 d.rectangle((414,225,655,453),fill='#26072f')
 py=268+112*(1-math.cos(a))/2
 gas=['#62d8b0','#dda2c8','#f6b254','#b7abbf'][s]
 d.rectangle((425,238,644,py),fill=gas)
 if s==1:
  for k in range(15):
   gx=436+(k%5)*44;gy=243+(k//5)*max(3,(py-246)/3);d.ellipse((gx,gy,gx+4,gy+4),fill='#9d568d')
 if s==2 and 15.75<t<18.41:
  strength=max(0,1-(t-16)/2.4)
  for k in range(9):
   x=430+k*26;d.polygon([(x,py),(x+13,py-15-25*strength*(.5+.5*math.sin(t*13+k))),(x+26,py)],fill='#f4d55a')
 # Cylinder liner cut faces.
 d.rectangle((411,225,425,456),fill='#bfabd1');d.rectangle((644,225,659,456),fill='#8f6aab')
 for x in [414,647]:d.line((x,230,x,450),fill='#e0d3e7',width=2)
 # Valves, seats, springs and cam caps.
 for vx,opened in [(468,s==0 and 6.26<=t<=8.78 and not intro),(605,s==3 and 20.02<=t<=22.30 and not intro)]:
  off=14 if opened else 0
  d.rectangle((vx-8,225,vx+8,241),fill='#26072f')
  d.line((vx,171,vx,236+off),fill='#d1b5db',width=7)
  for k in range(6):d.line((vx-13,180+k*6,vx+13,185+k*6),fill='#613372',width=3)
  d.ellipse((vx-17,166,vx+17,179),fill='#ae8abd')
  d.polygon([(vx-23,235+off),(vx+23,235+off),(vx+14,243+off),(vx-14,243+off)],fill='#cbb6da')
 # Ceramic plug and threaded tip.
 d.rectangle((531,152,543,223),fill='#e5d6ea')
 for k in range(5):d.line((529,164+k*6,545,164+k*6),fill='#aa8bb7',width=3)
 d.rectangle((532,219,542,242),fill='#92709a');d.line((541,237,541,245,535,245),fill='#f0d95b',width=3)
 if s==2 and 15.75<=t<=16.15:
  d.polygon([(537+math.cos(k*math.pi/8)*(29 if k%2==0 else 8),249+math.sin(k*math.pi/8)*(29 if k%2==0 else 8)) for k in range(16)],fill='#fff986')
 # Crankcase with depth.
 d.rounded_rectangle((387,442,684,594),38,fill='#421050');d.rounded_rectangle((405,453,666,579),28,fill='#290731')
 for x,y in [(403,461),(668,461),(411,578),(662,578)]:
  d.ellipse((x-6,y-6,x+6,y+6),fill='#ac8cbe');d.line((x-3,y,x+3,y),fill='#4a205c',width=2)
 # Physically aligned rod and crank; crank turns once per two strokes.
 cx,cy=536,516;r=37;pin=(cx+r*math.sin(a),cy-r*math.cos(a))
 d.ellipse((cx-59,cy-59,cx+59,cy+59),fill='#562267',outline='#77428b',width=4)
 d.line((cx,cy,*pin),fill='#a889bd',width=25)
 d.line((*pin,cx,py+30),fill='#3c184d',width=22);d.line((*pin,cx,py+30),fill='#a687bb',width=14);d.line((pin[0]-3,pin[1],cx-3,py+30),fill='#cfb9dd',width=4)
 for px,pz in [(cx,cy),pin]:d.ellipse((px-11,pz-11,px+11,pz+11),fill='#c4a7d3');d.ellipse((px-5,pz-5,px+5,pz+5),fill='#4b225b')
 # Piston crown, rings and skirt.
 d.rounded_rectangle((427,py,642,py+49),7,fill='#ae8ac3');d.rectangle((430,py+8,640,py+13),fill='#5b2d70');d.rectangle((430,py+20,640,py+24),fill='#613477');d.rectangle((430,py+1,640,py+5),fill='#d1b8df')
 d.ellipse((527,py+29,545,py+47),fill='#68407e');d.ellipse((532,py+34,540,py+42),fill='#d0b8df')
 # Moving particles in inlet and outlet.
 if not intro and s in [0,3] and scenes[s][1]<=t<=scenes[s][2]:
  for k in range(20):
   if s==0:
    u=(t*1.1+k/20)%1;px=300+u*185;yy=226+max(0,u-.75)*140
   else:
    u=(t*1.4+k/20)%1;px=605+u*180;yy=226
   color='#c6ffe1' if s==0 else '#d3b5d3';d.ellipse((px,yy,px+5,yy+5),fill=color)
 return im,py
p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-an','-c:v','libx264','-preset','fast','-threads','2','-crf','18','-pix_fmt','yuv420p',str(P/'estilo-silent.mp4')],stdin=subprocess.PIPE)
for n in range(int(D*FPS)):
 t=n/FPS;intro=t<5.09;recap=t>=22.73;s=max([i for i,z in enumerate(scenes) if t>=z[0]],default=0)
 st,mo,en,title,part=scenes[s];u=smooth((t-mo)/(en-mo));a=(s+u)*math.pi
 if intro:a=.15*math.sin(t);title='Motor Otto'
 if recap:a=4*math.pi+(t-22.73)*math.pi*1.4;title='El ciclo se repite'
 layer,py=engine(a,s,t,intro or recap)
 # Slow, smooth camera moves on the full cutaway.
 zoom=1 if intro or recap else 1+.075*smooth((t-st)/1.1)
 if zoom!=1:
  layer=layer.transform((W,H),Image.Transform.AFFINE,(1/zoom,0,536*(1-1/zoom),0,1/zoom,360*(1-1/zoom)),Image.Resampling.BICUBIC)
 im=BACKGROUND.copy();shadow=Image.new('RGBA',(W,H));sd=ImageDraw.Draw(shadow);sd.ellipse((352,580,747,625),fill=(47,27,55,75));shadow=shadow.filter(ImageFilter.GaussianBlur(11));im=Image.alpha_composite(im.convert('RGBA'),shadow);im=Image.alpha_composite(im,layer)
 d=ImageDraw.Draw(im)
 txt(d,(56,39),'MOTOR OTTO  /  CUATRO TIEMPOS',18,'#3c385b')
 tag(d,(57,76),title,28)
 # Circular animated detail view, matching the reference's circular inserts.
 if intro or recap:box=(398,420,689,600);part='Cigüeñal';anchor=(575,520)
 elif s==0:box=(396,147,532,284);anchor=(468,237)
 elif s==1:box=(416,228,653,370);anchor=(640,py-12)
 elif s==2:box=(490,145,587,278);anchor=(537,222)
 else:box=(558,146,695,283);anchor=(605,237)
 size=245;bw=box[2]-box[0];bh=box[3]-box[1];side=max(bw,bh);mx=(box[0]+box[2])/2;my=(box[1]+box[3])/2
 square=(int(mx-side/2),int(my-side/2),int(mx+side/2),int(my+side/2))
 crop=layer.crop(square).resize((size,size),Image.Resampling.LANCZOS)
 circlebg=Image.new('RGBA',(size,size),'#daf4df');circlebg=Image.alpha_composite(circlebg,crop)
 mask=Image.new('L',(size,size));ImageDraw.Draw(mask).ellipse((1,1,size-2,size-2),fill=255)
 im.paste(circlebg,(914,280),mask);d=ImageDraw.Draw(im)
 d.ellipse((913,279,1159,525),outline='#aaebbb',width=2)
 tag(d,(899,211),part,20)
 # Yellow leader line tracks selected component under the zoom.
 ax=536+(anchor[0]-536)*zoom;ay=360+(anchor[1]-360)*zoom
 d.line((ax,ay,ax+45,ay-40,858,ay-40,888,235),fill=YELLOW,width=2);d.ellipse((ax-3,ay-3,ax+3,ay+3),fill=YELLOW)
 if intro:
  tag(d,(94,344),'Pistón',20);d.line((188,360,265,360,427,py+25),fill=YELLOW,width=2)
 if recap:txt(d,(861,558),'4 tiempos · 2 vueltas',20)
 # Bottom rhythm markers.
 for k in range(4):
  x=58+k*300;active=not intro and not recap and k==s
  if active:tag(d,(x,654),['Admisión','Compresión','Expansión','Escape'][k],20)
  else:txt(d,(x+10,658),['Admisión','Compresión','Expansión','Escape'][k],20,'#315b68')
 if t>D-.45:im=Image.blend(im.convert('RGB'),BACKGROUND,(t-(D-.45))/.45)
 p.stdin.write(im.convert('RGB').tobytes())
 if n in [24,180,275,386,505]:im.convert('RGB').save(P/f'estilo-frame-{n}.jpg',quality=94)
p.stdin.close();assert p.wait()==0
# Reuse the validated narrated mix without re-encoding its audio.
subprocess.run(['ffmpeg','-y','-loglevel','error','-i',str(P/'estilo-silent.mp4'),'-i',str(P/'motor-otto-narrado.mp4'),'-map','0:v:0','-map','1:a:0','-c','copy','-t',str(D),'-movflags','+faststart',str(P/'motor-otto-estilo.mp4')],check=True)
print('Rendered motor-otto-estilo.mp4')
