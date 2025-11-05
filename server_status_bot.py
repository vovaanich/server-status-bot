import os
import sys
from datetime import datetime
import pytz
import psutil
import requests
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
HOSTNAME = os.getenv("HOSTNAME") or os.uname().nodename
TIMEOUT = float(os.getenv("TIMEOUT", 10))
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

KYIV_TZ = pytz.timezone("Europe/Kiev")

def get_cpu_percent():
    return psutil.cpu_percent(interval=1)

def get_loadavg():
    try:
        return os.getloadavg()
    except:
        return (0.0, 0.0, 0.0)

def get_memory():
    v = psutil.virtual_memory()
    return {"total": v.total, "used": v.used, "percent": v.percent}

def format_bytes(n):
    for unit in ['B','KB','MB','GB','TB']:
        if n < 1024.0:
            return f"{n:3.1f}{unit}"
        n /= 1024.0
    return f"{n:.1f}PB"

def build_message():
    tnow = datetime.now(KYIV_TZ).strftime("%Y-%m-%d %H:%M:%S")
    cpu = get_cpu_percent()
    load1, load5, load15 = get_loadavg()
    mem = get_memory()
    lines = [
        f"✅ Status сервера: {HOSTNAME}",
        f"⏰ Time: {tnow}",
        f"💻 CPU: {cpu:.1f}%  (load: {load1:.2f}, {load5:.2f}, {load15:.2f})",
        f"🖥 RAM: {format_bytes(mem['used'])} / {format_bytes(mem['total'])} ({mem['percent']}%)"
    ]
    return "\n".join(lines)

def send_telegram(text):
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True,
    }
    try:
        r = requests.post(API_URL, json=payload, timeout=TIMEOUT)
        r.raise_for_status()
        return True
    except Exception as e:
        print("Failed to send:", e, file=sys.stderr)
        return False

def main():
    msg = build_message()
    send_telegram(msg)
    return 0

if __name__ == "__main__":
    sys.exit(main())
