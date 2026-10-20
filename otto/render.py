from PIL import Image, ImageDraw, ImageFont
import numpy as np, math, subprocess, wave
from pathlib import Path
P=Path(__file__).parent
W,H,FPS,D=1280,720,24,28
font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
bold=font.replace('.ttf','-Bold.ttf')
def txt(d,xy,s,size=24,fill='#eaf1fb',b=False):d.text(xy,s,font=ImageFont.truetype(bold if b else font,size),fill=fill)
def arrow(d,x,y,dy,c):
 d.line((x,y,x,y+dy),fill=c,width=7); end=y+dy; sign=1 if dy>0 else -1
 d.polygon([(x,end),(x-10,end-sign*16),(x+10,end-sign*16)],fill=c)
stages=[('ADMISIÓN','Entra aire + combustible.','El pistón baja. La válvula de admisión abre.','#4dd8ff'),('COMPRESIÓN','La mezcla se comprime.','El pistón sube. Ambas válvulas se cierran.','#b49bff'),('COMBUSTIÓN / EXPANSIÓN','La chispa inicia la combustión.','Los gases se expanden y empujan el pistón.','#ffb454'),('ESCAPE','Salen los gases quemados.','El pistón sube. La válvula de escape abre.','#ff7e96')]
proc=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-an','-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p',str(P/'silent.mp4')],stdin=subprocess.PIPE)
for frame in range(D*FPS):
 t=frame/FPS
 im=Image.new('RGB',(W,H),'#0b1220');d=ImageDraw.Draw(im)
 txt(d,(64,34),'MOTOR OTTO',22,fill='#76d9ed',b=True);txt(d,(64,67),'Cuatro tiempos. Un ciclo.',40,b=True)
 # 2 sec intro, 4 x 5.5 sec, 4 sec recap
 elapsed=max(0,min(t-2,21.999));s=int(elapsed/5.5);u=(elapsed%5.5)/5.5
 if t>=24: s=int((t-24)*1)%4;u=((t-24)*1)%1
 title,desc,sub,c=stages[s]
 txt(d,(65,195),f'0{s+1}',65,fill=c,b=True);txt(d,(65,280),title,27,fill=c,b=True)
 # wrap description
 import textwrap
 for j,line in enumerate(textwrap.wrap(desc,32)):txt(d,(65,337+j*36),line,28,b=True)
 for j,line in enumerate(textwrap.wrap(sub,44)):txt(d,(65,430+j*30),line,22,fill='#aebdd3')
 if t<2:
  txt(d,(65,548),'Así convierte combustible',22);txt(d,(65,580),'en movimiento.',22)
 elif t>=24:txt(d,(65,555),'4 tiempos = 2 vueltas del cigüeñal',22,fill='#76d9ed',b=True)
 # cylinder with piston kinematics (schematic)
 x0,x1,top=795,1055,232
 a=(s+u)*math.pi
 y=346+79*(-math.cos(a))
 d.rounded_rectangle((750,171,1100,590),20,fill='#172338')
 gas={'0':'#194054','1':'#3e3158','2':'#754b24','3':'#513441'}[str(s)]
 d.rectangle((x0,top,x1,y),fill=gas)
 d.line((x0,top,x0,532),fill='#8da4bf',width=10);d.line((x1,top,x1,532),fill='#8da4bf',width=10)
 d.rectangle((x0-5,212,x1+5,232),fill='#8da4bf')
 # intake/exhaust ports and valves
 for vx,opened,color in [(840,s==0,'#4dd8ff'),(1010,s==3,'#ff7e96')]:
  d.rectangle((vx-14,209,vx+14,237),fill='#0b1220');offset=15 if opened else 0
  d.line((vx,176,vx,229+offset),fill=color,width=6);d.line((vx-23,229+offset,vx+23,229+offset),fill=color,width=6)
 txt(d,(764,143),'ENTRADA',14,fill='#4dd8ff',b=True);txt(d,(1000,143),'SALIDA',14,fill='#ff7e96',b=True)
 # spark plug and spark
 d.rectangle((920,190,930,239),fill='#eaf1fb')
 if s==2 and u<.24:
  pts=[(925+math.cos(k*math.pi/6)*(38 if k%2==0 else 12),250+math.sin(k*math.pi/6)*(38 if k%2==0 else 12)) for k in range(12)]
  d.polygon(pts,fill='#ffe887')
 # crank/rod
 cx,cy=925,550; pin=(cx+40*math.sin(a),cy-40*math.cos(a))
 d.ellipse((cx-49,cy-49,cx+49,cy+49),outline='#58708f',width=5)
 d.line((cx,cy,*pin),fill=c,width=12);d.line((*pin,925,y+25),fill='#acbcd0',width=15)
 d.rounded_rectangle((800,y,1050,y+48),7,fill='#b8cadf');d.line((803,y+12,1047,y+12),fill='#5d728f',width=4)
 d.ellipse((917,y+17,933,y+33),fill='#4d6381')
 if s==0:
  for k in range(6):
   yy=245+((u*170+k*23)%max(25,y-246));d.ellipse((835,yy,841,yy+6),fill=c)
 if s==3: arrow(d,1010,181,-44,c)
 if s==0: arrow(d,840,151,48,c)
 arrow(d,1140,350,65 if s in [0,2] else -65,c)
 txt(d,(818,614),'CORTE ESQUEMÁTICO',16,fill='#8da4bf')
 for k in range(4):
  xx=64+k*292;d.rounded_rectangle((xx,667,xx+270,674),3,fill=stages[k][3] if k==s else '#26354c');txt(d,(xx,686),['01 Admisión','02 Compresión','03 Expansión','04 Escape'][k],14,fill=stages[k][3] if k==s else '#8da4bf')
 proc.stdin.write(im.tobytes())
 if frame in [24,210,350,480]: im.save(P/f'frame-{frame}.png')
proc.stdin.close(); assert proc.wait()==0
# Original subtle sound design: soft mechanical pulses, air and ignition.
sr=48000;rng=np.random.default_rng(9);audio=np.zeros(D*sr,dtype=np.float32)
def add(at,v):
 st=int(at*sr);n=min(len(v),len(audio)-st)
 if n>0:audio[st:st+n]+=v[:n]
for st in [2,7.5,13,18.5,24,25,26,27]:
 q=np.arange(int(.18*sr))/sr;add(st,.12*np.sin(2*np.pi*110*q)*np.exp(-q*30))
for at in [2.2,19]:
 q=np.arange(sr)/sr;add(at,.025*rng.normal(size=sr)*np.sin(np.pi*q)**2)
q=np.arange(int(.45*sr))/sr;add(13.1,.15*rng.normal(size=len(q))*np.exp(-q*18)+.15*np.sin(2*np.pi*65*q)*np.exp(-q*12))
with wave.open(str(P/'effects.wav'),'wb') as f:f.setnchannels(1);f.setsampwidth(2);f.setframerate(sr);f.writeframes((np.clip(audio,-1,1)*32767).astype('<i2').tobytes())
print('Render complete')
