import os

os.environ["CLASSPATH"] = "C:\Users\Adi\opencv"

import cv2

from json import loads
import time
from kafka import KafkaConsumer
from flask import Flask, request


PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
app = Flask(__name__)


@app.route('/resize', methods=['GET'])
def resize(ratio):
    """Video streaming generator function."""
    ratio = request.args.get('ratio')
    consumer = KafkaConsumer('flask',
                             bootstrap_servers='localhost:9092',
                             auto_offset_reset='earliest',
                             enable_auto_commit=True,
                             auto_commit_interval_ms=1000,
                             group_id='resizers',
                             value_deserializer=(lambda x: loads(x.decode('utf-8'))),
                             fetch_max_bytes=15728640,
                             max_partition_fetch_bytes=15728640)
    for msg in consumer:
        instance, frame_num, frame = msg['instance'], msg['frame_num'], msg['frame']
        width = int(frame.shape[1] * ratio)
        height = int(frame.shape[0] * ratio)
        dim = (width, height)
        resized = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
        path = os.path.join(PROJECT_ROOT, "%s/%s" % (instance,frame_num))
        cv2.imwrite(path, resized)


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
