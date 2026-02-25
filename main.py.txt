from flask import Flask, jsonify
import requests

app = Flask(name)

RSN = "Rafolax"
BASE_XP = 4458457
XP_PER_LAP = 889
AGILITY_LINE = 16  # 17th line (0-based)

@app.route("/ardy")
def ardy_laps():
    url = f"https://secure.runescape.com/m=hiscore_oldschool/index_lite.ws?player={RSN}"
    r = requests.get(url)
    if r.status_code != 200:
        return jsonify({"error": "Could not fetch hiscores"}), 500

    lines = r.text.splitlines()
    try:
        agility_xp = int(lines[AGILITY_LINE])
    except (IndexError, ValueError):
        return jsonify({"error": "Agility XP not found"}), 500

    laps = (agility_xp - BASE_XP) // XP_PER_LAP
    if laps < 0:
        laps = 0

    return jsonify({"laps": laps})

if name == "main":
    app.run(host="0.0.0.0", port=10000)