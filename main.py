from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

# =========================
# Settings
# =========================
RSN = "Rafolax"          # Your RuneScape username
BASE_XP = 4458457        # XP already completed (from previous laps)
XP_PER_LAP = 889         # XP per 1 Ardougne Rooftop lap
# =========================

@app.route("/ardy")
def ardy_laps():
    # Fetch hiscores
    url = f"https://secure.runescape.com/m=hiscore_oldschool/index_lite.ws?player={RSN}"
    r = requests.get(url)
    if r.status_code != 200:
        return jsonify({"error": "Could not fetch hiscores"}), 500

    # Split by commas and remove spaces
    data = [x.strip() for x in r.text.split(",")]

    try:
        # Agility XP is the 37th number
        agility_xp = int(data[36])
    except (IndexError, ValueError):
        return jsonify({"error": "Agility XP not found"}), 500

    # Calculate laps
    laps = (agility_xp - BASE_XP) // XP_PER_LAP
    if laps < 0:
        laps = 0

    return jsonify({"laps": laps})

# =========================
# Dynamic port for Render
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Use Render-assigned port
    app.run(host="0.0.0.0", port=port)