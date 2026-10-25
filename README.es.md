Languages: [English](README.md) | [Italiano](README.it.md) | Español | [Français](README.fr.md) | [Deutsch](README.de.md)

CUTITO - descarga un vídeo de YouTube, córtalo y conviértelo a MP4
==================================================================

INSTALACIÓN (una sola vez)
--------------------------
1. Python 3.9 o superior: https://www.python.org/downloads/
   En el instalador marca "Add python.exe to PATH".
2. ffmpeg: abre PowerShell o el Símbolo del sistema y ejecuta
       winget install Gyan.FFmpeg
   Después CIERRA y vuelve a abrir el terminal (si no, no ve ffmpeg).
3. Extrae todo el zip en cualquier carpeta (p. ej. Documentos\Cutito).

USO
---
1. Doble clic en start.bat (la primera vez descarga las dependencias, tarda un minuto).
2. Se abre la ventana de Cutito.
3. Pega el enlace, pon inicio/fin (p. ej. 1:30 y 3:30), elige 720p y pulsa
   "Descargar y convertir".
4. Al terminar pulsa "Descargar MP4" o "Abrir carpeta de salida".
   Los archivos quedan en la carpeta "output" junto a app.py.

IDIOMA
------
Arriba a la derecha está el menú de idioma (Italiano, English, Español, Français,
Deutsch). Al principio usa el idioma del sistema; tu elección se recuerda.

AJUSTES POR DEFECTO (pensados para analizar patadas)
----------------------------------------------------
- MP4, códec H.264, resolución máxima 720p
- Audio eliminado (marca la casilla si lo quieres)
- Se mantiene la tasa de fotogramas original: un vídeo a 50/60 fps sigue a 50/60

VENTANA PROPIA
--------------
Cutito se abre en su propia ventana (sin barra de direcciones ni pestañas), usando
Edge o Chrome en "modo aplicación". Al cerrar la ventana, la aplicación se apaga. La
dirección interna es cutito.localhost:5000 (*.localhost apunta siempre a tu PC, sin
permisos de administrador).
Si no encuentra ni Edge ni Chrome, abre el navegador predeterminado en una pestaña normal.
Para forzar otro navegador Chromium define CUTITO_BROWSER con la ruta de su exe.

SIN VENTANA NEGRA
-----------------
Se inicie como se inicie, la aplicación se apaga sola al cerrar la ventana. Si aún
está descargando o convirtiendo, termina el trabajo (el archivo queda en output) y
luego se cierra. Si la abres de nuevo mientras sigue en marcha, solo reabre la
ventana sobre la instancia activa.

Opción A - Cutito.exe (un solo archivo)
  1. Doble clic en build_exe.bat (una vez; tarda uno o dos minutos).
  2. Obtienes Cutito.exe en la carpeta: doble clic y arranca, sin ventanas.
  3. Los vídeos van a Vídeos\Cutito. Si antes usabas Clipper, los vídeos antiguos
     siguen en Vídeos\Clipper. Cierra el antiguo Clipper.exe: usa el mismo puerto (5000).
  4. El exe tiene el icono del gatito (cutito.ico debe estar junto a build_exe.bat).
     Si Windows aún muestra el icono antiguo es la caché del Explorador: reinícialo
     o mueve el exe a otra carpeta.
  5. ffmpeg sigue siendo necesario: winget install Gyan.FFmpeg, o pon ffmpeg.exe y
     ffprobe.exe junto a Cutito.exe.
  Dentro del exe hay una copia "congelada" de yt-dlp. Cuando YouTube la rompe: vuelve
  a ejecutar build_exe.bat (actualiza y reconstruye) o pon yt-dlp.exe junto a Cutito.exe
  (github.com/yt-dlp/yt-dlp/releases): si está, la aplicación usa ese.
  Los exe de PyInstaller a veces disparan falsas alarmas del antivirus: es un falso
  positivo conocido del método.

Opción B - sin crear el exe: start_silent.vbs
  Doble clic: arranca sin ventana negra (ejecuta start.bat al menos una vez antes).

Si algo no arranca y no ves ningún error, mira el registro:
  %TEMP%\Cutito\cutito.log

CÓMO SABER SI AVANZA
--------------------
- Bajo la barra ves el tiempo transcurrido, los MB en disco y la última línea de
  yt-dlp/ffmpeg. Si los MB crecen, está descargando.
- Con inicio/fin la barra está "animada" durante la descarga: es normal. El
  porcentaje real aparece en la conversión.
- ETA = tiempo estimado restante, solo una estimación. En una descarga "normal" el
  vídeo y el audio son dos archivos: % y ETA vuelven a 0 en la segunda pista.
- Si nada cambia durante 45 segundos aparece un aviso naranja.

PROBLEMAS COMUNES
-----------------
- "yt-dlp ha fallado": YouTube cambia a menudo. Vuelve a ejecutar start.bat (actualiza yt-dlp).
- "Sign in to confirm you're not a bot" o errores 403: inténtalo más tarde o con otro método.
- El programa solo funciona en tu propio PC (127.0.0.1).

NOTAS
-----
Úsalo solo con vídeos tuyos o que tengas permiso para descargar. Descargar contenido
ajeno sin autorización incumple las condiciones de YouTube.
