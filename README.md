
# API d'événements avec RabbitMQ et Docker

Ce projet est une API qui gère la création d'événements et publie ces événements dans une file RabbitMQ. L'application est développée avec Flask et avec les dependances necessaires, et est configurée pour s'exécuter à l'aide de Docker et Docker Compose.

## Fonctionnalités

- API de création d'événements
- Publication des événements dans une file RabbitMQ
- Stockage des événements dans une base de données SQLite
- Mécanisme de retry en cas de défaillance de RabbitMQ
- Services Dockerisés (API et RabbitMQ)
- Tests unitaires pour l'API

## Prérequis

- Docker
- Docker Compose

## Structure du projet

```
.
├── app.py                # Fichier principal de l'application
├── db.py                 # Configuration de la base de données
├── models.py             # Modèles SQLAlchemy
├── test_app.py           # Tests unitaires pour l'application
├── Dockerfile            # Fichier Docker pour l'API
├── docker-compose.yml    # Fichier Docker Compose
├── requirements.txt      # Dépendances Python
└── README.md             # Documentation du projet
```

## Démarrage rapide

### Cloner le dépôt

```bash
git clone https://github.com/namb1nts0a/APIEvent.git
cd APIEvent
git checkout backend
```

### Construire et exécuter l'application avec Docker Compose

Assurez-vous que Docker et Docker Compose sont installés. Ensuite, exécutez la commande suivante :

```bash
docker-compose up --build
```

Cela va construire le service API et télécharger l'image RabbitMQ. L'API sera accessible à l'adresse `http://localhost:5000`, et l'interface de gestion de RabbitMQ sera accessible à `http://localhost:15672`.

### Endpoints de l'API

#### Créer un événement

- **URL**: `/api/event/<string:solution>/<string:model>/<string:action>`
- **Méthode**: `POST`
- **Exemple de payload**:

```json
{
  "order_id": 12345,
  "customer": "John Doe",
  "total_amount": 250
}
```

- **Exemple de réponse**:

```json
{
  "event_uid": "2af8a276-e77a-4fd5-b11b-580e79a844d3",
  "event_timestamp": "2024-09-30T18:07:44.171754Z",
  "event_data": {
    "order_id": 12345,
    "customer": "John Doe",
    "total_amount": 250
  }
}
```

### Interface de gestion de RabbitMQ

Pour accéder à l'interface de gestion de RabbitMQ, ouvrez un navigateur et rendez-vous sur :

```
http://localhost:15672
```

Les identifiants par défaut sont :

- **Nom d'utilisateur**: guest
- **Mot de passe**: guest

### Exécuter les tests unitaires

Vous pouvez exécuter les tests unitaires avec la commande suivante :

```bash
python -m unittest test_app.py
```

### Mécanisme de retry

En cas d'échec lors de la publication dans RabbitMQ, l'application réessaiera jusqu'à 5 fois avec une stratégie de backoff exponentiel.

