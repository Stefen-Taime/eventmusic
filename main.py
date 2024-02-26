import csv
import threading
import time
import uuid
from confluent_kafka import SerializingProducer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.serialization import StringSerializer

schema_registry_url = 'http://localhost:8081'
schema_registry_client = SchemaRegistryClient({'url': schema_registry_url})

def load_avro_serializer_from_file(schema_file):
    with open(schema_file) as f:
        schema_str = f.read()
    return AvroSerializer(schema_str=schema_str, schema_registry_client=schema_registry_client)

page_view_key_serializer = StringSerializer('utf_8')
page_view_value_serializer = load_avro_serializer_from_file('page_view_eventsVALUE.avsc')

listen_events_key_serializer = StringSerializer('utf_8')
listen_events_value_serializer = load_avro_serializer_from_file('listen_eventsVALUE.avsc')

auth_events_key_serializer = StringSerializer('utf_8')
auth_events_value_serializer = load_avro_serializer_from_file('auth_eventsVALUE.avsc')

def send_csv_data_avro(topic, filename, key_serializer, value_serializer):
    producer_config = {
        'bootstrap.servers': 'localhost:9092',
        'key.serializer': key_serializer,
        'value.serializer': value_serializer,
    }
    producer = SerializingProducer(producer_config)

    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        batch_size = 5  
        batch = []  

        for row in reader:
            key = str(uuid.uuid4()) if topic == 'page_view_events' else row.get('sessionid', str(uuid.uuid4()))
            data = {
                k: str(v) if k in ['sessionId', 'itemInSession', 'registration', 'page', 'auth', 'method', 'status', 'level', 'city', 'zip', 'state', 'userAgent', 'lon', 'lat', 'userId', 'lastName', 'firstName', 'gender', 'artist', 'song', 'duration'] else int(v) if k == 'ts' else v
                for k, v in row.items()
            }
            batch.append((key, data))

            if len(batch) >= batch_size:
                for key, data in batch:
                    producer.produce(topic=topic, key=key, value=data, on_delivery=delivery_report)
                producer.flush()
                batch = []
                time.sleep(30)

        if batch:
            for key, data in batch:
                producer.produce(topic=topic, key=key, value=data, on_delivery=delivery_report)
            producer.flush()

def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

def run_producer_for_page_view_events():
    send_csv_data_avro('page_view_events', 'page_view_events.csv',  page_view_key_serializer, page_view_value_serializer)

def run_producer_for_listen_events():
    send_csv_data_avro('listen_events', 'listen_events.csv', listen_events_key_serializer, listen_events_value_serializer)

def run_producer_for_auth_events():
    send_csv_data_avro('auth_events', 'auth_events.csv', auth_events_key_serializer, auth_events_value_serializer)    

page_view_thread = threading.Thread(target=run_producer_for_page_view_events)
listen_events_thread = threading.Thread(target=run_producer_for_listen_events)
auth_events_thread = threading.Thread(target=run_producer_for_auth_events)

page_view_thread.start()
listen_events_thread.start()
auth_events_thread.start()

page_view_thread.join()
listen_events_thread.join()
auth_events_thread.join()
