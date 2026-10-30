# What to watch

Flask front page with a **Trending now** page (today / this week).
Data comes from TVmaze (https://www.tvmaze.com). No account or API key needed.

## Project structure
```
tv-shows/
├── app.py                  # entry point: routes only
├── config.py               # loads settings from .env
├── .env                    # your settings (not committed)
├── .env.example            # template for .env
├── requirements.txt
├── services/
│   └── tvmaze.py           # TVmaze API calls and trending logic
├── templates/
│   ├── base.html           # page shell (head, footer, script/css links)
│   ├── index.html          # front page
│   └── partials/
│       └── card.html       # one show card (macro)
└── static/
    ├── css/style.css
    └── js/main.js          # trending row arrows
```

## Run
```
python -m venv .venv
.venv\Scripts\activate          # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python app.py
```
Open http://127.0.0.1:5000

## Settings (.env)
| Variable | Default | Meaning |
|---|---|---|
| `TVMAZE_COUNTRY` | `US` | Country whose TV schedule counts as "airing" (`ES`, `GB`, ...) |
| `SHOW_COUNT` | `20` | Number of trending shows |
| `FLASK_DEBUG` | `1` | `0` to turn debug mode off |
| `HOST` / `PORT` | `127.0.0.1` / `5000` | Server address |

## How it works
- **Trending now**: the most popular shows (TVmaze popularity score) airing on TV or streaming today or in the last 7 days. TVmaze has no real "trending" feed, so this is the closest equivalent. Refreshed hourly.
