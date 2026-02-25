from flask import Flask, jsonify
import requests

app = Flask(__name__)

# Your RSN and lap calculation settings
RSN = "rafolax"
BASE_XP = 4458457  # XP already done
XP_PER_LAP = 889
AGILITY_INDEX = 17  # 18th skill in OSRS index_lite.ws (0-based)

@app.route("/ardy")
def ardy_laps():
    # Fetch your hiscores lite file
    url = f"https://secure.runescape.com/m=hiscore_oldschool/index_lite.ws?player={RSN}"
    r = requests.get(url)
    if r.status_code != 200:
        return jsonify({"error": "Could not fetch hiscores"}), 500

    # Split the file by commas (single-line hiscores)
    data = r.text.split(",")
    try:
        agility_xp = int(data[AGILITY_INDEX*2 + 1])  # XP is second number in pair
    except (IndexError, ValueError):
        return jsonify({"error": "Agility XP not found"}), 500

    # Calculate laps
    laps = (agility_xp - BASE_XP) // XP_PER_LAP
    if laps < 0:
        laps = 0

    return jsonify({"laps": laps})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)