from functools import wraps
from flask import session, redirect, url_for, flash, render_template

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            flash("You need to be logged in to access this content.", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

def error(message, code=400):
    """Renders an error message in a HTML page."""
    return render_template("error.html", message=message, code=code), code