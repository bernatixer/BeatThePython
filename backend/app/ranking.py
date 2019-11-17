from flask import Blueprint, current_app, request, url_for, redirect, jsonify
from werkzeug.security import check_password_hash

from app.db import get_db


bp = Blueprint("ranking", __name__, url_prefix="/ranking")


@bp.route("/", methods=("GET", "POST"))
def ranking():
    db = get_db()

    if request.method == "POST":
        username = request.form["username"]
        score = request.form["score"]
        error = None

        if not username:
            error = "Username is required"
            current_app.logger.error(f"{error} || {username}")
        elif not score:
            error = "Score is required"
            current_app.logger.error(f"{error} || {username}")
        elif (
            db.execute(
                "SELECT id FROM ranking WHERE username = ?", (username,)
            ).fetchone()
            is not None
        ):
            db.execute(
                "UPDATE ranking SET score = ? WHERE username = ?", (score, username)
            )
            db.commit()
            current_app.logger.info(f"Updated {username}'s score!")
            # return redirect(url_for("ranking.ranking"))
            return dict(ranking=db.execute("SELECT * FROM ranking ORDER BY SCORE DESC").fetchall())
        else:
            db.execute(
                "INSERT INTO ranking (username, score) VALUES (?, ?)", (username, score)
            )
            db.commit()
            current_app.logger.info(f"Inserted {username} into ranking!")
            # return redirect(url_for("ranking.ranking"))
            return dict(ranking=db.execute("SELECT * FROM ranking ORDER BY SCORE DESC").fetchall())

    return dict(ranking=db.execute("SELECT * FROM ranking ORDER BY SCORE DESC").fetchall())
