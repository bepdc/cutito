Languages: English (README.en.txt) | Italiano (README.it.txt) | Español (README.es.txt) | Français (README.fr.txt) | Deutsch (README.de.txt)

CUTITO - scarica un video YouTube, taglialo e convertilo in MP4
================================================================

INSTALLAZIONE (una volta sola)
------------------------------
1. Python 3.9 o superiore: https://www.python.org/downloads/
   Nell'installer spunta "Add python.exe to PATH".
2. ffmpeg: apri PowerShell o Prompt dei comandi e lancia
       winget install Gyan.FFmpeg
   Poi CHIUDI e riapri il terminale (altrimenti non vede ffmpeg).
3. Estrai tutto lo zip in una cartella qualsiasi (es. Documenti\Cutito).

USO
---
1. Doppio clic su start.bat (la prima volta scarica le dipendenze, ci mette un minuto).
2. Si apre la finestra di Cutito.
3. Incolla il link, metti inizio/fine (es. 1:30 e 3:30), scegli 720p, clic su
   "Scarica e converti".
4. A fine lavoro clicchi "Scarica MP4" oppure "Apri cartella output".
   I file restano nella cartella "output" accanto ad app.py.

LINGUA
------
In alto a destra c'e' il menu della lingua (Italiano, English, Espanol, Francais,
Deutsch). All'inizio usa la lingua del sistema; la scelta viene ricordata.

IMPOSTAZIONI DI DEFAULT (pensate per l'analisi dei calci)
---------------------------------------------------------
- MP4, codec H.264, risoluzione massima 720p
- Audio rimosso (spunta la casella se lo vuoi)
- Frame rate originale mantenuto: se il video e' a 50/60 fps resta a 50/60

FINESTRA DEDICATA
-----------------
Cutito si apre come una finestra tutta sua (senza barra degli indirizzi e senza
schede), usando Edge o Chrome in "modalita' app". Quando chiudi la finestra, l'app
si spegne. L'indirizzo interno e' cutito.localhost:5000 (*.localhost punta sempre
al tuo PC, nessun permesso di amministratore).
Se non trova ne' Edge ne' Chrome, apre il browser predefinito in una normale scheda.
Per forzare un altro browser Chromium imposta CUTITO_BROWSER con il percorso dell'exe.

SENZA FINESTRA NERA
-------------------
In tutti i modi di avvio l'app si spegne da sola quando chiudi la finestra. Se sta
ancora scaricando o convertendo, finisce il lavoro (il file resta in output) e poi
si chiude. Se la riapri mentre e' ancora in esecuzione, riapre la finestra sull'istanza attiva.

Opzione A - Cutito.exe (un solo file)
  1. Doppio clic su build_exe.bat (una volta; ci mette uno o due minuti).
  2. Ti ritrovi Cutito.exe nella cartella: doppio clic e parte, senza finestre.
  3. I video vanno in Video\Cutito. Se prima usavi Clipper, i vecchi video sono
     rimasti in Video\Clipper. Chiudi il vecchio Clipper.exe: usa la stessa porta (5000).
  4. L'exe ha l'icona del gattino (cutito.ico deve restare accanto a build_exe.bat).
     Se Windows mostra ancora l'icona vecchia e' la cache di Esplora risorse:
     riavvialo o sposta l'exe in un'altra cartella.
  5. ffmpeg serve comunque: winget install Gyan.FFmpeg, oppure metti ffmpeg.exe e
     ffprobe.exe accanto a Cutito.exe.
  Dentro l'exe c'e' una copia "congelata" di yt-dlp. Quando YouTube la rompe: rilancia
  build_exe.bat (aggiorna e ricostruisce) oppure metti yt-dlp.exe accanto a Cutito.exe
  (github.com/yt-dlp/yt-dlp/releases): se c'e', l'app usa quello.
  Gli exe PyInstaller a volte fanno scattare falsi allarmi dell'antivirus: e' un
  falso positivo noto del metodo.

Opzione B - senza creare l'exe: start_silent.vbs
  Doppio clic: parte senza finestra nera (lancia start.bat almeno una volta prima).

Se qualcosa non parte e non vedi errori, guarda il log:
  %TEMP%\Cutito\cutito.log

COME CAPIRE SE STA ANDANDO AVANTI
---------------------------------
- Sotto la barra vedi tempo trascorso, MB su disco e l'ultima riga di yt-dlp/ffmpeg.
  Se i MB crescono, sta scaricando.
- Con inizio/fine la barra e' "animata" durante il download: e' normale. La
  percentuale vera compare nella conversione.
- ETA = tempo stimato rimanente, solo una stima. Nel download "normale" video e audio
  sono due file separati: % ed ETA ripartono da 0 alla seconda traccia.
- Se non cambia nulla per 45 secondi compare un avviso arancione.

PROBLEMI COMUNI
---------------
- "yt-dlp ha fallito": YouTube cambia spesso. Rilancia start.bat (aggiorna yt-dlp).
- "Sign in to confirm you're not a bot" o errori 403: riprova piu' tardi o con un
  altro metodo.
- Il programma funziona solo sul tuo PC (127.0.0.1).

NOTE
----
Usalo solo per video tuoi o che hai il permesso di scaricare. Scaricare contenuti
altrui senza autorizzazione viola i termini di YouTube.
