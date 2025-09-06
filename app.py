import os
from flask import Flask, jsonify
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app)

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="Jewllista_DB",
        user="postgres",
        password="Tiger@1234",
        port=5432
    )

@app.route("/sales", methods=["GET"])
def get_sales():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT times, store, barcode, quantity, subtotal, discount
        FROM sales
        WHERE quantity IS NOT NULL
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()

    result = [
        {
            "times": str(r[0]),
            "store": r[1],
            "barcode": r[2],
            "quantity": r[3],
            "subtotal": float(r[4]),
            "discount": float(r[5])
        } 
        for r in rows
    ]
    return jsonify(result)

# ใช้ PORT จาก environment variable หรือ default 5000
port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)
