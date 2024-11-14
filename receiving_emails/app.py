from flask import Flask, jsonify
from receiving_emails import bp_receiving_emails

app = Flask(__name__)

@app.route('/')
def hello_world():
    return jsonify({"status": "healthy"}), 200

app.register_blueprint(bp_receiving_emails, url_prefix='/api')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
