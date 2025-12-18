import requests
from src.graphql import get_user_medialists_query
from src.google import add_anime_event, get_calendar_service
from src.data import AiringListData
from datetime import datetime

ANILIST_URL = 'https://graphql.anilist.co'

def get_user_medialist(USER: str):
    query = get_user_medialists_query(USER)
    response = requests.post(ANILIST_URL, json={'query': query})
    data = response.json()
    return data


def add_airing_anime_to_calendar(USER: str, SEASON: str, YEAR: int):
    calendar_service = get_calendar_service()
    data = get_user_medialist(USER)
    airinglist_data = AiringListData(data, SEASON, YEAR)
    for media in airinglist_data.airing_anilist:
        
        title = media["title"]["english"] or media["title"]["romaji"]
        anilist_id = media["id"]
        schedule = media["airingSchedule"]["nodes"]
        start_timestamp = schedule[0]["airingAt"] if schedule else int(datetime(media["startDate"]["year"], media["startDate"]["month"], media["startDate"]["day"], 19, 0).timestamp())
        have_airing_time =  "true" if schedule and schedule[0]["airingAt"] else "false"
        total_episodes = media["episodes"] or (schedule[-1]["episode"] if schedule else None) or 12  # Default to 12 if unknown

        add_anime_event(
            calendar_service,
            anime_title=title,
            start_timestamp=start_timestamp,
            total_episodes=total_episodes,
            anilist_id=anilist_id,
            have_airing_time=have_airing_time
        )