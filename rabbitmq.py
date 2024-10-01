import pika


def publish_to_rabbitmq(queue_name, message):
    try:
        #connexion a rabbitmq
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()

        #declarer la queue si elle n'existe pas
        channel.queue_declare(queue=queue_name)

        #publie la message dans la queue
        channel.basic_publish(exchange='', routing_key=queue_name, body=message)
        print(f"Message publie dans la queue {queue_name}")

        #fermer la connection
        connection.close()
    except Exception as e:
        print("Erreur lors de la publication dans rabbitmq", e)
        raise e