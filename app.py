from flask import Flask, request, jsonify
import uuid
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return "Bonjour"


@app.route('/api/event/<string:solution>/<string:model>/<string:action>', methods=['POST'])
def create_event(solution, model, action):
    try:
        #recevoir les donnees json
        event_data = request.get_json()

        if not event_data:
            return jsonify({"message":"Invalid JSON"}), 400
        
        #generer un uid et un horodatage
        event_uid = str(uuid.uuid4())
        event_timestamp = datetime.utcnow().isoformat() + 'Z'

        #preparer la reponse
        response_message = {
            "event_uid" : event_uid,
            "event_timestamp" : event_timestamp,
            "event_data" : event_data
        }

        return jsonify(response_message), 200
    except Exception as e:
        return jsonify({"message" : str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)