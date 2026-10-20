"""Render sincronizado con narracion.mp3 (24.03 s). Requiere Pillow, NumPy y FFmpeg."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import subprocess,math,wave
import numpy as np
P=Path(__file__).parent
W,H,FPS,D=1280,720,24,25.5
F='/usr/share/fonts/truetype/dejavu/DejaVuSans'
def text(d,pos,s,size=24,c='#e8f0fa',bold=False):d.text(pos,s,font=ImageFont.truetype(F+('-Bold' if bold else '')+'.ttf',size),fill=c)
# Name onset, piston movement onset/end; pauses preserve the natural narration.
scenes=[(5.09,6.26,8.78,'ADMISIÓN','#4dd8ff'),(9.31,10.45,12.51,'COMPRESIÓN','#b49bff'),(13.07,16.05,18.41,'EXPANSIÓN','#ffb454'),(19.01,20.02,22.30,'ESCAPE','#ff7e96')]
p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-an','-c:v','libx264','-preset','fast','-crf','19','-pix_fmt','yuv420p',str(P/'narrado-silent.mp4')],stdin=subprocess.PIPE)
for n in range(int(D*FPS)):
 t=n/FPS; intro=t<5.09; recap=t>=22.73
 s=max([i for i,z in enumerate(scenes) if t>=z[0]],default=0)
 start,motion,end,label,c=scenes[s];u=max(0,min(1,(t-motion)/(end-motion)))
 if intro: a=0;u=0
 elif recap:a=4*math.pi+(t-22.73)*math.pi*1.4
 else:a=(s+u)*math.pi
 y=300+75*(-math.cos(a));im=Image.new('RGB',(W,H),'#0b1220');d=ImageDraw.Draw(im)
 text(d,(60,30),'MOTOR OTTO',24,'#76d9ed',True)
 text(d,(60,72),'Cuatro tiempos. Un ciclo.' if intro or recap else f'0{s+1}  '+('COMBUSTIÓN Y EXPANSIÓN' if s==2 else label),34,'#e8f0fa' if intro or recap else c,True)
 # Spacious central cutaway, driven by the same crank angle as the piston.
 x0,x1,cx=520,780,650;cy=510
 d.rounded_rectangle((470,160,830,578),24,fill='#172338')
 gas=['#194054','#3e3158','#754b24','#513441'][s]
 d.rectangle((x0,210,x1,y),fill=gas if not intro else '#20364a')
 d.line((x0,210,x0,475),fill='#8da4bf',width=10);d.line((x1,210,x1,475),fill='#8da4bf',width=10)
 d.rectangle((515,190,785,210),fill='#8da4bf')
 for vx,opened,color in [(565,s==0 and not intro and not recap and t>=motion,'#4dd8ff'),(735,s==3 and not recap,'#ff7e96')]:
  off=15 if opened else 0;d.rectangle((vx-14,187,vx+14,216),fill='#0b1220');d.line((vx,154,vx,207+off),fill=color,width=6);d.line((vx-22,207+off,vx+22,207+off),fill=color,width=6)
 d.rectangle((645,168,655,220),fill='#eaf1fb')
 spark=s==2 and 15.75<=t<=16.15 and not recap
 if spark:
  pts=[(650+math.cos(k*math.pi/6)*(40 if k%2==0 else 12),231+math.sin(k*math.pi/6)*(40 if k%2==0 else 12)) for k in range(12)];d.polygon(pts,fill='#ffe887')
 pin=(cx+40*math.sin(a),cy-40*math.cos(a))
 d.ellipse((cx-49,cy-49,cx+49,cy+49),outline='#58708f',width=5)
 d.line((cx,cy,*pin),fill=c if not intro else '#76d9ed',width=12);d.line((*pin,cx,y+25),fill='#acbcd0',width=15)
 d.rounded_rectangle((525,y,775,y+48),7,fill='#b8cadf');d.line((528,y+12,772,y+12),fill='#5d728f',width=4);d.ellipse((642,y+17,658,y+33),fill='#4d6381')
 if not intro and not recap and s in [0,3] and t>=motion and t<=end:
  vx=565 if s==0 else 735;sign=1 if s==0 else -1;yy=120 if s==0 else 165;ey=yy+sign*42
  d.line((vx,yy,vx,ey),fill=c,width=6);d.polygon([(vx,ey),(vx-9,ey-sign*14),(vx+9,ey-sign*14)],fill=c)
  if s==0:
   for k in range(12):
    yy=229+((t*65+k*19)%max(15,y-235));xx=545+(k%4)*55;d.ellipse((xx,yy,xx+5,yy+5),fill=c)
 if not intro and not recap:
  d.line((880,315,880,315+(45 if s in [0,2] else -45)),fill=c,width=6)
  ey=315+(45 if s in [0,2] else -45);sg=1 if s in [0,2] else -1;d.polygon([(880,ey),(870,ey-sg*14),(890,ey-sg*14)],fill=c)
  if s==2 and t<16.15:text(d,(895,208),'CHISPA' if spark else 'BUJÍA',17,c,True)
 if intro:
  for pos,name,line in [((900,295),'PISTÓN',(892,326,782,326)),((900,497),'CIGÜEÑAL',(892,527,705,527)),((295,153),'VÁLVULAS',(395,183,540,183))]:
   text(d,pos,name,18,'#9fb2ca');d.line(line,fill='#526883',width=2)
 if recap:text(d,(432,602),'El ciclo se repite.',27,'#76d9ed',True)
 else:text(d,(527,602),'CORTE ESQUEMÁTICO',17,'#8da4bf')
 for k in range(4):
  x=60+k*295;active=(k==s and not intro and not recap);cc=scenes[k][4] if active else '#63758e'
  d.rounded_rectangle((x,660,x+275,666),3,fill=cc)
  text(d,(x,680),['01  Admisión','02  Compresión','03  Expansión','04  Escape'][k],18,cc,active)
 if t>D-.5:
  im=Image.blend(im,Image.new('RGB',(W,H),'#0b1220'),(t-(D-.5))/.5)
 p.stdin.write(im.tobytes())
 if n in [24,180,275,386,505]:im.save(P/f'narrado-frame-{n}.png')
p.stdin.close();assert p.wait()==0
sr=48000;aud=np.zeros(int(D*sr));rng=np.random.default_rng(42)
def add(at,v):
 st=int(at*sr);aud[st:st+len(v)]+=v
for at in [6.26,10.45,16.05,20.02]:
 q=np.arange(int(.15*sr))/sr;add(at,.045*np.sin(2*np.pi*95*q)*np.exp(-q*27))
for at in [6.3,20.05]:
 q=np.arange(int(.7*sr))/sr;add(at,.012*rng.normal(size=len(q))*np.sin(np.pi*q/.7)**2)
q=np.arange(int(.35*sr))/sr;add(15.8,.045*rng.normal(size=len(q))*np.exp(-q*22)+.06*np.sin(2*np.pi*65*q)*np.exp(-q*16))
with wave.open(str(P/'narrado-effects.wav'),'wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes((aud*32767).astype('<i2').tobytes())
subprocess.run(['ffmpeg','-y','-loglevel','error','-i',str(P/'narrado-silent.mp4'),'-i',str(P/'narracion.mp3'),'-i',str(P/'narrado-effects.wav'),'-filter_complex','[1:a]loudnorm=I=-16:TP=-1.5:LRA=9,apad[v];[v][2:a]amix=inputs=2:duration=longest:normalize=0,alimiter=limit=0.95[a]','-map','0:v','-map','[a]','-c:v','copy','-c:a','aac','-b:a','192k','-t',str(D),'-movflags','+faststart',str(P/'motor-otto-narrado.mp4')],check=True)
print('Narrated render complete:',D,'seconds')
