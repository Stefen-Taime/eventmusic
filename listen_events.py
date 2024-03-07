import pandas as pd
import random
from datetime import datetime
import time
import ast

from faker import Faker
fake = Faker()
locales = ['en_US', 'en_CA', 'fr_FR', 'nl_BE', 'pt_BR']
Faker.seed(0)

def generate_location():
    locale = random.choice(locales)
    fake = Faker(locale)
    
    city = fake.city()
    state = ""
    zip_code = ""
    if locale == 'en_US':
        state = fake.state_abbr()
        zip_code = fake.zipcode()
    elif locale == 'en_CA':
        state = fake.province_abbr()
        zip_code = fake.postalcode_in_province()
    elif locale in ['fr_FR', 'nl_BE']:
        zip_code = fake.postcode()
    elif locale == 'pt_BR':
        state = fake.state_abbr()
        zip_code = f"{fake.postcode()}-{random.randint(100,999)}"
    
    return city, state, zip_code, locale.split('_')[1]

def generate_timestamp(year_start, year_end):
    start = datetime(year_start, 1, 1)
    end = datetime(year_end, 2, 28, 23, 59, 59)
    return int(time.mktime(start.timetuple()) + random.random() * (time.mktime(end.timetuple()) - time.mktime(start.timetuple())))

artists_with_duration_path = 'data/artiste_with_duration.csv'
artists_with_duration_df = pd.read_csv(artists_with_duration_path)

artists_with_duration_df['song'] = artists_with_duration_df['song'].apply(ast.literal_eval)

def generate_data_updated():
    artist_row = artists_with_duration_df.sample(1).iloc[0]
    artist_name = artist_row['name']
    
    song_info = random.choice(artist_row['song'])
    song_title = song_info['title']
    song_duration = song_info['duration']
    
    city, state, zip_code, country = generate_location()
    
    auth_status = random.choice(["Logged In", "Logged Out"])
    level = "free" if auth_status == "Logged Out" else random.choice(["free", "paid"])
    
    user_info = {
        "userId": None if auth_status == "Logged Out" else fake.random_int(min=1, max=100000),
        "lastName": None if auth_status == "Logged Out" else fake.last_name(),
        "firstName": None if auth_status == "Logged Out" else fake.first_name(),
        "gender": None if auth_status == "Logged Out" else random.choice(["M", "F"]),
        "registration": None if auth_status == "Logged Out" else generate_timestamp(2024, 2024)
    }
    
    return {
        "artist": artist_name,
        "song": song_title,
        "duration": song_duration,
        "ts": generate_timestamp(2024, 2024),
        "sessionid": fake.random_int(min=1, max=10000),
        "auth": auth_status,
        "level": level,
        "itemInSession": fake.random_int(min=1, max=100),
        "city": city,
        "zip": zip_code if auth_status == "Logged In" else None,
        "state": state,
        "country": country,
        "userAgent": fake.user_agent(),
        "lon": fake.longitude(),
        "lat": fake.latitude(),
        **user_info
    }

updated_data = [generate_data_updated() for _ in range(10000)]
updated_df = pd.DataFrame(updated_data)

csv_file_path = "listen_events.csv"
updated_df.to_csv(csv_file_path, index=False)
