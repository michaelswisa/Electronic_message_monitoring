from kafka import KafkaConsumer
import json
from database import db_session, init_db
from explos_consumer.models import Email, Location, DeviceInfo, Sentence
from datetime import datetime


init_db()

consumer = KafkaConsumer(
    'messages.explos',
    bootstrap_servers=['kafka:9092'],
    auto_offset_reset='earliest',
    group_id='explos_group',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)


def save_to_postgres(data):
    session = db_session()
    try:
        email = Email(
            email=data['email'],
            username=data['username'],
            ip_address=data['ip_address'],
            created_at=datetime.fromisoformat(data['created_at'])
        )
        session.add(email)
        email = session.refresh(email)

        location = Location(
            latitude=data['location']['latitude'],
            longitude=data['location']['longitude'],
            city=data['location']['city'],
            country=data['location']['country'],
            email=email.id
        )
        session.add(location)

        device_info = DeviceInfo(
            browser=data['device_info']['browser'],
            os=data['device_info']['os'],
            device_id=data['device_info']['device_id'],
            email=email.id
        )
        session.add(device_info)

        for sentence in data['sentences']:
            session.add(Sentence(sentence=sentence, email=email.id))

        session.commit()
        print(f"Saved email from {data['email']} to PostgreSQL")

    except Exception as e:
        print(f"Error saving to PostgreSQL: {e}")
        session.rollback()
    finally:
        session.close()


for message in consumer:
    save_to_postgres(message.value)
