import os
import cv2
from json import loads
from kafka import KafkaConsumer

PROJECT_ROOT = os.environ.get("SCALER_OUTPUT_DIR", "/tmp")
RATIO = 0.5

consumer = KafkaConsumer('flask',
                         bootstrap_servers='localhost:9092',
                         auto_offset_reset='earliest',
                         enable_auto_commit=True,
                         auto_commit_interval_ms=1000,
                         group_id='scalers',
                         value_deserializer=(
                           lambda x: loads(x.decode('utf-8'))),
                         fetch_max_bytes=15728640,
                         max_partition_fetch_bytes=15728640)


def handle(frame_package):
  """Video streaming generator function."""
  video_id, frame_index, frame = frame_package['instance'], \
                                 frame_package['frame_num'], \
                                 frame_package['frame']
  width = int(frame.shape[1] * RATIO)
  height = int(frame.shape[0] * RATIO)
  dimension = (width, height)
  resized = cv2.resize(frame, dimension, interpolation=cv2.INTER_AREA)
  file_name = "Frame%i.jpg" % frame_index
  path = os.path.join(PROJECT_ROOT, video_id, file_name)
  cv2.imwrite(path, resized)


def main():
  for frame_package in consumer:
    handle(frame_package)


if __name__ == '__main__':
  main()
