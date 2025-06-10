import sqlite3
from flask import Flask, flash, redirect, render_template, request, session, jsonify, make_response, g
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
from datetime import datetime
from collections import Counter
from dotenv import load_dotenv

import os
import csv, io, json

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configuration
app.secret_key = os.getenv("SECRET_KEY")
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

DATABASE = os.path.join(app.instance_path, "jar.db")


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/faq")
        return f(*args, **kwargs)
    return decorated_function


@app.template_filter('datetimeformat')
def datetimeformat(value):
    dt = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
    return dt.strftime("%b %d, %Y at %I:%M %p")


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    return render_template("index.html")


@app.route("/past")
@login_required
def past():
    db = get_db()
    rows = db.execute("SELECT memory, mood, created_at FROM memories WHERE user_id = ? ORDER BY RANDOM() LIMIT 1", (session["user_id"],)).fetchall()

    if not rows:
        flash("You haven’t added any memories yet!")
        return redirect("/new")

    memory = rows[0]
    return render_template("past.html", memory=memory)


@app.route("/new", methods=["GET", "POST"])
@login_required
def new():
    db = get_db()
    if request.method == "POST":
        memory = request.form.get("memory")
        mood = request.form.get("mood")

        if not memory:
            flash("Memory can't be empty!")
            return redirect("/new")

        db.execute("INSERT INTO memories (user_id, memory, mood) VALUES (?, ?, ?)", (session["user_id"], memory, mood))
        db.commit()
        flash("Memory added successfully!")
        return redirect("/")

    return render_template("new.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    session.pop("user_id", None)

    if request.method == "POST":
        if not request.form.get("username"):
            flash("Username can't be blank")
            return redirect("/login")

        elif not request.form.get("password"):
            flash("Password can't be blank")
            return redirect("/login")

        db = get_db()
        rows = db.execute("SELECT * FROM users WHERE username = ?", (request.form.get("username"),)).fetchall()

        if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
            flash("Invalid username and/or password")
            return redirect("/login")

        session["user_id"] = rows[0]["id"]
        return redirect("/")

    else:
        return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    session.clear()
    return redirect("/login")


@app.route("/register", methods=["GET", "POST"])
def register():
    db = get_db()
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        rows = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchall()

        if not username:
            flash("Username can't be blank")
            return redirect("/register")

        elif not password:
            flash("Password can't be blank")
            return redirect("/register")

        elif password != confirmation:
            flash("Password didn't match")
            return redirect("/register")

        elif len(rows) == 1:
            flash("Username already exists")
            return redirect("/register")

        hash_pw = generate_password_hash(password)
        db.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hash_pw))
        db.commit()

        flash("Registration successful! Please log in.")
        return redirect("/login")

    return render_template("register.html")


@app.route("/faq", methods=["GET"])
def faq():
    return render_template("faq.html")


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.route("/history")
@login_required
def history():
    db = get_db()
    rows = db.execute("SELECT memory, mood, created_at FROM memories WHERE user_id = ? ORDER BY created_at DESC", (session["user_id"],)).fetchall()
    return render_template("history.html", memories=rows)


@app.route("/mood-data")
@login_required
def mood_data():
    db = get_db()
    rows = db.execute("SELECT mood, COUNT(*) as count FROM memories WHERE user_id = ? GROUP BY mood", (session["user_id"],)).fetchall()
    data = {row["mood"]: row["count"] for row in rows}
    return jsonify(data)


@app.route("/mood")
@login_required
def mood():
    db = get_db()
    user_id = session["user_id"]
    rows = db.execute("SELECT mood, created_at FROM memories WHERE user_id = ?", (user_id,)).fetchall()

    mood_counts = Counter(row["mood"] for row in rows)

    month_moods = {}
    year_moods = {}

    for row in rows:
        month = row["created_at"][:7]
        year = row["created_at"][:4]
        mood = row["mood"]
        month_moods.setdefault(month, []).append(mood)
        year_moods.setdefault(year, []).append(mood)

    def happiest(period_dict):
        happiness_rank = {"happy": 3, "content": 2, "neutral": 1, "sad": 0}
        def mood_score(mood_list):
            return sum(happiness_rank.get(m, 0) for m in mood_list)
        if not period_dict:
            return None
        return max(period_dict.items(), key=lambda x: mood_score(x[1]))[0]

    happiest_month = happiest(month_moods)
    happiest_year = happiest(year_moods)

    return render_template("mood.html", mood_counts=mood_counts, happiest_month=happiest_month, happiest_year=happiest_year, has_memories=len(rows) > 0)


@app.template_filter("datetimeformat")
def datetimeformat(value, format="%B %Y"):
    try:
        dt = datetime.strptime(value, "%Y-%m")
        return dt.strftime(format)
    except Exception:
        return value


@app.route("/export")
@login_required
def export():
    format = request.args.get("format", "csv")
    db = get_db()
    memories = db.execute("SELECT memory, mood, created_at FROM memories WHERE user_id = ?", (session["user_id"],)).fetchall()

    if format == "csv":
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["Memory", "Mood", "Created At"])
        for row in memories:
            writer.writerow([row["memory"], row["mood"], row["created_at"]])
        response = make_response(output.getvalue())
        response.headers["Content-Disposition"] = "attachment; filename=memories.csv"
        response.headers["Content-Type"] = "text/csv"

    elif format == "json":
        response = make_response(json.dumps([dict(row) for row in memories], indent=4))
        response.headers["Content-Disposition"] = "attachment; filename=memories.json"
        response.headers["Content-Type"] = "application/json"

    elif format == "txt":
        output = io.StringIO()
        for row in memories:
            output.write(f"{row['created_at']} - [{row['mood']}] {row['memory']}\n")
        response = make_response(output.getvalue())
        response.headers["Content-Disposition"] = "attachment; filename=memories.txt"
        response.headers["Content-Type"] = "text/plain"

    else:
        return "Invalid format", 400

    return response


if __name__ == "__main__":
    app.run(debug=True)
