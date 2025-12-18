

class AiringListData:
    MEDIA_LIST_STATUS = [
        "CURRENT",
        "PLANNING",
        "COMPLETED",
        "DROPPED",
        "PAUSED",
        "REPEATING",
    ]

    airing_anilist = []

    season = ""
    year = 2026

    def __init__(self, data, SEASON: str, YEAR: int):
        self.season = SEASON
        self.year = YEAR
        # Go through each list in the MediaListCollection
        # Here there are standard lists like "Watching", "Completed", etc.
        # And also any custom lists the user may have created.
        # I have created custom lists for each season to easily filter seasonal anime I will watch.
        for list in data["data"]["MediaListCollection"]["lists"]:
            list_name = list["name"]
            if list_name.capitalize() == SEASON.capitalize(): # Match the custom list for the season
                for entry in list["entries"]:
                    media = entry["media"]
                    if media["season"].upper() == SEASON.upper() and media["seasonYear"] == YEAR: # Match season and year
                        self.airing_anilist.append(media.copy())  # Store the media info

    
