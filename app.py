from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import os

app = Flask(__name__)
CORS(app)

# Neon connection string from environment variable
DATABASE_URL = os.environ.get("DATABASE_URL")

def get_conn():
    return psycopg2.connect(DATABASE_URL)

def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS chats (
            id SERIAL PRIMARY KEY,
            user_message TEXT,
            bot_reply TEXT,
            time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

init_db()

@app.route("/")
def home():
    return "AI Healthcare Backend Running (PostgreSQL)"

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

    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO chats (user_message, bot_reply) VALUES (%s, %s)",
        (user_msg, bot_reply)
    )
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"reply": bot_reply})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
