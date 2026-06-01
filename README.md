# 📅 AniCalendar

**AniCalendar** is a Python-based automation tool that bridges the gap between your **AniList** seasonal plans and your **Google Calendar**. No excuses to miss an episode!

---

## ✨ Features

* **Smart Sync:** Automatically fetches anime from your custom seasonal lists (e.g., "Winter", "Spring").
* **Precision Scheduling:** Sets events **30 minutes after** the Japanese air time so you have time to find a stream.
* **Intelligent Updates:** If a show only has a "Date" but no "Time," the script adds a placeholder. If you run it again later when the time is confirmed, it **updates the existing event** instead of duplicating it.
* **Recurrence Built-in:** Schedules the entire season (default 12 episodes) in one go using Google Calendar's `RRULE`.
* **Duplicate Prevention:** Uses AniList IDs to ensure your calendar stays clean.

## 🚀 Getting Started

### 1. Prerequisites

* A Google Cloud Project with the **Google Calendar API** enabled.
* An AniList account with custom lists named after the seasons.

### 2. Installation

```bash
# Clone the repository
git clone https://github.com/ChuckySRB/AniCalendar.git
cd AniCalendar

# Install dependencies
pip install -r requirements.txt

```

### 3. Setup Credentials

1. Download your `credentials.json` from the [Google Cloud Console](https://console.cloud.google.com/).
2. Place it in the root directory of this project.

### 4. Usage

Run the script using the following arguments:

```cmd
python run.py -u YourUsername -s Season -y Year
# My Commands 
python run.py -u ChuckySRB -s Winter -y 2026
python run.py -u ChuckySRB -s Spring -y 2026
python run.py -u ChuckySRB -s Summer -y 2026
python run.py -u ChuckySRB -s Fall -y 2026

```

### 5. Dashboard Page (AniList Catch-up View)

The dashboard is served by a small [Bun](https://bun.sh) HTTP server so it can run on your LAN and share streaming links across every device.

Default values:
- User: `ChuckySRB`
- Season: current season
- Year: current year

Features:
- Weekly schedule view (Monday-first, previous/next week arrows)
- Current week loaded by default with current day highlighted
- Left catch-up list sorted by how many aired episodes you are behind
- Color severity for backlog (`5+` red, `3-4` orange, `2` yellow, `1` white, `0` green)
- Streaming-link modal on anime card click, persisted to `streaming_links.json` on the server
- Dedicated **Edit Links** page (`/links`) for live-editing the JSON file in the browser
- PWA: installable on phones, tablets, and desktops with offline shell caching

#### Run the dashboard server

```bash
# One-time: install Bun (Linux/macOS)
curl -fsSL https://bun.sh/install | bash

# Start the server (binds 0.0.0.0:7843 by default)
bun run server.js
```

Then open:
- `http://<server-ip>:7843/` — dashboard
- `http://<server-ip>:7843/links` — streaming-links JSON editor

Override host/port with env vars when needed:

```bash
ANICALENDAR_PORT=8080 ANICALENDAR_HOST=0.0.0.0 bun run server.js
```

#### Streaming links file

Links are stored next to the HTML in `streaming_links.json` (gitignored). The server creates an empty `{}` on first launch. Schema:

```json
{
  "21519": {
    "title": "Frieren: Beyond Journey's End",
    "url": "https://your-stream/series/frieren"
  }
}
```

- Keys are AniList media IDs (the dashboard's modal fills these in automatically when you add a link).
- Use `/links` in the browser to view, edit, format, and save the whole file.
- Copy the file to back it up or share your link set with a friend.

See `streaming_links.example.json` for a starter you can rename to `streaming_links.json`.

#### Install as a PWA

With the server running:
1. Open `http://<server-ip>:7843/` on your phone, tablet, or laptop.
2. Use the browser's **Install app** / **Add to Home Screen** option.
3. Launch from the home screen; it runs full-screen and works offline for previously-loaded screens (live AniList data still requires network).

---

## 🛠 Command Line Arguments

| Argument | Description | Example |
| --- | --- | --- |
| `-u`, `--user` | Your AniList Username | `ChuckySRB` |
| `-s`, `--season` | The season list to sync | `Winter` |
| `-y`, `--year` | The year of the season | `2026` |

---

## 📜 License

Distributed under the **MIT License**. See `LICENSE` for more information.
