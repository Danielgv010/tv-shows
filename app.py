"""Entry point: routes only. Settings live in config.py / .env, data access in services/."""
import requests
from flask import Flask, render_template, request

import config
from services import tvmaze

app = Flask(__name__)


@app.route("/")
def index():
    window = request.args.get("window", "week")
    if window not in ("day", "week"):
        window = "week"

    try:
        trending, trending_error = tvmaze.get_trending(window), False
    except requests.RequestException:
        trending, trending_error = [], True

    return render_template(
        "index.html",
        window=window,
        trending=trending,
        trending_error=trending_error,
    )


if __name__ == "__main__":
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)
