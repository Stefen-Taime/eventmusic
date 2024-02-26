import csv
import json
import threading
import time
import uuid

from confluent_kafka import Producer

producer = Producer({'bootstrap.servers': 'localhost:9092'})

topics = ['listen_events', 'page_view_events', 'auth_events']

def send_csv_data(topic, filename):
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        batch_size = 5  
        batch = []  

        for row in reader:
            key = str(uuid.uuid4())
            data = json.dumps(row)
            batch.append((key, data))

            if len(batch) >= batch_size:
                for key, data in batch:
                   
                    producer.produce(topic, key=key, value=data)
                producer.flush()  
                batch = []  
                time.sleep(30) 

        
        if batch:
            for key, data in batch:
                producer.produce(topic, key=key, value=data)
            producer.flush()

threads = []
for topic, filename in zip(topics, ['listen_events.csv', 'page_view_events.csv', 'auth_events.csv']):
    thread = threading.Thread(target=send_csv_data, args=(topic, filename))
    threads.append(thread)

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()

producer.flush()
