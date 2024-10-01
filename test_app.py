import unittest
from app import app
from db import Base, engine, get_db
from models import Event
import json
from unittest.mock import patch

class EventAPITestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        #cree la base de donnee de test
        Base.metadata.create_all(bind=engine)


    @classmethod
    def tearDownClass(cls):
        #supprimer la base de donnees apres la test
        Base.metadata.drop_all(bind=engine)


    def setUp(self):
        #initialise l'applicatione et le client du test
        self.app = app.test_client()
        self.app.testing = True
        self.db = next(get_db())

    def tearDown(self):
        #nettoyer la base de donnees apres chaque test
        self.db.query(Event).delete()
        self.db.commit()
        self.db.close()

    def test_create_event_success(self):
        #test si un evenement est cree
        event_data = {
            "order_id" : 12345,
            "customer" : "John Doe",
            "total_amount" : 250
        }

        response = self.app.post('/api/event/ecommerce/order/create', json=event_data)

        #verifier que la requete a bien reussie
        self.assertEqual(response.status_code, 200)

        #verifier que l'event est cree dans la base de donnee
        event = self.db.query(Event).first()
        self.assertIsNotNone(event)
        self.assertEqual(json.loads(event.event_data), event_data)


    def test_create_event_invalid_json(self):
        #test pour la validation de json 
        response = self.app.post('/api/event/ecommerce/order/create', data="invalid json")

        #verification pour la statut 400 est pour la json invalid
        self.assertEqual(response.status_code, 400)

    def test_create_event_db_failure(self):
        #teste la gestion d'erreurs lors de l'enregistrement
        with patch('sqlalchemy.orm.Session.commit', side_effect=Exception("Database error")):
            #simuler un echec d'insertion dans la db
            # self.db.close()
            event_data = {
                "order_id": 12345,
                "customer": "John Doe",
                "total_amount": 250
            }
            
            response = self.app.post('/api/event/ecommerce/order/create', json=event_data)

            #verifier l'erreur 500
            self.assertEqual(response.status_code, 500)


if __name__ == "__main__":
    unittest.main()