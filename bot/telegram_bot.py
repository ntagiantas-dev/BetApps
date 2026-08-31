# bot/telegram_bot.py

class LiveStatBot:
    """
    Διαχειρίζεται τις ειδοποιήσεις και τα μηνύματα του Bot (π.χ. Telegram).
    Στέλνει live ενημερώσεις για γκολ, κατοχή και momentum.
    """
    def __init__(self, token=None):
        self.token = token

    def send_match_update(self, chat_id, team_a, team_b, score, momentum_info):
        """
        Διαμορφώνει και στέλνει ένα καθαρό μήνυμα κατάστασης αγώνα.
        """
        message = (
            f"🚨 **LIVE UPDATE** 🚨\n\n"
            f"⚽ {team_a} vs {team_b}\n"
            f"📊 Σκορ: {score}\n"
            f"⚡ {momentum_info}\n"
        )
        # Εδώ θα μπει η λογική αποστολής (π.χ. requests.post στο Telegram API)
        print(f"[Bot Simulator] Sending to chat {chat_id}:\n{message}")
        return message