from flask import Blueprint, render_template, request, redirect, url_for
import pandas as pd

from flasche.db.data import load_vocabulary

bp = Blueprint("quiz", __name__, url_prefix="/quiz")

SESSION = {}


@bp.route("/", methods=["GET", "POST"])
def quiz():
    if request.method == "POST":
        vocab_types = request.form.getlist("vocab_type")
        vocab_levels = request.form.getlist("vocab_level")
        word_count = int(request.form.get("word_count", 10))
        translation_direction = request.form.get("translation_direction")

        column_maping = {
            "English": (
                "Question" if translation_direction == "english_to_german" else "Answer"
            ),
            "German": (
                "Answer" if translation_direction == "english_to_german" else "Question"
            ),
        }

        df = load_vocabulary()

        if "All" not in vocab_types:
            df = df[df["Type"].isin(vocab_types)]

        if "All" not in vocab_levels:
            df = df[df["Level"].isin(vocab_levels)]

        # sample with replacement if df to small to prevent errors in niche request
        df = df.sample(n=word_count, replace=word_count < len(df))
        df = df.rename(columns=column_maping)

        # Save the filtered DataFrame to a session for persistence
        SESSION["quiz_data"] = df.to_dict(
            orient="records"
        )  # Save as list of dictionaries
        return redirect(url_for("quiz.question"))

    return render_template("quiz/setup.html")


@bp.route("/question", methods=["GET", "POST"])
def question():
    quiz_data = SESSION.get("quiz_data", [])

    if request.method == "POST":
        # Retrieve user answers from form submission
        user_answers = request.form.getlist("answer")
        # Retrieve the original questions from the session data
        quiz_data_df = pd.DataFrame(quiz_data)

        # Compare answers
        quiz_data_df["User Answer"] = user_answers
        quiz_data_df["Correct"] = quiz_data_df["User Answer"] == quiz_data_df["Answer"]

        # Pass results to the results page
        results = quiz_data_df.to_dict(orient="records")
        return render_template("quiz/results.html", results=results)

    return render_template("quiz/question.html", quiz_data=quiz_data)
