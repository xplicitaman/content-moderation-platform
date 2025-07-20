import pika
import time
import json

# --- Database setup will be added soon ---
def on_message_received(ch, method, properties, body):
    """Callback function to process a message from the queue."""
    submission_data = json.loads(body)
    submission_id = submission_data.get("submission_id")
    text_to_moderate = submission_data.get("text")

    print(f"[*] Received submission {submission_id}. Moderating text: '{text_to_moderate}'")
    # --- Simulate AI Moderation ---
    time.sleep(5)
    
    print(f"[*] Finished processing for submission {submission_id}")

    ch.basic_ack(delivery_tag=method.delivery_tag)

# --- RabbitMQ connection ---
connection_parameters = pika.ConnectionParameters('localhost')
connection = pika.BlockingConnection(connection_parameters)
channel = connection.channel()

# Ensure the 'moderation_queue' exists
channel.queue_declare(queue='moderation_queue')

# Start consuming messages from the queue and run the callback function
channel.basic_consume(queue='moderation_queue', on_message_callback=on_message_received)

print('[*] Worker starting to consume. To exit, process CTRL+C')
channel.start_consuming()