
from flask import Flask, render_template
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)


def get_visits():
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

    try:
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE visitor_counter
            SET visits = visits + 1
            WHERE id = 1
        """)

        cursor.execute("""
            SELECT visits
            FROM visitor_counter
            WHERE id = 1
        """)

        visits = cursor.fetchone()[0]
        conn.commit()

        return visits

    finally:
        cursor.close()
        conn.close()


@app.route("/")
def home():
    visits = get_visits()

    return render_template(
        "index.html",
        visits=visits
    )


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=8000
    )
