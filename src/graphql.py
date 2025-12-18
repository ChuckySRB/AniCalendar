"""
    In this file you have helper functions for deffining GraphQL request strings for AniList API.
"""


def get_user_medialists_query(USER: str, type="ANIME") -> str:
    """
    Creates a GraphQL query for AniList API to fetch calendar data for a given user and type.
    """
    # Note: We use double curly braces {{ }} in f-strings where we want 
    # literal curly braces to appear in the final GraphQL string.
    return f"""
    query {{
      MediaListCollection(userName: "{USER}", type: {type}) {{
        lists {{
          name
          isCustomList
          entries {{
            media {{
              id
              title {{
                english
                romaji
              }}
              season
              seasonYear
              episodes
              airingSchedule(perPage: 25) {{
                nodes {{
                  airingAt
                  episode
                  timeUntilAiring
                }}
              }}
              startDate {{
                year
                month
                day
              }}
            }}
          }}
        }}
      }}
    }}
    """