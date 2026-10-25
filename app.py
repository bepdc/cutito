import sys

# --- "Child" mode: inside the .exe, this same program acts as yt-dlp ---------
# (must stay at the top, before importing Flask and the rest)
if __name__ == "__main__" and len(sys.argv) > 1 and sys.argv[1] == "--run-yt-dlp":
    import yt_dlp
    yt_dlp.main(sys.argv[2:])
    sys.exit(0)

import logging
import os
import re
import shutil
import socket
import subprocess
import tempfile
import threading
import time
import traceback
import urllib.request
import uuid
import webbrowser
from pathlib import Path

from flask import Flask, Response, request, jsonify, send_file, abort

FROZEN = bool(getattr(sys, "frozen", False))  # True when running as an .exe
RES = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))  # index.html
BASE = Path(sys.executable).resolve().parent if FROZEN else Path(__file__).resolve().parent
WORK = Path(tempfile.gettempdir()) / "Cutito"  # log and temp files of the .exe


def _pick_out():
    if not FROZEN:
        return BASE / "output"
    for cand in (Path.home() / "Videos" / "Cutito", BASE / "output"):
        try:
            cand.mkdir(parents=True, exist_ok=True)
            return cand
        except OSError:
            continue
    return WORK / "output"


OUT = _pick_out()
TMP = (WORK / "tmp") if FROZEN else (BASE / "tmp")
OUT.mkdir(parents=True, exist_ok=True)
TMP.mkdir(parents=True, exist_ok=True)

PORT = 5000
TOKEN = uuid.uuid4().hex

# Auto-close: the app exits when no tab is open and no job is running.
GRACE = float(os.environ.get("CUTITO_GRACE", 6))            # seconds after the last tab is closed
STARTUP_GRACE = float(os.environ.get("CUTITO_STARTUP", 40))  # time allowed for the browser to open
PING_TIMEOUT = float(os.environ.get("CUTITO_PING_TIMEOUT", 150))  # browser dead/suspended

NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0)  # no black console windows on Windows
BUSY = ("queued", "download", "convert")


def setup_streams():
    """Without a console (windowed exe / pythonw) stdout and stderr are None: redirect them to a log."""
    if FROZEN or sys.stdout is None or sys.stderr is None:
        try:
            WORK.mkdir(parents=True, exist_ok=True)
            lf = WORK / "cutito.log"
            if lf.exists() and lf.stat().st_size > 2_000_000:
                lf.unlink()
            fh = open(lf, "a", encoding="utf-8", buffering=1)
            sys.stdout = fh
            sys.stderr = fh
        except OSError:
            sys.stdout = sys.stderr = open(os.devnull, "w")
    if sys.stdin is None:
        sys.stdin = open(os.devnull, "r")


setup_streams()

app = Flask(__name__)
jobs = {}
clients = {}  # tab id -> last ping
state_lock = threading.Lock()
empty_since = time.time() + STARTUP_GRACE  # None while at least one tab is open

# No "GET /api/status" spam in the log.
logging.getLogger("werkzeug").setLevel(logging.WARNING)

PCT = re.compile(r"\[download\]\s+(\d+(?:\.\d+)?)%")
OUT_TIME = re.compile(r"out_time_(?:us|ms)=(\d+)")
FFMPEG_PROGRESS_PREFIXES = (
    "frame=", "fps=", "stream_", "bitrate=", "total_size=", "out_time",
    "dup_frames=", "drop_frames=", "speed=", "progress=",
)
NUM = r"\d+(?:\.\d+)?"
ETA_RE = re.compile(r"ETA\s+(\d+(?::\d+){1,2}|Unknown)")
SPEED_RE = re.compile(r"\bat\s+(\S+/s)")
FFMPEG_TIME = re.compile(r"time=(\d+):(\d+):(\d+(?:\.\d+)?)")


def hms_to_sec(text):
    secs = 0.0
    for p in text.split(":"):
        secs = secs * 60 + float(p)
    return int(secs)


class Coded(Exception):
    """Error with a code: the page translates it into the chosen language."""
    def __init__(self, code, text, arg=""):
        super().__init__(text)
        self.code, self.arg = code, arg


class CodedValueError(Coded, ValueError):
    pass


def parse_time(text):
    """Accepts 'ss', 'mm:ss' or 'hh:mm:ss'. Empty -> None."""
    text = (text or "").strip()
    if not text:
        return None
    if re.fullmatch(NUM, text):
        return float(text)
    parts = text.split(":")
    if len(parts) in (2, 3) and all(re.fullmatch(NUM, p) for p in parts):
        secs = 0.0
        for p in parts:
            secs = secs * 60 + float(p)
        return secs
    raise CodedValueError("bad_time", f"Invalid time: '{text}' (use mm:ss, hh:mm:ss or seconds)", text)


