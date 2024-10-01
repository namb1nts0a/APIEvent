from flask import Flask, request, jsonify
import uuid
from datetime import datetime
from sqlalchemy.orm import Session
from db import engine, get_db
from models import Event
from db import Base
from rabbitmq import publish_to_rabbitmq
import json


#creation du tables dans le db au demarrage
Base.metadata.create_all(bind=engine)


app = Flask(__name__)

@app.route('/')
def home():
    return "Bonjour"


@app.route('/api/event/<string:solution>/<string:model>/<string:action>', methods=['POST'])
def create_event(solution, model, action):
    db = next(get_db()) #obtenir une session
    try:
        #recevoir les donnees json
        try:
            event_data = request.get_json()
        except Exception:
            return jsonify({"message": "Invalid JSON"}), 400

        if not event_data:
            return jsonify({"message": "No data provided"}), 400
        
        #generer un uid et un horodatage
        event_uid = str(uuid.uuid4())
        event_timestamp = datetime.utcnow()

        #cree un nouvel Event
        new_event = Event(
            event_uid = event_uid,
            event_timestamp = event_timestamp,
            event_data = json.dumps(event_data)
        )

        #enregistrement dans la base de donnee
        db.add(new_event)
        db.commit()

        #preparer la reponse
        response_message = {
            "event_uid" : event_uid,
            "event_timestamp" : event_timestamp.isoformat() + 'Z', #on formate le type
            "event_data" : event_data
        }

        queue_name = f"{solution}/{model}/{action}"

        #publier le message dans rabbitmq
        publish_to_rabbitmq(queue_name, json.dumps(response_message))

        return jsonify({"message" : f"Event published to queue {queue_name}", "status" : "success"}), 200
    except Exception as e:
        db.rollback() # s'il y a erreur on annule la transaction
        return jsonify({"message" : str(e)}), 500
    
    finally:
        db.close()


if __name__ == "__main__":
    app.run(debug=True)