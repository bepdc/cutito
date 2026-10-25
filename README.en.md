Languages: [English](README.md) | [Italiano](README.it.md) | [Español](README.es.md) | [Français](README.fr.md) | [Deutsch](README.de.md)

CUTITO - download a YouTube video, cut it and convert it to MP4
================================================================

INSTALLATION (one time only)
----------------------------
1. Python 3.9 or newer: https://www.python.org/downloads/
   In the installer tick "Add python.exe to PATH".
2. ffmpeg: open PowerShell or Command Prompt and run
       winget install Gyan.FFmpeg
   Then CLOSE and reopen the terminal (otherwise it won't see ffmpeg).
3. Extract the whole zip into any folder (e.g. Documents\Cutito).

USAGE
-----
1. Double-click start.bat (the first time it downloads dependencies, about a minute).
2. The Cutito window opens.
3. Paste the link, set start/end (e.g. 1:30 and 3:30), choose 720p, click
   "Download and convert".
4. When it's done click "Download MP4" or "Open output folder".
   Files stay in the "output" folder next to app.py.

LANGUAGE
--------
The language menu is at the top right (Italiano, English, Espanol, Francais,
Deutsch). It starts in your system language; your choice is remembered.

DEFAULT SETTINGS (made for analysing kicks)
-------------------------------------------
- MP4, H.264 codec, maximum resolution 720p
- Audio removed (tick the box to keep it)
- Original frame rate kept: a 50/60 fps video stays 50/60 fps

DEDICATED WINDOW
----------------
Cutito opens in its own window (no address bar, no tabs), using Edge or Chrome in
"app mode". When you close the window the app shuts down. The internal address is
cutito.localhost:5000 (*.localhost always points to your own PC, no admin rights needed).
If neither Edge nor Chrome is found, it opens the default browser in a normal tab.
To force another Chromium browser set CUTITO_BROWSER to the path of its exe.

NO BLACK WINDOW
---------------
However you start it, the app shuts down by itself when you close the window. If it
is still downloading or converting, it finishes the job (the file stays in output)
and then closes. If you reopen it while it is still running, it just reopens the
window on the running instance.

Option A - Cutito.exe (a single file)
  1. Double-click build_exe.bat (once; takes one or two minutes).
  2. You get Cutito.exe in the folder: double-click and it starts, no windows.
  3. Videos go to Videos\Cutito. If you used Clipper before, the old videos are
     still in Videos\Clipper. Close the old Clipper.exe: it uses the same port (5000).
  4. The exe has the kitten icon (cutito.ico must stay next to build_exe.bat).
     If Windows still shows the old icon it's the Explorer cache: restart Explorer
     or move the exe to another folder.
  5. ffmpeg is still required: winget install Gyan.FFmpeg, or put ffmpeg.exe and
     ffprobe.exe next to Cutito.exe.
  The exe contains a "frozen" copy of yt-dlp. When YouTube breaks it: rerun
  build_exe.bat (updates and rebuilds) or put yt-dlp.exe next to Cutito.exe
  (github.com/yt-dlp/yt-dlp/releases): if present, the app uses that one.
  PyInstaller exes sometimes trigger antivirus false alarms: it's a known false
  positive of the method.

Option B - without building the exe: start_silent.vbs
  Double-click: starts without a black window (run start.bat at least once first).

If something doesn't start and you see no error, check the log:
  %TEMP%\Cutito\cutito.log

HOW TO TELL IF IT IS MAKING PROGRESS
------------------------------------
- Under the bar you see elapsed time, MB on disk and the last yt-dlp/ffmpeg line.
  If the MB grow, it is downloading.
- With start/end the bar is "animated" during download: that's normal. The real
  percentage appears during conversion.
- ETA = estimated time left, only an estimate. In a "normal" download video and audio
  are two separate files: % and ETA restart from 0 on the second track.
- If nothing changes for 45 seconds an orange warning appears.

COMMON PROBLEMS
---------------
- "yt-dlp failed": YouTube changes often. Rerun start.bat (it updates yt-dlp).
- "Sign in to confirm you're not a bot" or 403 errors: try again later or use
  another method.
- The program only works on your own PC (127.0.0.1).

NOTES
-----
Use it only for videos that are yours or that you have permission to download.
Downloading other people's content without permission violates YouTube's terms.
