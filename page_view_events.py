import pandas as pd
from faker import Faker
import random

fake = Faker()

music_app_pages = [
    "/explore",
    "/discover",
    "/new-releases",
    "/playlists",
    "/my-music",
    "/charts",
    "/artists",
    "/albums",
    "/songs",
]

def generate_page_view_data_from_csv(row):
    return {
        "ts": row["ts"],
        "sessionId": row["sessionid"],
        "page": random.choice(music_app_pages),  
        "auth": row["auth"],
        "method": random.choice(["GET", "POST"]),
        "status": random.choice([200, 404, 500]),
        "level": row["level"],
        "itemInSession": row["itemInSession"],
        "city": row["city"],
        "zip": row["zip"],
        "state": row["state"],
        "userAgent": row["userAgent"],
        "lon": row["lon"],
        "lat": row["lat"],
        "userId": row["userId"],
        "lastName": row["lastName"],
        "firstName": row["firstName"],
        "gender": row["gender"],
        "registration": row["registration"],
        "artist": row["artist"],
        "song": row["song"],
        "duration": row["duration"]
    }

listen_events_df = pd.read_csv("listen_events.csv")

page_view_data_from_csv = [generate_page_view_data_from_csv(row) for index, row in listen_events_df.iterrows()]

page_view_df_from_csv = pd.DataFrame(page_view_data_from_csv)

csv_file_path = "page_view_events.csv"  
page_view_df_from_csv.head(1000).to_csv(csv_file_path, index=False)
