import pika
from tenacity import retry, stop_after_attempt, wait_fixed


# Stratégie de retry : arrêter après 5 tentatives, attendre 2 secondes entre chaque tentative
@retry(stop=stop_after_attempt(5), wait=wait_fixed(2))
def publish_to_rabbitmq(queue_name, message):
    try:
        #connexion a rabbitmq
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()

        #declarer la queue si elle n'existe pas
        channel.queue_declare(queue=queue_name, durable=True)

        #publie la message dans la queue
        channel.basic_publish(exchange='', routing_key=queue_name, body=message, properties=pika.BasicProperties(delivery_mode=2))
        print(f"Message publie dans la queue {queue_name}")

        #fermer la connection
        connection.close()
    except Exception as e:
        print("Erreur lors de la publication dans rabbitmq", e)
        raise 