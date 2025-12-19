from src.api import add_airing_anime_to_calendar
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add airing anime to calendar.")
    parser.add_argument("-u", "--user", required=True, help="AniList username")
    parser.add_argument("-s", "--season", required=True, help="Season to fetch (e.g., Winter, Spring, Summer, Fall)")
    parser.add_argument("-y", "--year", type=int, required=True, help="Year to fetch")

    args = parser.parse_args()

    add_airing_anime_to_calendar(args.user, args.season, args.year)

