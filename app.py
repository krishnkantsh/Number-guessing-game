
from flask import Flask, render_template, request, session
import random
import os

app = Flask(__name__)
app.secret_key = os.environ.get(
    "FLASK_SECRET_KEY", "dev-only-change-this-key"
)


def new_game():
    session["secret_number"] = random.randint(1, 100)
    session["attempts"] = 0
    session["message"] = "Enter your first guess and test your luck!"
    session["message_icon"] = "🎯"
    session["message_type"] = "info"
    session["game_over"] = False
    session["won"] = False


@app.route("/", methods=["GET", "POST"])
def home():
    if "secret_number" not in session:
        new_game()

    if request.method == "POST":
        action = request.form.get("action", "")

        if action == "restart":
            new_game()

        elif not session["game_over"]:
            guess_text = request.form.get("guess", "").strip()

            try:
                guess = int(guess_text)

                if not 1 <= guess <= 100:
                    session["message"] = (
                        "Please enter a number between 1 and 100!"
                    )
                    session["message_icon"] = "⚠️"
                    session["message_type"] = "warning"

                else:
                    session["attempts"] += 1
                    secret = session["secret_number"]

                    if guess == secret:
                        session["message"] = (
                            f"Correct! You won in "
                            f"{session['attempts']} attempts!"
                        )
                        session["message_icon"] = "🏆"
                        session["message_type"] = "success"
                        session["game_over"] = True
                        session["won"] = True

                    elif guess < secret:
                        session["message"] = (
                            "Too LOW! Try a HIGHER number!"
                        )
                        session["message_icon"] = "⬆️"
                        session["message_type"] = "higher"

                    else:
                        session["message"] = (
                            "Too HIGH! Try a LOWER number!"
                        )
                        session["message_icon"] = "⬇️"
                        session["message_type"] = "lower"

            except ValueError:
                session["message"] = (
                    "Please enter a valid whole number!"
                )
                session["message_icon"] = "⚠️"
                session["message_type"] = "warning"

    return render_template(
        "index.html",
        attempts=session["attempts"],
        message=session["message"],
        message_icon=session["message_icon"],
        message_type=session["message_type"],
        game_over=session["game_over"],
        won=session["won"]
    )


if __name__ == "__main__":
    app.run(debug=True)
