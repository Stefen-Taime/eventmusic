import pandas as pd
from faker import Faker
import random
import ast

fake = Faker()
locales = ['en_US', 'en_CA', 'fr_FR', 'nl_BE', 'pt_BR']
Faker.seed(0)  

def generate_location():
    locale = random.choice(locales)
    fake = Faker(locale)
    
    if locale == 'en_US':
        city = fake.city()
        state = fake.state_abbr()
        zip_code = fake.zipcode()
    elif locale == 'en_CA':
        city = fake.city()
        state = fake.province_abbr()
        zip_code = fake.postalcode_in_province()
    elif locale in ['fr_FR', 'nl_BE']:
        city = fake.city()
        state = ""  
        zip_code = fake.postcode()
    elif locale == 'pt_BR':
        city = fake.city()
        state = fake.state_abbr()
        zip_code = f"{fake.postcode()}-{random.randint(100,999)}"
    
    return city, state, zip_code, locale.split('_')[1]

file_path = 'data/artist.csv'  
artists_df = pd.read_csv(file_path)

artists_df['song'] = artists_df['song'].apply(ast.literal_eval)

def generate_data_updated():
    artist_row = artists_df.sample(1).iloc[0]
    artist_name = artist_row['name']
    songs = artist_row['song']
    song_title = random.choice(songs)
    
    city, state, zip_code, country = generate_location()
    
    return {
        "artist": artist_name,
        "song": song_title,
        "duration": random.uniform(180, 600), 
        "ts": fake.unix_time(),
        "sessionid": fake.random_int(min=1, max=10000),
        "auth": random.choice(["Logged In", "Logged Out"]),
        "level": random.choice(["free", "paid"]),
        "itemInSession": fake.random_int(min=1, max=100),
        "city": city,
        "zip": zip_code,
        "state": state,
        "country": country,  
        "userAgent": fake.user_agent(),
        "lon": fake.longitude(),
        "lat": fake.latitude(),
        "userId": fake.random_int(min=1, max=100000),
        "lastName": fake.last_name(),
        "firstName": fake.first_name(),
        "gender": random.choice(["M", "F"]),
        "registration": fake.unix_time()
    }

updated_data = [generate_data_updated() for _ in range(1000)]
updated_df = pd.DataFrame(updated_data)

csv_file_path = "listen_events.csv"
updated_df.to_csv(csv_file_path, index=False)


