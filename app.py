from flask import Flask, render_template, jsonify, Response

from monitor import get_system_metrics
from camera import generate_frames

app = Flask(__name__)


@app.route("/")
def home():
    metrics = get_system_metrics()
    return render_template("index.html", metrics=metrics)


@app.route("/api/metrics")
def metrics_api():
    return jsonify(get_system_metrics())


@app.route("/video_feed")
def video_feed():
    return Response(
        generate_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True,
        use_reloader=False
    )
