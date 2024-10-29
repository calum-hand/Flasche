from flask import Blueprint, render_template, request, jsonify

from flasche.db.data import load_vocabulary


bp = Blueprint("metrics", __name__, url_prefix="/metrics")


@bp.route("/")
def metrics():
    return render_template("metrics.html")


@bp.route("/generate_stats", methods=["POST"])
def generate_stats():
    group_by = request.form.get("group_by")
    value_col = request.form.get("value_col")

    stats = (
        load_vocabulary()
        .groupby(group_by)[value_col]
        .count()
        .reset_index()
        .rename(columns={value_col: "Count"})
    )

    return jsonify(stats.to_dict(orient="records"))
