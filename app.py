import os
import psycopg2
from flask import Flask, jsonify

app = Flask(__name__)

def get_connection():
    try:
        return psycopg2.connect(
            host=os.environ["DB_HOST"],
            database=os.environ["DB_NAME"],
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASSWORD"],
            port=os.environ["DB_PORT"]
        )
    except Exception as e:
        print("❌ Database connection failed:", e)
        return None

@app.route("/")
def home():
    return "✅ Flask API is running!"

@app.route("/sales")
def get_sales():
    conn = get_connection()
    if conn is None:
        return jsonify({"error": "Database not connected"}), 500

    cur = conn.cursor()
    cur.execute("SELECT * FROM sales LIMIT 10;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(rows)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
