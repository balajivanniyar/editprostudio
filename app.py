from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sqlite3
from datetime import datetime

app = Flask(__name__)
CORS(app)

def init_db():
    conn = sqlite3.connect("messages.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS enquiries(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        phone TEXT,
        project_type TEXT,
        message TEXT,
        created_at TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

@app.route("/")
def home():
    return render_template("editprostudio.html")

@app.route("/submit", methods=["POST"])
def submit():
    data = request.json

    conn = sqlite3.connect("messages.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO enquiries
    (name,email,phone,project_type,message,created_at)
    VALUES (?,?,?,?,?,?)
    """,(
        data["name"],
        data["email"],
        data["phone"],
        data["project_type"],
        data["message"],
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()

    return jsonify({"success": True})

@app.route("/admin")
def admin():
    conn = sqlite3.connect("messages.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM enquiries ORDER BY id DESC")
    data = cursor.fetchall()

    conn.close()

    html = """
    <h1>Enquiries</h1>
    <table border='1' cellpadding='10'>
    <tr>
    <th>ID</th>
    <th>Name</th>
    <th>Email</th>
    <th>Phone</th>
    <th>Project</th>
    <th>Message</th>
    <th>Date</th>
    </tr>
    """

    for row in data:
        html += f"""
        <tr>
        <td>{row[0]}</td>
        <td>{row[1]}</td>
        <td>{row[2]}</td>
        <td>{row[3]}</td>
        <td>{row[4]}</td>
        <td>{row[5]}</td>
        <td>{row[6]}</td>
        </tr>
        """

    html += "</table>"
    return html

if __name__ == "__main__":
    app.run(debug=True)