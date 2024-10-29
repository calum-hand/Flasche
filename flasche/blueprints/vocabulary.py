from flask import Blueprint, render_template, request, jsonify

from flasche.db.data import load_vocabulary


bp = Blueprint("vocabulary", __name__, url_prefix="/vocabulary")


@bp.route("/")
def vocabulary():
    return render_template("vocabulary.html")


@bp.route("/filter_vocab_data", methods=["GET"])
def filter_vocab_data():
    # Get filter parameters from request
    word_type = request.args.get("word_type", "All")
    level = request.args.get("level", "All")

    # Filter DataFrame based on selection
    filtered_df = load_vocabulary()

    if word_type != "All":
        filtered_df = filtered_df[filtered_df["Type"] == word_type]

    if level != "All":
        filtered_df = filtered_df[filtered_df["Level"] == level]

    # Convert filtered DataFrame to dictionary and send as JSON
    data = filtered_df.to_dict(orient="records")
    return jsonify(data)
