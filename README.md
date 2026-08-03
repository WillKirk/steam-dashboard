# Steam Dashboard

A personal Steam stats dashboard built with Python and Flask, using the Steam Web API to display your gaming profile, library, playtime stats, and achievements.

**Live demo:** [steam-dashboard-wk.vercel.app](https://steam-dashboard-wk.vercel.app)

---

## Features

- **Profile** — displays your Steam avatar, username, and ID
- **Game Library** — full game library with cover art, playtime, and search/sort controls
- **Achievements** — per-game achievement list with unlock status and progress bar
- **Stats** — summary cards (total hours, games owned/played) and a top 10 playtime chart
- **Responsive** — mobile-friendly layout
- **Error handling** — graceful fallbacks if the Steam API is unavailable

---

## Tech Stack

- **Backend:** Python, Flask
- **API:** Steam Web API (REST)
- **Frontend:** Jinja2 templates, HTML, CSS, Chart.js
- **Deployment:** Vercel

---

## Getting Started

### Prerequisites

- Python 3.10+
- A [Steam API key](https://steamcommunity.com/dev/apikey)
- Your 64-bit Steam ID (find it at [steamidfinder.com](https://www.steamidfinder.com))

### Installation

1. **Clone the repo**
   ```bash
   git clone https://github.com/WillKirk/steam-dashboard.git
   cd steam-dashboard
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create a `.env` file** in the project root
   ```
   STEAM_API_KEY=your_api_key_here
   STEAM_ID=your_steam_id_here
   ```

5. **Run the app**
   ```bash
   python app.py
   ```

6. Visit `http://localhost:5000`

### Note

Your Steam profile must be set to **Public** (Steam → Privacy Settings → Game Details → Public) for the API to return data.

---

## Project Structure

```
steam-dashboard/
├── app.py               # Flask routes
├── steam_api.py         # Steam API calls
├── config.py            # Environment variable loading
├── templates/
│   ├── base.html
│   ├── index.html       # Profile + top games
│   ├── library.html     # Full game library
│   ├── game.html        # Per-game achievements
│   ├── stats.html       # Stats and charts
│   └── error.html
├── static/
│   └── css/style.css
└── requirements.txt
```

---

## Deployment

Deployed on Vercel with environment variables set via the Vercel dashboard. See `vercel.json` for configuration.
