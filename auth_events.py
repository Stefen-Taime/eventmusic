import pandas as pd
from faker import Faker
import random

fake = Faker()

page_view_events_df = pd.read_csv("page_view_events.csv")

def generate_auth_data_from_page_view(row):
    return {
        "ts": row["ts"],
        "sessionId": row["sessionId"],
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
        "success": fake.boolean()  
    }

auth_data_from_page_view = [generate_auth_data_from_page_view(row) for index, row in page_view_events_df.iterrows()]

auth_df_from_page_view = pd.DataFrame(auth_data_from_page_view)

csv_file_path_auth_events = "auth_events.csv"
auth_df_from_page_view.to_csv(csv_file_path_auth_events, index=False)


