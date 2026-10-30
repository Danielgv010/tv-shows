"""TVmaze data access: trending shows (from TV schedules)."""
import html
import logging
import re
import time
from datetime import date, timedelta

import requests

import config

log = logging.getLogger(__name__)

API = "https://api.tvmaze.com"
EXCLUDED_TYPES = {"News", "Talk Show", "Sports"}  # keeps daily talk/news shows out of "trending"

session = requests.Session()
session.headers["User-Agent"] = "what-to-watch/1.0 (personal project)"


def get_json(path, **params):
    """GET from TVmaze. Returns None on 404 and retries when rate limited."""
    for _ in range(4):
        resp = session.get(f"{API}{path}", params=params, timeout=15)
        if resp.status_code == 429:
            time.sleep(5)
            continue
        if resp.status_code == 404:
            return None
        resp.raise_for_status()
        return resp.json()
    raise requests.RequestException("TVmaze rate limit hit")


def _https(url):
    return url.replace("http://", "https://") if url else None


def _clean(text):
    """TVmaze summaries contain HTML tags; keep plain text."""
    return html.unescape(re.sub(r"<[^>]+>", "", text or "")).strip()


def shape(show):
    """Reduce a TVmaze show to what the templates need."""
    images = show.get("image") or {}
    channel = show.get("network") or show.get("webChannel") or {}
    return {
        "id": show["id"],
        "name": show.get("name", "Untitled"),
        "year": (show.get("premiered") or "")[:4],
        "rating": (show.get("rating") or {}).get("average"),
        "poster": _https(images.get("medium")),
        "poster_large": _https(images.get("original")),
        "summary": _clean(show.get("summary")),
        "genres": show.get("genres") or [],
        "network": channel.get("name"),
        "url": show.get("url"),
        "weight": show.get("weight") or 0,
        "type": show.get("type"),
    }


# ---------- Trending: popular shows airing today / in the last 7 days ----------
_trending_cache = {}


def get_trending(window):
    hit = _trending_cache.get(window)
    if hit and time.time() - hit[0] < config.TRENDING_TTL:
        return hit[1]

    found = {}
    for i in range(1 if window == "day" else 7):
        day = (date.today() - timedelta(days=i)).isoformat()
        for ep in get_json("/schedule/web", date=day) or []:  # streaming
            show = (ep.get("_embedded") or {}).get("show")
            if show:
                found[show["id"]] = shape(show)
        for ep in get_json("/schedule", country=config.COUNTRY, date=day) or []:  # broadcast TV
            show = ep.get("show")
            if show:
                found[show["id"]] = shape(show)

    shows = [s for s in found.values() if s["type"] not in EXCLUDED_TYPES]
    shows.sort(key=lambda s: s["weight"], reverse=True)
    shows = shows[: config.SHOW_COUNT]
    _trending_cache[window] = (time.time(), shows)
    return shows
