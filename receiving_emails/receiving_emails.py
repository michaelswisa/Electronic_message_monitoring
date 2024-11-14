from flask import Blueprint, request, jsonify
from kafka import KafkaProducer
import json

bp_receiving_emails = Blueprint('receiving_emails', __name__)

producer = KafkaProducer(
    bootstrap_servers=['kafka:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)


@bp_receiving_emails.route('/email', methods=['POST'])
def receiving_emails():
    email = request.get_json()
    producer.send('messages.all', value=email)

    return jsonify({"status": "success"}), 200