def safe_name(name):
    return re.sub(r"[^\w\-. ]", "_", (name or "").strip())[:80].strip(" .")


def log(line):
    try:
        print(line, flush=True)
    except Exception:  # noqa: BLE001
        pass


def ytdlp_cmd():
    """How to launch yt-dlp: external exe next to the app if present; otherwise ourselves."""
    if FROZEN:
        ext = BASE / "yt-dlp.exe"
        if ext.exists():
            return [str(ext)]
        return [sys.executable, "--run-yt-dlp"]
    exe = Path(sys.executable)
    if exe.name.lower() == "pythonw.exe" and exe.with_name("python.exe").exists():
        exe = exe.with_name("python.exe")  # with pythonw, child processes have stdout None
    return [str(exe), "-m", "yt_dlp"]


def run(cmd, job, parse_progress=False, on_line=None):
    proc = subprocess.Popen(
        cmd,
        stdin=subprocess.DEVNULL,  # without a console, inheriting stdin breaks everything (WinError 6)
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        creationflags=NO_WINDOW,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    tail = []
    for line in proc.stdout:
        line = line.strip()
        if not line:
            continue
        consumed = on_line(line) if on_line else False
        if consumed:
            continue
        tail.append(line)
        tail = tail[-15:]
        job["last_line"] = line[:200]
        log(line)
        if parse_progress:
            m = PCT.search(line)
            if m:
                job["progress"] = float(m.group(1))
    proc.wait()
    return proc.returncode, "\n".join(tail)


def probe_duration(path):
    try:
        p = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=nw=1:nk=1", str(path)],
            stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=30,
            creationflags=NO_WINDOW,
        )
        return float(p.stdout.strip())
    except Exception:  # noqa: BLE001
        return None


def convert(src, dst, height, audio, crf, job=None, duration=None):
    job = job if job is not None else {}
    cmd = [
        "ffmpeg", "-y", "-loglevel", "error", "-nostats", "-progress", "pipe:1",
        "-i", str(src),
        "-vf", f"scale=-2:'min(ih,{height})'",
        "-c:v", "libx264", "-preset", "medium", "-crf", str(crf),
        "-pix_fmt", "yuv420p", "-movflags", "+faststart",
    ]
    cmd += ["-c:a", "aac", "-b:a", "128k"] if audio else ["-an"]
    cmd.append(str(dst))
    t0 = time.time()

    def on_line(line):
        m = OUT_TIME.match(line)
        if m:
            if duration:
                p = min(99.0, int(m.group(1)) / 1e6 / duration * 100)
                job["progress"] = p
                if p >= 2:
                    job["eta"] = int((time.time() - t0) * (100 - p) / p)
            return True
        return line.startswith(FFMPEG_PROGRESS_PREFIXES)

    return run(cmd, job, on_line=on_line)


def tmp_size_mb(d):
    total = 0
    try:
        for p in d.rglob("*"):
            try:
                if p.is_file():
                    total += p.stat().st_size
            except OSError:
                pass
    except OSError:
        pass
    return round(total / 1024 / 1024, 1)


