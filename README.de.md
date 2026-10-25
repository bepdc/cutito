Languages: [English](README.md) | [Italiano](README.it.md) | [Español](README.es.md) | [Français](README.fr.md) | Deutsch

CUTITO - YouTube-Video herunterladen, zuschneiden und in MP4 umwandeln
======================================================================

INSTALLATION (nur einmal)
-------------------------
1. Python 3.9 oder neuer: https://www.python.org/downloads/
   Im Installer "Add python.exe to PATH" anhaken.
2. ffmpeg: PowerShell oder Eingabeaufforderung öffnen und ausführen
       winget install Gyan.FFmpeg
   Danach das Terminal SCHLIESSEN und neu öffnen (sonst findet es ffmpeg nicht).
3. Das ganze Zip in einen beliebigen Ordner entpacken (z. B. Dokumente\Cutito).

BENUTZUNG
---------
1. Doppelklick auf start.bat (beim ersten Mal werden Abhängigkeiten geladen, ca. eine Minute).
2. Das Cutito-Fenster öffnet sich.
3. Link einfügen, Start/Ende eintragen (z. B. 1:30 und 3:30), 720p wählen und auf
   "Herunterladen und konvertieren" klicken.
4. Danach auf "MP4 herunterladen" oder "Ausgabeordner öffnen" klicken.
   Die Dateien bleiben im Ordner "output" neben app.py.

SPRACHE
-------
Oben rechts ist das Sprachmenü (Italiano, English, Español, Français, Deutsch).
Zu Beginn wird die Systemsprache verwendet; die Auswahl wird gespeichert.

STANDARDEINSTELLUNGEN (für die Analyse von Tritten gedacht)
-----------------------------------------------------------
- MP4, H.264-Codec, maximale Auflösung 720p
- Ton entfernt (Kästchen anhaken, um ihn zu behalten)
- Originale Bildrate bleibt erhalten: ein 50/60-fps-Video bleibt bei 50/60

EIGENES FENSTER
---------------
Cutito öffnet sich in einem eigenen Fenster (ohne Adressleiste und Tabs) über Edge
oder Chrome im "App-Modus". Wenn du das Fenster schließt, beendet sich die App. Die
interne Adresse ist cutito.localhost:5000 (*.localhost zeigt immer auf deinen PC, keine
Administratorrechte nötig).
Werden weder Edge noch Chrome gefunden, öffnet sie den Standardbrowser in einem normalen Tab.
Um einen anderen Chromium-Browser zu erzwingen, setze CUTITO_BROWSER auf den Pfad seiner exe.

OHNE SCHWARZES FENSTER
----------------------
Egal wie gestartet: Die App beendet sich von selbst, wenn du das Fenster schließt. Lädt
oder konvertiert sie noch, beendet sie die Arbeit (die Datei bleibt in output) und
schließt sich dann. Öffnest du sie erneut, während sie noch läuft, öffnet sich nur das
Fenster der laufenden Instanz erneut.

Option A - Cutito.exe (eine einzige Datei)
  1. Doppelklick auf build_exe.bat (einmalig; dauert ein bis zwei Minuten).
  2. Du erhältst Cutito.exe im Ordner: Doppelklick, und es startet ohne Fenster.
  3. Die Videos landen in Videos\Cutito. Falls du früher Clipper benutzt hast, liegen
     die alten Videos noch in Videos\Clipper. Schließe das alte Clipper.exe: Es nutzt
     denselben Port (5000).
  4. Die exe hat das Kätzchen-Symbol (cutito.ico muss neben build_exe.bat bleiben).
     Zeigt Windows noch das alte Symbol, ist es der Explorer-Cache: Explorer neu
     starten oder die exe in einen anderen Ordner verschieben.
  5. ffmpeg wird trotzdem benötigt: winget install Gyan.FFmpeg, oder ffmpeg.exe und
     ffprobe.exe neben Cutito.exe legen.
  In der exe steckt eine "eingefrorene" Kopie von yt-dlp. Wenn YouTube sie kaputt macht:
  build_exe.bat erneut ausführen (aktualisiert und baut neu) oder yt-dlp.exe neben
  Cutito.exe legen (github.com/yt-dlp/yt-dlp/releases): Falls vorhanden, nutzt die App diese.
  PyInstaller-exe lösen manchmal Fehlalarme beim Virenscanner aus: Das ist ein bekannter
  Fehlalarm dieser Methode.

Option B - ohne exe zu erstellen: start_silent.vbs
  Doppelklick: startet ohne schwarzes Fenster (vorher mindestens einmal start.bat ausführen).

Startet etwas nicht und du siehst keinen Fehler, schau ins Protokoll:
  %TEMP%\Cutito\cutito.log

WIE ERKENNE ICH, OB ES VORANGEHT
--------------------------------
- Unter dem Balken siehst du die vergangene Zeit, die MB auf der Platte und die letzte
  Zeile von yt-dlp/ffmpeg. Wachsen die MB, wird heruntergeladen.
- Mit Start/Ende ist der Balken beim Download "animiert": das ist normal. Der echte
  Prozentwert erscheint bei der Konvertierung.
- ETA = geschätzte Restzeit, nur eine Schätzung. Beim "normalen" Download sind Video und
  Ton zwei getrennte Dateien: % und ETA beginnen bei der zweiten Spur wieder bei 0.
- Ändert sich 45 Sekunden lang nichts, erscheint eine orangefarbene Warnung.

HÄUFIGE PROBLEME
----------------
- "yt-dlp ist fehlgeschlagen": YouTube ändert sich oft. start.bat erneut ausführen (aktualisiert yt-dlp).
- "Sign in to confirm you're not a bot" oder 403-Fehler: später oder anders erneut versuchen.
- Das Programm funktioniert nur auf deinem eigenen PC (127.0.0.1).

HINWEISE
--------
Nur für eigene Videos oder solche verwenden, die du herunterladen darfst. Das Herunterladen
fremder Inhalte ohne Erlaubnis verstößt gegen die Nutzungsbedingungen von YouTube.
