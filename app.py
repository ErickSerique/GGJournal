from flask import Flask, render_template, request, redirect, session, url_for, flash
from werkzeug.security import check_password_hash, generate_password_hash
from cs50 import SQL
from helpers import login_required, error
import os
import requests
from datetime import date

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev_super_secret")

# Gets the RAWG Database key from the .env file
RAWG_KEY = os.getenv("RAWG_KEY")

# Connects to the sqlite database
db = SQL("sqlite:///ggjournal.db")

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username").strip()
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username or not password or not confirmation:
            return error("All fields are required.", 400)
        if password != confirmation:
            return error("Passwords do not match.", 400)

        existing = db.execute("SELECT id FROM users WHERE username = ?", username)
        if existing:
            return error("Username already taken.", 400)

        hash_pw = generate_password_hash(password)
        db.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", username, hash_pw)

        flash("Account created. Please log in.", "success")
        return redirect("/login")
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        username = request.form.get("username").strip()
        password = request.form.get("password")

        if not username or not password:
            return error("You must provide both username and password.", 400)

        user = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(user) != 1 or not check_password_hash(user[0]["password_hash"], password):
            return error("Invalid username or password.", 403)

        session["user_id"] = user[0]["id"]
        flash("Welcome back!", "success")
        return redirect(url_for("lists_page"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect("/")


@app.route("/lists")
@login_required
def lists_page():
    # Load all lists owned by logged user
    lists = db.execute("SELECT * FROM lists WHERE user_id = ? ORDER BY created_at DESC", session["user_id"])
    return render_template("lists.html", lists=lists)


@app.route("/lists/create", methods=["GET", "POST"])
@login_required
def create_list():
    if request.method == "POST":
        name = request.form.get("name").strip()
        description = request.form.get("description").strip()

        if not name:
            return error("List name is required.", 400)

        # Insert new list connected to user
        db.execute("INSERT INTO lists (user_id, name, description) VALUES (?, ?, ?)", session["user_id"], name, description)

        flash("List created.", "success")
        return redirect(url_for("lists_page"))

    return render_template("create_list.html")


@app.route("/lists/<int:list_id>/edit", methods=["GET", "POST"])
@login_required
def edit_list(list_id):
    # Ensure list exists and belongs to user
    lst = db.execute("SELECT * FROM lists WHERE id = ? AND user_id = ?", list_id, session["user_id"])
    if not lst:
        return error("List not found.", 404)

    if request.method == "POST":
        name = request.form.get("name").strip()
        description = request.form.get("description").strip()

        if not name:
            return error("Name required.", 400)

        # Update list
        db.execute("UPDATE lists SET name = ?, description = ? WHERE id = ?", name, description, list_id)

        flash("List updated.", "success")
        return redirect(url_for("lists_page"))

    return render_template("list_edit.html", list=lst[0])


@app.route("/lists/<int:list_id>/delete", methods=["POST"])
@login_required
def delete_list(list_id):
    # Delete all games belonging to this list
    db.execute("DELETE FROM games WHERE list_id = ?", list_id)

    # Delete list itself
    db.execute("DELETE FROM lists WHERE id = ? AND user_id = ?", list_id, session["user_id"])

    flash("List deleted.", "info")
    return redirect(url_for("lists_page"))


@app.route("/list/<int:list_id>")
@login_required
def view_list(list_id):
    # Ensure list exists
    lst = db.execute("SELECT * FROM lists WHERE id = ? AND user_id = ?", list_id, session["user_id"])

    if not lst:
        return error("List not found.", 404)

    # Load games sorted newest → oldest
    games = db.execute("SELECT * FROM games WHERE list_id = ? ORDER BY created_at DESC, id DESC", list_id)

    return render_template("list_view.html", list=lst[0], games=games)


@app.route("/list/<int:list_id>/add", methods=["GET", "POST"])
@login_required
def add_game(list_id):
    # Checks if list exists and belongs to user
    lst = db.execute("SELECT * FROM lists WHERE id = ? AND user_id = ?", list_id, session["user_id"])

    if not lst:
        return error("List not found.", 404)

    if request.method == "POST":
        title = request.form.get("title").strip()
        cover = request.form.get("cover").strip() if request.form.get("cover") else None
        added_date = request.form.get("added_date") or str(date.today())
        notes = request.form.get("notes").strip() if request.form.get("notes") else None

        if not title:
            return error("Game title required.", 400)

        # Insert new game entry
        db.execute("INSERT INTO games (list_id, title, cover, release_date, notes) VALUES (?, ?, ?, ?, ?)", list_id, title, cover, added_date, notes)

        flash("Game added to the list.", "success")
        return redirect(url_for("view_list", list_id=list_id))

    # Prefill fields when adding game from search results
    title_prefill = request.args.get("title", "")
    cover_prefill = request.args.get("cover", "")

    return render_template("add_game.html", list_id=list_id, title_prefill=title_prefill, cover_prefill=cover_prefill, today=str(date.today()))


@app.route("/list/<int:list_id>/game/<int:game_id>/edit", methods=["GET", "POST"])
@login_required
def edit_game(list_id, game_id):
    # Validate game + list
    game = db.execute("SELECT * FROM games WHERE id = ? AND list_id = ?", game_id, list_id)

    if not game:
        return error("Game not found.", 404)

    game = game[0]

    if request.method == "POST":
        title = request.form.get("title").strip()
        cover = request.form.get("cover").strip() if request.form.get("cover") else None
        added_date = request.form.get("added_date") or game["release_date"]
        notes = request.form.get("notes").strip() if request.form.get("notes") else None

        if not title:
            return error("Title required.", 400)

        # Update row
        db.execute("UPDATE games SET title = ?, cover = ?, release_date = ?, notes = ? WHERE id = ?", title, cover, added_date, notes, game_id)

        flash("Game updated.", "success")
        return redirect(url_for("view_list", list_id=list_id))

    return render_template("edit_game.html", list_id=list_id, game=game)


@app.route("/list/<int:list_id>/game/<int:game_id>/delete", methods=["POST"])
@login_required
def delete_game(list_id, game_id):
    db.execute("DELETE FROM games WHERE id = ? AND list_id = ?", game_id, list_id)
    flash("Game removed.", "info")
    return redirect(url_for("view_list", list_id=list_id))


@app.route("/search", methods=["GET", "POST"])
@login_required
def search():
    results = None

    # Pagination tracking
    page = int(request.form.get("page", 1)) if request.method == "POST" else 1

    if request.method == "POST":
        query = request.form.get("query").strip()

        if not query:
            return error("You must type something to search.", 400)

        url = "https://api.rawg.io/api/games"
        params = {"key": RAWG_KEY, "search": query, "page_size": 10, "page": page}

        api_response = requests.get(url, params=params)

        if api_response.status_code != 200:
            return error("API Error while searching games.", 500)

        data = api_response.json().get("results", [])

        results = [
            {"id": game["id"], "title": game["name"], "image": game["background_image"] or "", "released": game.get("released")}
            for game in data
        ]

    # Also load user's lists for the add menu in search page
    lists = db.execute("SELECT id, name FROM lists WHERE user_id = ?", session["user_id"])

    return render_template("search.html", results=results, lists=lists, page=page)


# --- Error Handle ---
@app.errorhandler(404)
def not_found(e):
    return error("Page not found", 404)


if __name__ == "__main__":
    app.run(debug=True)
