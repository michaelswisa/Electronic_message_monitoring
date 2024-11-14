from flask import Blueprint, request, jsonify
from services import send_email_to_kafka

bp_receiving_emails = Blueprint('receiving_emails', __name__)




@bp_receiving_emails.route('/email', methods=['GET', 'POST'])
def receiving_emails():
    email = request.get_json()
    print(email)
    send_email_to_kafka(email)

    return jsonify({"status": "success"}), 200
