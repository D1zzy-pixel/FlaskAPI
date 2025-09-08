from flask import Flask, jsonify
from flask_cors import CORS
import psycopg2
import os

app = Flask(__name__)
CORS(app)

# ดึง DATABASE_URL จาก Environment Variables ของ Render
DATABASE_URL = os.getenv("DATABASE_URL")

def get_connection():
    return psycopg2.connect(DATABASE_URL)

@app.route("/")
def home():
    return jsonify({"message": "Flask API is running!"})

@app.route("/sales")
def get_sales():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM sales LIMIT 10;")  # ดึงตัวอย่าง 10 แถว
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(rows)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
