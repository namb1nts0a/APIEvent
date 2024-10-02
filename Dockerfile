FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt

#installer les dependances
RUN pip install --no-cache-dir -r requirements.txt

#copier les reste du code dans la conteneur
COPY . .

#expose le port du flask
EXPOSE 5000

#lance l'api
CMD ["python", "app.py"]