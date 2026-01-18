from flask import Flask, request, jsonify
import sqlite3, os

app = Flask(__name__)

# Correct path for Render + local
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "chatbot.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS chats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            bot TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_msg = data.get("message", "")

    if "fever" in user_msg.lower():
        bot_reply = "You may have fever. Drink water, rest, and see a doctor if it stays high."
    elif "headache" in user_msg.lower():
        bot_reply = "For headache, try resting and staying hydrated."
    elif "thanks" in user_msg.lower():
        bot_reply = "You're welcome! Take care."
    else:
        bot_reply = "Please describe your symptoms clearly."

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO chats (user, bot) VALUES (?, ?)", (user_msg, bot_reply))
    conn.commit()
    conn.close()

    return jsonify({"reply": bot_reply})

# Render uses dynamic PORT
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
