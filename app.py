from flask import Flask, render_template, request
import mbta_helper
from datetime import datetime


app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/nearest_mbta", methods=["POST"])
def nearest_mbta():
    place_name = request.form.get("place_name", "").strip()

    if not place_name:
        return render_template(
            "error.html",
            message="You must enter a place name or address.",
        )

    try:
        stop_name, wheelchair_accessible, next_train = mbta_helper.find_stop_near(place_name)
    except Exception as e:
        return render_template(
            "error.html",
            message=f"Something went wrong while searching: {e}",
        )

    next_train = format_time(next_train) # Convert from ISO to pretty time

    return render_template(
        "mbta_station.html",
        place_name=place_name,
        stop_name=stop_name,
        wheelchair_accessible=wheelchair_accessible,
        next_train=next_train
    )

def format_time(iso_string):
    if not iso_string:
        return None

    dt = datetime.fromisoformat(iso_string)
    return dt.strftime("%-I:%M %p")

if __name__ == "__main__":
    app.run(debug=True)
