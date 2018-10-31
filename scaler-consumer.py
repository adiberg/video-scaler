import os
import cv2
from json import loads
from kafka import KafkaConsumer

PROJECT_ROOT = os.environ.get("SCALER_OUTPUT_DIR", "/tmp")


def resize(ratio):
  """Video streaming generator function."""
  consumer = KafkaConsumer('flask',
                           bootstrap_servers='localhost:9092',
                           auto_offset_reset='earliest',
                           enable_auto_commit=True,
                           auto_commit_interval_ms=1000,
                           group_id='resizers',
                           value_deserializer=(
                             lambda x: loads(x.decode('utf-8'))),
                           fetch_max_bytes=15728640,
                           max_partition_fetch_bytes=15728640)
  for msg in consumer:
    instance, frame_num, frame = msg['instance'], msg['frame_num'], msg['frame']
    width = int(frame.shape[1] * ratio)
    height = int(frame.shape[0] * ratio)
    dim = (width, height)
    resized = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
    path = os.path.join(PROJECT_ROOT, "%s/%s" % (instance, frame_num))
    cv2.imwrite(path, resized)


if __name__ == '__main__':
  resize(0.5)
