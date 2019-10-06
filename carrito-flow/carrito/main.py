import base64
import logging
import datetime
import os
import random

from simplejson import dumps

from flask import Flask
from googleapiclient.discovery import build


app = Flask(__name__)


@app.route('/')
def publish():
    from google.cloud import pubsub_v1

    project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
    print(project_id)

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, 'carrito')
    data = {'floor': random.randint(0, 4), 'date': '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())}
    future = publisher.publish(topic_path, data=dumps(data).encode())
    return 'Send'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888   , debug=True)
