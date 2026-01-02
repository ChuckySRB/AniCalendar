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