def run_job(job_id, url, start, end, height, audio, crf, name):
    job = jobs[job_id]
    tmpdir = TMP / job_id
    tmpdir.mkdir(parents=True, exist_ok=True)
    try:
        job.update(stage="download", progress=0, msg="Downloading the video from YouTube...", code="downloading",
                   eta=None, speed=None, track=0)
        stage_t0 = time.time()
        section_total = (end - (start or 0)) if end is not None else None

        def on_dl_line(line):
            if line.startswith("[download]"):
                if line.startswith("[download] Destination:"):
                    job["track"] = job.get("track", 0) + 1
                e = ETA_RE.search(line)
                if e:
                    job["eta"] = None if e.group(1) == "Unknown" else hms_to_sec(e.group(1))
                sp = SPEED_RE.search(line)
                if sp:
                    job["speed"] = sp.group(1)
                return False  # stays in the log, and run() reads the %
            # With start/end yt-dlp prints no percentages: ffmpeg does the work and writes "time=..."
            if "frame=" in line and "time=" in line:
                m = FFMPEG_TIME.search(line)
                if m:
                    t = int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))
                    if section_total:
                        p = min(99.0, t / section_total * 100)
                        job["progress"] = p
                        if p >= 2:
                            job["eta"] = int((time.time() - stage_t0) * (100 - p) / p)
                        job["last_line"] = f"ffmpeg: {t:.0f}s of {section_total:.0f}s of the cut processed"
                    else:
                        job["last_line"] = f"ffmpeg: {t:.0f}s processed (no end given, no ETA)"
                return True  # consumed: don't clutter the log
            return False

        cmd = ytdlp_cmd() + [
            "--no-playlist", "--newline", "--no-colors",
            "-f", f"bv*[height<={height}]+ba/b[height<={height}]/b",
            "--merge-output-format", "mp4",
            "-o", str(tmpdir / "src.%(ext)s"),
        ]
        if start is not None or end is not None:
            s = f"{(start or 0):.2f}"
            e = f"{end:.2f}" if end is not None else "inf"
            cmd += ["--download-sections", f"*{s}-{e}", "--force-keyframes-at-cuts"]
        cmd.append(url)

        code, tail = run(cmd, job, parse_progress=True, on_line=on_dl_line)
        if code != 0:
            raise Coded("ytdlp_failed", "yt-dlp failed:\n" + tail, tail)

        candidates = [
            p for p in tmpdir.glob("src.*")
            if p.suffix not in (".part", ".ytdl") and p.is_file()
        ]
        if not candidates:
            raise Coded("no_file", "Download finished but the downloaded file can't be found.")
        src = max(candidates, key=lambda p: p.stat().st_size)

        duration = probe_duration(src)
        job.update(stage="convert", progress=0 if duration else None,
                   msg="Converting to MP4 H.264...", code="converting", last_line="", eta=None, speed=None)
        base = name or time.strftime("clip_%Y%m%d_%H%M%S")
        dst = OUT / f"{base}.mp4"
        if dst.exists():
            dst = OUT / f"{base}_{job_id[:4]}.mp4"
        code, tail = convert(src, dst, height, audio, crf, job, duration)
        if code != 0:
            raise Coded("ffmpeg_failed", "ffmpeg failed:\n" + tail, tail)

        job.update(stage="done", progress=100, msg="Done.", file=str(dst), filename=dst.name,
                   size_mb=round(dst.stat().st_size / 1024 / 1024, 1))
    except Exception as exc:  # noqa: BLE001
        job.update(stage="error", msg=str(exc), code=getattr(exc, "code", None), arg=getattr(exc, "arg", ""))
    finally:
        job["t_end"] = time.time()
        shutil.rmtree(tmpdir, ignore_errors=True)


def guard():
    # Block "blind" requests from other pages open in the browser.
    if request.headers.get("X-Cutito") != "1":
        abort(403)


@app.get("/")
def index():
    html = (RES / "index.html").read_text(encoding="utf-8").replace("__TOKEN__", TOKEN)
    resp = Response(html, mimetype="text/html")
    resp.headers["Cache-Control"] = "no-store"
    return resp


@app.get("/api/who")
def who():
    return "cutito"


@app.post("/api/ping")
def ping():
    global empty_since
    guard()
    cid = (request.args.get("c") or "?")[:40]
    with state_lock:
        clients[cid] = time.time()
        empty_since = None
    return jsonify(ok=True)


@app.post("/api/bye")
def bye():
    """Called by the browser when the tab is closed (sendBeacon: no custom headers)."""
    global empty_since
    if request.args.get("t") != TOKEN:
        abort(403)
    cid = (request.args.get("c") or "?")[:40]
    with state_lock:
        clients.pop(cid, None)
        if not clients:
            empty_since = time.time()
    return "", 204


@app.post("/api/start")
def start():
    guard()
    d = request.get_json(force=True, silent=True) or {}
    url = (d.get("url") or "").strip()
    if not re.match(r"https?://", url):
        return jsonify(error="Invalid link: it must start with http:// or https://", code="bad_url"), 400
    try:
        s = parse_time(d.get("start"))
        e = parse_time(d.get("end"))
    except ValueError as ex:
        return jsonify(error=str(ex), code=getattr(ex, "code", None), arg=getattr(ex, "arg", "")), 400
    if s is not None and e is not None and e <= s:
        return jsonify(error="The end must be after the start.", code="end_before_start"), 400
    if not shutil.which("ffmpeg"):
        return jsonify(error="ffmpeg not found. Install it (see README.en.md) and restart.", code="no_ffmpeg"), 400

    try:
        height = int(d.get("height", 720))
        crf = int(d.get("crf", 26))
    except (TypeError, ValueError):
        return jsonify(error="Invalid parameters.", code="bad_params"), 400
    if height not in (480, 720, 1080):
        height = 720
    if crf not in (23, 26, 30):
        crf = 26
    audio = bool(d.get("audio", False))
    name = safe_name(d.get("name"))

    job_id = uuid.uuid4().hex
    jobs[job_id] = {"stage": "queued", "progress": 0, "msg": "Queued...", "code": "queued",
                    "last_line": "", "t0": time.time()}
    threading.Thread(
        target=run_job, args=(job_id, url, s, e, height, audio, crf, name), daemon=True
    ).start()
    return jsonify(id=job_id)


