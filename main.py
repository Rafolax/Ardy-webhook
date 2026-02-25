from flask import Flask, jsonify
import requests
import os
import re

app = Flask(__name__)

RSN = "Rafolax"
BASE_XP = 4458457
XP_PER_LAP = 889

@app.route("/ardy")
def ardy_laps():
    url = f"https://secure.runescape.com/m=hiscore_oldschool/index_lite.ws?player={RSN}"
    r = requests.get(url)
    if r.status_code != 200:
        return jsonify({"error": "Could not fetch hiscores"}), 500

    # Split by commas, remove spaces, ignore empty strings
    data = [x.strip() for x in r.text.split(",") if x.strip()]

    try:
        # Exact index for Agility XP in your file
        agility_xp = int(data[36])
    except (IndexError, ValueError):
        return jsonify({"error": "Agility XP not found"}), 500

    laps = (agility_xp - BASE_XP) // XP_PER_LAP
    if laps < 0:
        laps = 0

    return jsonify({"laps": laps})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)