"""Turn an Open-Meteo multi-location response into weather.json and weather.js for Hanamura Naoki."""
import json, sys, datetime
KEYS = ["sai-gon", "can-tho", "ha-noi", "hai-phong", "hue", "da-nang", "nha-trang", "da-lat"]
raw = json.load(open(sys.argv[1], encoding="utf-8"))
if isinstance(raw, dict):
    raw = [raw]
cities = {}
for key, loc in zip(KEYS, raw):
    cur = loc.get("current") or {}
    if cur.get("temperature_2m") is None:
        continue
    cities[key] = {
        "t": round(cur["temperature_2m"]),
        "h": round(cur.get("relative_humidity_2m") or 0),
        "code": cur.get("weather_code", 0),
        "day": cur.get("is_day", 1),
        "time": cur.get("time"),
    }
if not cities:
    sys.exit("no weather data")
data = {"at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"), "source": "Open-Meteo", "cities": cities}
body = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
open("weather.json", "w", encoding="utf-8").write(body + "\n")
open("weather.js", "w", encoding="utf-8").write(
    "window.NAOKI_WX=" + body + ";try{window.dispatchEvent(new Event('naoki-wx'))}catch(e){}\n")
print("updated", len(cities), "cities")
