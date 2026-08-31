# services/match_service.py
from api.client import BSDAPIClient
from database import LiveStatDatabase
from core.config import TARGET_TEAMS

class MatchService:
    def __init__(self):
        self.api_client = BSDAPIClient()
        self.db = LiveStatDatabase()

    def sync_greek_teams_pregame(self):
        """
        Τραβάει τις ομάδες από το API, φιλτράρει τις 5 ελληνικές ομάδες στόχους (v0.1)
        και αποθηκεύει τα pregame data τους στη βάση.
        """
        print("[Service] Συγχρονισμός pregame δεδομένων για τις ελληνικές ομάδες...")
        response = self.api_client.get_greek_teams()
        
        if not response or "data" not in response:
            print("[Service] Αποτυχία λήψης ομάδων από το API.")
            return False

        teams_data = response["data"]
        count = 0

        for team in teams_data:
            team_name = team.get("name")
            if team_name in TARGET_TEAMS:
                country = team.get("country_code", "GR")
                # Ενδεικτικά πεδία μορφής και xG για το v0.1
                form_data = team.get("form", ["W", "D", "L"])
                xg_avg = team.get("xg_avg", 1.35)  # Default τιμή αν δεν υπάρχει
                
                # Αποθήκευση στη SQLite
                self.db.save_pregame_data(team_name, country, form_data, xg_avg)
                print(f"[Service] Αποθηκεύτηκε η ομάδα: {team_name} (xG avg: {xg_avg})")
                count += 1

        print(f"[Service] Επιτυχής συγχρονισμός {count}/5 ελληνικών ομάδων.")
        return True

    def process_live_tick(self):
        """
        Ελέγχει τα live events, εντοπίζει αγώνες των ελληνικών ομάδων
        και καταγράφει live row με xG για τα γραφικά.
        """
        print("[Service] Έλεγχος live αγώνων...")
        live_response = self.api_client.get_live_events()
        
        if not live_response or "data" not in live_response:
            print("[Service] Κανένα live event ή σφάλμα σύνδεσης.")
            return

        events = live_response["data"]
        for event in events:
            home_team = event.get("home_team", {}).get("name")
            away_team = event.get("away_team", {}).get("name")

            # Αν αγωνίζεται κάποια από τις 5 ελληνικές ομάδες μας
            if home_team in TARGET_TEAMS or away_team in TARGET_TEAMS:
                match_id = str(event.get("id"))
                minute = event.get("minute", 0)
                home_xg = event.get("home_xg", 0.0)
                away_xg = event.get("away_xg", 0.0)
                possession = event.get("possession", {"home": 50, "away": 50})
                
                # Καταγραφή στη βάση για τα γραφικά (xG history κλπ.)
                self.db.log_live_row(
                    match_id=match_id,
                    minute=minute,
                    home_team=home_team,
                    away_team=away_team,
                    home_xg=home_xg,
                    away_xg=away_xg,
                    possession_dict=possession,
                    raw_data=event
                )
                print(f"[Live Match] {home_team} vs {away_team} | Λεπτό: {minute}' | xG: {home_xg} - {away_xg}")