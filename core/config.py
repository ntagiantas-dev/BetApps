# config.py
import os

# Το βασικό URL του BSD Football API (με το /football/ στη μέση)
BASE_URL = "https://sports.bzzoiro.com/api/v2"

# Διαβάζει το API key αυτόματα από τις Environment Variables του Render
API_KEY = os.getenv("BSD_API_KEY", "MISSING_API_KEY")

# Οι 5 ελληνικές ομάδες που στοχεύουμε στο v0.1
TARGET_COUNTRY = "GR"
TARGET_TEAMS = [
    "Olympiacos",
    "AEK Athens",
    "PAOK",
    "Panathinaikos",
    "Aris Thessaloniki"
]