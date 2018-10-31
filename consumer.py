import os

os.environ["CLASSPATH"] = "C:\Users\Adi\opencv"

import cv2
from flask import Flask, Response
from kafka import KafkaConsumer
from flask import request

# connect to Kafka server and pass the topic we want to consume
consumer = KafkaConsumer('my-topic', bootstrap_servers='localhost:9092')  # group_id='view'


# Continuously listen to the connection and print messages as recieved
app = Flask(__name__)


@app.route('/resize', methods=['POST'])
def resize():
    ratio = request.args.get('ratio')
    for frame in consumer:
        width = int(frame.shape[1] * ratio)
        height = int(frame.shape[0] * ratio)
        dim = (width, height)
        resized = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
        # cv2.imwrite(path, resized)


@app.route('/', methods=['POST'])
def index():
    # return a multipart response
    return Response(kafkastream(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


def kafkastream():
    for msg in consumer:
        yield (b'--frame\r\n'
               b'Content-Type: image/png\r\n\r\n' + msg.value + b'\r\n\r\n')


if __name__ == '__main__':
    app.run(debug=True)
