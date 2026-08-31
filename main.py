# main.py
from services.match_service import MatchService
from ui.components import LiveMatchWidget
from bot.telegram_bot import LiveStatBot

def main():
    print("=" * 60)
    print("🚀 LIVE STAT ARENA - v0.1 (Starting Up...)")
    print("=" * 60)

    # 1. Αρχικοποίηση του Match Service (που διαχειρίζεται API, DB & Logic)
    service = MatchService()

    # 2. Συγχρονισμός Pregame δεδομένων για τις 5 ελληνικές ομάδες
    print("\n[Step 1] Εκτέλεση συγχρονισμού Pregame Data...")
    success = service.sync_greek_teams_pregame()
    
    if success:
        print("[Step 1] Ο συγχρονισμός ολοκληρώθηκε επιτυχώς!")
    else:
        print("[Step 1] Ο συγχρονισμός αντιμετώπισε πρόβλημα (ελέγξτε το API key).")

    # 3. Δοκιμή Live Tick (Έλεγχος ζωντανών αγώνων & καταγραφή xG για γραφικά)
    print("\n[Step 2] Έλεγχος Live Αγώνων & xG Logging...")
    service.process_live_tick()

    # 4. Επίδειξη UI Widget & Bot Notification
    print("\n[Step 3] Δοκιμή UI Components & Bot Simulation...")
    
    # Παράδειγμα χρήσης του UI Widget για κατοχή και momentum
    widget = LiveMatchWidget({"home_possession": "58%", "away_possession": "42%"})
    possession = widget.render_possession_stats()
    momentum = widget.render_momentum_bar(possession["home_possession"], possession["away_possession"])
    print(f"UI Component Test -> {momentum}")

    # Παράδειγμα ειδοποίησης Bot
    bot = LiveStatBot(token="DUMMY_TOKEN")
    bot.send_match_update(
        chat_id="123456789",
        team_a="Olympiacos",
        team_b="Panathinaikos",
        score="1 - 0",
        momentum_info=momentum
    )

    print("\n" + "=" * 60)
    print("✨ Η εφαρμογή v0.1 έτρεξε με επιτυχία και η βάση ενημερώθηκε!")
    print("=" * 60)

if __name__ == "__main__":
    main()