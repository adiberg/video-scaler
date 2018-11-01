# producer.py
import time
import imageio
from kafka import KafkaProducer
from json_tricks import dumps

# message size
MSG_SIZE = 15728640

producer = KafkaProducer(bootstrap_servers='localhost:9092',
                         batch_size=MSG_SIZE,
                         # linger_ms=2000,
                         max_request_size=MSG_SIZE,
                         value_serializer=lambda x: dumps(x).encode('utf-8')
                         )
# Assign a topic
TOPIC = 'frames'
TRANSACTIONS_PER_SECOND = 10
SLEEP_TIME = 1 / TRANSACTIONS_PER_SECOND
instance_id = 0


def resize(frame_msg):
    producer.send(TOPIC, value=frame_msg)
    time.sleep(SLEEP_TIME)