# producer.py
import time
import imageio
from kafka import KafkaProducer
from json_tricks import dumps

producer = KafkaProducer(bootstrap_servers='localhost:9092',
                         batch_size=15728640,
                         # linger_ms=2000,
                         max_request_size=15728640,
                         value_serializer=lambda x: dumps(x).encode('utf-8')
                         )
# Assign a topic
TOPIC = 'frames'
TRANSACTIONS_PER_SECOND = 10
SLEEP_TIME = 1 / TRANSACTIONS_PER_SECOND
instance_id = 0


def _produce_frames(video):
    global instance_id
    print(' emitting %s.....' % instance_id)
    index = 0
    # read the file

    reader = imageio.get_reader(video, 'ffmpeg')
    for image in reader:
        frame = image
        msg = {"instance": "vid-instance%i" % instance_id,
               "frame_num": index,
               "frame": frame}
        # send message to kafka
        producer.send(TOPIC, value=msg)
        if index % 10 == 0:
            print("produced frame %i" % index)
            producer.flush()
        index += 1
        # To reduce CPU usage
        time.sleep(SLEEP_TIME)

    video.release()
    # producer.flush()
    instance_id += 1


def resize(video_path):
    _produce_frames(video_path)
