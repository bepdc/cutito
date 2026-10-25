# Cutito

![Cutito logo](cutito.png)

**Language:** English | [Italiano](README.it.md) | [Español](README.es.md) | [Français](README.fr.md) | [Deutsch](README.de.md)

Cutito is a small Windows app that downloads a YouTube video, trims the part you
want, and converts it to MP4 (H.264). It opens in a dedicated browser window and
runs locally on your computer.

## Features

- Download a full video or a selected section by setting start and end times.
- Choose a maximum resolution (480p, 720p, or 1080p) and output quality.
- Remove audio by default, or choose to keep it.
- See download and conversion progress.
- Use the interface in Italian, English, Spanish, French, or German.

## Requirements

- Windows (the launch and build scripts are for Windows).
- Python 3.9 or newer. Select **Add python.exe to PATH** during installation.
- [ffmpeg](https://ffmpeg.org/) available on your `PATH`. To install it with
  WinGet, run this command in PowerShell:

  ```powershell
  winget install Gyan.FFmpeg
  ```

  After installation, close and reopen the terminal.

## Run Cutito

1. Download or extract the project to a folder.
2. Double-click `start.bat`.

On the first run, the script creates a Python environment and installs the
dependencies. It also updates `yt-dlp` every time it starts. Cutito opens in a
dedicated Edge or Chrome window; if neither browser is found, it opens in a
regular tab in your default browser.

Paste a video link, optionally set start and end times, choose your options, and
click **Download and convert**. When the job is complete, download the MP4 or
open the output folder.

Files are saved in the `output` folder next to `app.py`. To run Cutito without a
terminal window, run `start.bat` at least once, then double-click
`start_silent.vbs`.

## Build the executable

To create a single `Cutito.exe`, double-click `build_exe.bat`. The script creates
the Python environment, installs PyInstaller, and builds the executable in the
project folder. `ffmpeg` is still required. Videos are saved to
`Videos\Cutito` in your user folder.

## Troubleshooting

- **ffmpeg not found:** install it and reopen the terminal, or place `ffmpeg.exe`
  and `ffprobe.exe` next to `Cutito.exe`.
- **yt-dlp or YouTube error:** check your connection and try again later.
  `start.bat` updates `yt-dlp` each time it starts.
- **The app does not start and shows no error:** check the log at
  `%TEMP%\Cutito\cutito.log`.
- **Port 5000 is already in use:** close the other application using that port
  and restart Cutito.

## Responsible use

Only use Cutito with videos you own or have permission to download. You are
responsible for complying with applicable copyright law and service terms.
