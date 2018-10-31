import sys
import os
from json import dumps
import time
import imageio
import cv2
import numpy as np
from kafka import KafkaProducer

PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


def video_loop(video_reader, producer, fps):

    return


def main(video_path):
    """Stream the video into a Kafka producer in an infinite loop"""

    video_reader = imageio.get_reader(video_path, 'ffmpeg')
    metadata = video_reader.get_meta_data()
    fps = metadata['fps']

    producer = KafkaProducer(bootstrap_servers='localhost:9092',
                             batch_size=15728640,
                             linger_ms=2000,
                             max_request_size=15728640,
                             value_serializer=lambda x: dumps(x).encode('utf-8'))

    # Iterate through frames and pass to the producer (with timing calibration)
    c = 0
    for frame in video_reader:
        if c % 3 != 0:
            continue
        producer.send('flask', value={"instance": "dd", "frame_num": 1, "frame": frame})
        # time.sleep(1.0/fps)


if __name__ == '__main__':
    main('video.mp4')
