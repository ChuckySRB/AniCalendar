import requests
from src.graphql import get_user_medialists_query

ANILIST_URL = 'https://graphql.anilist.co'

def get_user_medialist(USER: str):
    query = get_user_medialists_query(USER)
    response = requests.post(ANILIST_URL, json={'query': query})
    data = response.json()
    return data