@app.get("/api/status/<job_id>")
def status(job_id):
    guard()
    job = jobs.get(job_id)
    if not job:
        abort(404)
    out = {k: v for k, v in job.items() if k not in ("file", "t0", "t_end")}
    out["elapsed"] = int(job.get("t_end", time.time()) - job["t0"])
    out["bytes_mb"] = tmp_size_mb(TMP / job_id)
    return jsonify(out)


@app.get("/api/file/<job_id>")
def get_file(job_id):
    job = jobs.get(job_id)
    if not job or job.get("stage") != "done":
        abort(404)
    return send_file(job["file"], as_attachment=True, download_name=job["filename"])


@app.post("/api/open-folder")
def open_folder():
    guard()
    if hasattr(os, "startfile"):
        os.startfile(str(OUT))  # Windows only
    return jsonify(ok=True)


def watchdog():
    """Closes the app when no tabs are open and no jobs are running."""
    global empty_since
    prev = time.time()
    while True:
        time.sleep(1)
        now = time.time()
        with state_lock:
            if now - prev > 10:  # the PC was asleep: give the pages time to ping again
                for k in clients:
                    clients[k] = now
                if not clients and empty_since is not None:
                    empty_since = max(empty_since, now)
            for k in [k for k, ts in clients.items() if now - ts > PING_TIMEOUT]:
                clients.pop(k)
            if not clients and empty_since is None:
                empty_since = now
            gone = not clients and empty_since is not None and now - empty_since > GRACE
        prev = now
        busy = any(j.get("stage") in BUSY for j in list(jobs.values()))
        if gone and not busy:
            log("No tab open and no job running: shutting down.")
            os._exit(0)


def alert(msg):
    log(msg)
    try:
        import ctypes
        ctypes.windll.user32.MessageBoxW(0, msg, "Cutito", 0x10)
    except Exception:  # noqa: BLE001  (not Windows)
        pass


UI_URL = f"http://cutito.localhost:{PORT}"  # *.localhost points to your PC: browsers resolve it on their own


def find_app_browser():
    """Edge or Chrome, to open Cutito in a dedicated window (no address bar)."""
    env = os.environ.get("CUTITO_BROWSER")
    if env and Path(env).exists():
        return env
    roots = [os.environ.get(k) for k in ("ProgramFiles", "ProgramFiles(x86)", "LocalAppData")]
    rels = (r"Microsoft\Edge\Application\msedge.exe", r"Google\Chrome\Application\chrome.exe")
    for rel in rels:
        for root in roots:
            if root and (Path(root) / rel).exists():
                return str(Path(root) / rel)
    for name in ("msedge", "chrome", "google-chrome", "chromium"):
        found = shutil.which(name)
        if found:
            return found
    return None


def open_ui():
    """Opens Cutito as an app window; if that fails, uses the default browser."""
    exe = find_app_browser()
    if exe:
        try:
            subprocess.Popen(
                [exe, f"--app={UI_URL}", "--window-size=780,880"],
                stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            )
            return
        except Exception as exc:  # noqa: BLE001
            log(f"Dedicated window failed ({exc}), using the default browser.")
    webbrowser.open(UI_URL)


def port_open():
    try:
        with socket.create_connection(("127.0.0.1", PORT), timeout=0.5):
            return True
    except OSError:
        return False


def cleanup_tmp():
    for p in TMP.iterdir():
        shutil.rmtree(p, ignore_errors=True)


def main():
    url = f"http://127.0.0.1:{PORT}"
    if port_open():
        # Something is already on the port: either it's Cutito (then just open the window) or something else.
        try:
            ours = urllib.request.urlopen(url + "/api/who", timeout=2).read() == b"cutito"
        except Exception:  # noqa: BLE001
            ours = False
        if ours:
            open_ui()
        else:
            alert(f"Port {PORT} is in use by another program. Close it and try again.")
        return

    cleanup_tmp()
    os.environ["PATH"] = str(BASE) + os.pathsep + os.environ.get("PATH", "")  # ffmpeg.exe next to the app
    threading.Thread(target=watchdog, daemon=True).start()
    threading.Timer(1.0, open_ui).start()
    log(f"Server at {url}")
    app.run(host="127.0.0.1", port=PORT, threaded=True)


if __name__ == "__main__":
    try:
        main()
    except Exception:  # noqa: BLE001
        err = traceback.format_exc()
        alert("Cutito stopped because of an error:\n\n" + err[-600:] + f"\nLog: {WORK / 'cutito.log'}")
        sys.exit(1)
