import os
import cv2
from json_tricks import loads
from kafka import KafkaConsumer

# output folder
PROJECT_ROOT = os.environ.get("SCALER_OUTPUT_DIR", "/tmp")

# ratio for scaling image
RATIO = 0.5

# consumer topic
TOPIC = 'frames'

# message size
MSG_SIZE = 15728640

# consumer connection to kafka
consumer = KafkaConsumer(TOPIC,
                         bootstrap_servers='localhost:9092',
                         auto_offset_reset='earliest',
                         # enable_auto_commit=True,
                         # auto_commit_interval_ms=500,
                         value_deserializer=(
                           lambda x: loads(x.decode('utf-8'))),
                         group_id="scalers",
                         fetch_max_bytes=MSG_SIZE,
                         max_partition_fetch_bytes=MSG_SIZE
                         )


def handle(frame_package):
    """Video streaming generator function."""
    # get message values
    video_id = frame_package['instance']
    frame_index = frame_package['frame_num']
    frame = frame_package['frame']
    print("Consumed frame %i of %s for scaling.." % (frame_index, video_id))

    # scaling image
    width = int(frame.shape[1] * RATIO)
    height = int(frame.shape[0] * RATIO)
    dimension = (width, height)
    resized = cv2.resize(frame, dimension, interpolation=cv2.INTER_AREA)

    # save new image to disk
    file_name = "Frame%i.jpg" % frame_index
    directory = os.path.join(PROJECT_ROOT, video_id)
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, file_name)
    # scipy.misc.imsave(path, image_array)
    cv2.imwrite(path, resized)
    print("Saved frame %i of %s to disk" % (frame_index, video_id))


def main():
    print("starting to consume")
    # Iterate through kafka messages
    for frame_package in consumer:
        handle(frame_package.value)


if __name__ == '__main__':
    main()
