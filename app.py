from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from database.db import get_db, init_db, seed_db

app = Flask(__name__)
app.secret_key = "dev-secret-key-change-in-production"


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")

    if not name or not email or not password:
        return render_template(
            "register.html",
            error="All fields are required.",
            name=name,
            email=email,
        )

    if len(password) < 8:
        return render_template(
            "register.html",
            error="Password must be at least 8 characters long.",
            name=name,
            email=email,
        )

    conn = get_db()
    try:
        existing = conn.execute(
            "SELECT id FROM users WHERE email = ?", (email,)
        ).fetchone()
        if existing is not None:
            return render_template(
                "register.html",
                error="An account with that email already exists.",
                name=name,
                email=email,
            )

        password_hash = generate_password_hash(password, method="pbkdf2:sha256")
        conn.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            (name, email, password_hash),
        )
        conn.commit()
    finally:
        conn.close()

    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")

    generic_error = "Invalid email or password."

    if not email or not password:
        return render_template("login.html", error=generic_error, email=email)

    conn = get_db()
    try:
        user = conn.execute(
            "SELECT id, name, password_hash FROM users WHERE email = ?", (email,)
        ).fetchone()
    finally:
        conn.close()

    if user is None or not check_password_hash(user["password_hash"], password):
        return render_template("login.html", error=generic_error, email=email)

    session["user_id"] = user["id"]
    session["user_name"] = user["name"]
    return redirect(url_for("profile"))


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/profile")
def profile():
    if not session.get("user_id"):
        return redirect(url_for("login"))

    conn = get_db()
    try:
        row = conn.execute(
            "SELECT name, email, created_at FROM users WHERE id = ?",
            (session["user_id"],),
        ).fetchone()
    finally:
        conn.close()

    name_parts = row["name"].split()
    initials = "".join(part[0] for part in name_parts[:2]).upper()
    member_since = datetime.strptime(
        row["created_at"], "%Y-%m-%d %H:%M:%S"
    ).strftime("%B %Y")

    user = {
        "initials": initials,
        "name": row["name"],
        "email": row["email"],
        "member_since": member_since,
    }
    stats = [
        {"label": "Total spent", "value": "₹345.99"},
        {"label": "Transactions", "value": "8"},
        {"label": "Top category", "value": "Bills"},
    ]
    transactions = [
        {"date": "2026-06-15", "description": "Dinner with friends", "category": "Food", "slug": "food", "amount": "₹18.75"},
        {"date": "2026-06-13", "description": "Miscellaneous", "category": "Other", "slug": "other", "amount": "₹9.99"},
        {"date": "2026-06-11", "description": "Clothing", "category": "Shopping", "slug": "shopping", "amount": "₹80.00"},
        {"date": "2026-06-09", "description": "Movie ticket", "category": "Entertainment", "slug": "entertainment", "amount": "₹25.00"},
        {"date": "2026-06-07", "description": "Pharmacy", "category": "Health", "slug": "health", "amount": "₹35.00"},
    ]
    categories = [
        {"name": "Bills", "slug": "bills", "total": "₹120.00", "percent": 35},
        {"name": "Shopping", "slug": "shopping", "total": "₹80.00", "percent": 23},
        {"name": "Transport", "slug": "transport", "total": "₹45.00", "percent": 13},
        {"name": "Health", "slug": "health", "total": "₹35.00", "percent": 10},
        {"name": "Food", "slug": "food", "total": "₹31.25", "percent": 9},
        {"name": "Entertainment", "slug": "entertainment", "total": "₹25.00", "percent": 7},
        {"name": "Other", "slug": "other", "total": "₹9.99", "percent": 3},
    ]
    return render_template(
        "profile.html",
        user=user,
        stats=stats,
        transactions=transactions,
        categories=categories,
    )


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


with app.app_context():
    init_db()
    seed_db()


if __name__ == "__main__":
    app.run(debug=True, port=5001)
