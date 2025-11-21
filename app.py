from flask import Flask, render_template, request
import mbta_helper

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
        stop_name, wheelchair_accessible = mbta_helper.find_stop_near(place_name)
    except Exception as e:
        return render_template(
            "error.html",
            message=f"Something went wrong while searching: {e}",
        )

    return render_template(
        "mbta_station.html",
        place_name=place_name,
        stop_name=stop_name,
        wheelchair_accessible=wheelchair_accessible,
    )


if __name__ == "__main__":
    app.run(debug=True)
