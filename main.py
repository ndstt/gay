# sse_probe.py
import requests, json

url = "https://stream.wikimedia.org/v2/stream/recentchange"
with requests.get(url, stream=True, timeout=30) as r:
    for raw in r.iter_lines():
        if not raw or not raw.startswith(b"data:"):
            continue
        ev = json.loads(raw[5:])
        print(ev.get("title"), ev.get("type"), ev.get("timestamp"))
        break  # แค่พิสูจน์ว่าของมา
