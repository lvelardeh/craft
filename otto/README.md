# Motor Otto: cuatro tiempos

Muestra educativa de 28 segundos, 1280 × 720, 24 fps. Incluye animación esquemática, textos en español y efectos de sonido originales. No incluye narración.

- `motor-otto.mp4`: video con sonido.
- `motor-otto.gif`: vista previa sin sonido.
- `render.py`: generador de la animación y los efectos.

## Reproducir el render

Requiere Python 3, Pillow, NumPy, FFmpeg y las fuentes DejaVu Sans en `/usr/share/fonts/truetype/dejavu/`.

Desde la raíz del repositorio:

```sh
python -m pip install Pillow numpy
python otto/render.py
ffmpeg -y -i otto/silent.mp4 -i otto/effects.wav -c:v copy -c:a aac -b:a 160k -movflags +faststart -t 28 otto/motor-otto.mp4
ffmpeg -y -i otto/motor-otto.mp4 -vf 'fps=8,scale=640:-1,split[a][b];[a]palettegen[p];[b][p]paletteuse' otto/motor-otto.gif
```

El render genera también archivos intermedios y capturas locales. El dibujo es esquemático, no un modelo mecánico a escala.

## Versión narrada

`motor-otto-narrado.mp4` incorpora la narración de ElevenLabs aportada por el usuario, sin acelerar su voz. Dura 25,5 segundos e incluye un cierre breve. El motor ocupa el centro de la imagen y los párrafos se sustituyen por los nombres de los tiempos. Los efectos se mezclan a bajo volumen.

Para regenerarla, con las mismas dependencias:

```sh
python otto/render_narrado.py
```

El archivo de entrada es `otto/narracion.mp3`. Los tiempos de escena y movimiento están definidos en `render_narrado.py`; se adaptaron a las frases y pausas de esta grabación concreta. Otra narración requiere reajustarlos. El script genera el MP4 final, capturas y archivos intermedios.
