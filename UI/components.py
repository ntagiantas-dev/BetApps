# ui/components.py

class LiveMatchWidget:
    """
    Διαχειρίζεται τα βασικά οπτικά στοιχεία του v0.1:
    - Momentum Bar (Δυναμική πίεσης αγώνα)
    - Possession & Data Points (Κατοχή και κρίσιμα νούμερα)
    """
    def __init__(self, match_data=None):
        self.match_data = match_data or {}

    def render_momentum_bar(self, home_possession, away_possession):
        """
        Επιστρέφει την οπτική μπάρα κατανομής κατοχής/πίεσης των δύο ομάδων.
        """
        return f"⚽ Momentum Bar -> [Home: {home_possession}%] === [Away: {away_possession}%]"

    def render_possession_stats(self):
        """
        Επιστρέφει τα βασικά στατιστικά κατοχής για απεικόνιση στην οθόνη.
        """
        return {
            "home_possession": self.match_data.get("home_possession", "50%"),
            "away_possession": self.match_data.get("away_possession", "50%")
        }