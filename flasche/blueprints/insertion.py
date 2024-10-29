from flask import Blueprint, render_template, request, redirect, url_for
import pandas as pd

from flasche.conjugations import collect_verb_conjugations
from flasche.db.insertion import insert_general, insert_nouns, insert_verbs


bp = Blueprint("insert", __name__, url_prefix="/insert")


@bp.route("/")
def insertion():
    return render_template("insert/insertion.html")


@bp.route("/<string:vocab_type>", methods=["GET", "POST"])
def insert_vocabulary(vocab_type: str):

    if request.method == "GET":
        return render_template(f"{request.path}.html")

    # Extract general vocabulary and insert
    df = pd.DataFrame(
        {
            field.title(): request.form.getlist(f"{field}[]")
            for field in ["english", "german", "type", "level"]
        }
    )
    insert_general(df)

    if vocab_type == "noun":
        df["Gender"] = request.form.getlist(f"gender[]")
        df["Plural"] = request.form.getlist(f"plural[]")
        insert_nouns(df[["English", "Gender", "German", "Plural"]])

    elif vocab_type == "verb":
        frames = []

        for english, infinitive in zip(df["English"], df["German"]):
            verb_table = collect_verb_conjugations(infinitive)
            verb_table["English"] = english
            frames.append(verb_table)

        insert_verbs(
            pd.concat(frames)[
                ["English", "Infinitive", "Tense", "Pronoun", "Conjugation"]
            ]
        )

    return redirect(url_for("insert.insertion"))
