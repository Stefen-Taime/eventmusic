import pandas as pd
from faker import Faker
import random

fake = Faker()

# Pages accessibles pour tous les utilisateurs
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

# Pages accessibles uniquement pour les utilisateurs "Logged Out"
logged_out_pages = [
    "/explore",
    "/new-releases",
    "/songs",
]

def generate_page_view_data_from_csv(row):
    # Sélectionner les pages en fonction du statut d'authentification
    available_pages = logged_out_pages if row["auth"] == "Logged Out" else music_app_pages
    page = random.choice(available_pages)

    return {
        "ts": row["ts"],
        "sessionId": row["sessionid"],
        "page": page,  
        "auth": row["auth"],
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
page_view_df_from_csv.head(10000).to_csv(csv_file_path, index=False)
