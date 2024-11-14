from kafka import KafkaConsumer
import json
from pymongo import MongoClient

# MongoDB setup
client = MongoClient('mongodb://mongodb:27017/')
db = client['all_messages']
collection = db['all_messages']

# Kafka consumer setup
consumer = KafkaConsumer(
    'messages.all',
    bootstrap_servers=['kafka:9092'],
    auto_offset_reset='earliest',
    group_id='messages.all_groups',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

for message in consumer:
    transaction = message.value
    collection.insert_one(transaction)
    print(f"Stored high-value transaction: {transaction}")


