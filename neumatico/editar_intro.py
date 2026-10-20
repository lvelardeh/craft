"""Sustituye los primeros siete segundos visuales; conserva el audio y resto del montaje.
Uso: python neumatico/editar_intro.py /ruta/al/original.mp4
Requiere Pillow, NumPy y FFmpeg.
"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageFilter
import numpy as np,subprocess,sys
P=Path(__file__).parent
src=Path(sys.argv[1]);W,H=1920,1080
subprocess.run(['ffmpeg','-y','-v','error','-ss','8','-i',str(src),'-frames:v','1',str(P/'referencia.png')],check=True)
# Isolate the original wheel silhouette, filling interior holes in the mask.
r=Image.open(P/'referencia.png').convert('RGB').crop((648,305,1242,916));a=np.asarray(r).astype(float)
m=Image.fromarray(np.uint8((a[:,:,1]<a[:,:,0]*.92)&(a[:,:,2]>a[:,:,1]*1.15))*255)
f=m.copy();ImageDraw.floodfill(f,(0,0),128,thresh=0);mask=Image.fromarray(np.where(np.array(f)==128,0,255).astype('uint8')).filter(ImageFilter.GaussianBlur(.5))
r.putalpha(mask);r=r.resize((624,642),Image.Resampling.LANCZOS)
y,x=np.mgrid[0:H,0:W];q=(x/W*.7+y/H*.3)[:,:,None];left=np.array([27,19,73]);right=np.array([11,132,156]);bg=left*(1-q)+right*q
light=np.exp(-(((x-1510)/650)**2+((y-750)/650)**2)*2);bg+=light[:,:,None]*np.array([10,44,27])
im=Image.fromarray(np.uint8(np.clip(bg,0,255))).convert('RGBA');d=ImageDraw.Draw(im)
for rad in [330,410,490]:d.ellipse((1480-rad,545-rad,1480+rad,545+rad),outline=(62,142,166,255),width=1)
shadow=Image.new('RGBA',(W,H));ImageDraw.Draw(shadow).ellipse((1195,855,1780,925),fill=(9,10,37,130));im=Image.alpha_composite(im,shadow.filter(ImageFilter.GaussianBlur(18)));im.alpha_composite(r,(1170,225));d=ImageDraw.Draw(im)
f='/usr/share/fonts/truetype/dejavu/DejaVuSans'
d.rounded_rectangle((150,327,239,334),3,fill='#ebf23c')
d.text((145,371),'PARTES DEL',font=ImageFont.truetype(f+'.ttf',65),fill='#b5e4ef')
d.text((140,446),'neumático',font=ImageFont.truetype(f+'-Bold.ttf',137),fill='#ffffff')
d.text((150,640),'Conoce su estructura',font=ImageFont.truetype(f+'.ttf',34),fill='#c0d9e9')
im.convert('RGB').save(P/'intro-moderna.png')
# Title visible from frame zero. Subtle push-in, then dissolve into the original.
subprocess.run(['ffmpeg','-y','-v','error','-i',str(src),'-loop','1','-framerate','30000/1001','-i',str(P/'intro-moderna.png'),'-filter_complex',"[1:v]zoompan=z='min(1+on*0.000045,1.01)':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s=1920x1080:fps=30000/1001,format=yuva420p,fade=t=out:st=6.2:d=0.8:alpha=1[cover];[0:v][cover]overlay=shortest=1:enable='lt(t,7)'[v]",'-map','[v]','-map','0:a:0','-c:v','libx264','-preset','veryfast','-threads','2','-crf','19','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(P/'partes-neumatico-intro-moderna.mp4')],check=True)
print('Exportación terminada')
