import os
import cv2
from json_tricks import loads
from kafka import KafkaConsumer

PROJECT_ROOT = os.environ.get("SCALER_OUTPUT_DIR", "/tmp")
RATIO = 0.5
TOPIC = 'frames'
consumer = KafkaConsumer(TOPIC,
                         bootstrap_servers='localhost:9092',
                         auto_offset_reset='earliest',
                         # enable_auto_commit=True,
                         # auto_commit_interval_ms=500,
                         value_deserializer=(
                           lambda x: loads(x.decode('utf-8'))),
                         group_id="scalers",
                         fetch_max_bytes=15728640,
                         max_partition_fetch_bytes=15728640
                         )


def handle(frame_package):
  """Video streaming generator function."""
  video_id = frame_package['instance']
  frame_index = frame_package['frame_num']
  frame = frame_package['frame']
  print("Consumed frame %i of %s" % (frame_index, video_id))
  width = int(frame.shape[1] * RATIO)
  height = int(frame.shape[0] * RATIO)
  dimension = (width, height)
  resized = cv2.resize(frame, dimension, interpolation=cv2.INTER_AREA)
  file_name = "Frame%i.jpg" % frame_index
  directory = os.path.join(PROJECT_ROOT, video_id)
  os.makedirs(directory, exist_ok=True)
  path = os.path.join(directory, file_name)
  # file_name)
  print(path)
  # scipy.misc.imsave(path, image_array)
  res = cv2.imwrite(path, resized)
  print(res)


def main():
  print("starting to consume")
  for frame_package in consumer:
    handle(frame_package.value)


if __name__ == '__main__':
  main()
