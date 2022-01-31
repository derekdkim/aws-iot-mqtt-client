import json
from time import sleep
import ssl
import paho.mqtt.client as mqtt
from dotenv import load_dotenv
import os
from geopy import distance

load_dotenv()


class IoTClient(object):
    def __init__(self, topic="default", lat=0, lng=0):
        self.connect = False
        self.topic = topic
        self.lat = lat
        self.lng = lng

    def on_connect(self, client, userdata, flags, rc):
        self.connect = True
        print("Connection successful!")
        # Reconnect if connection is lost
        client.subscribe(self.topic)

    def on_message(self, client, userdata, msg):
        if msg.topic == "geolocation":
            incoming = json.loads(msg.payload)
            # Only emit if the source is from another device
            if incoming["id"] != os.getenv("ID"):
                # Use GeoPy haversine formula to calculate distance
                client_coord = (self.lat, self.lng)
                payload_coord = (incoming["lat"], incoming["lng"])
                print(
                    f"Distance to {incoming['id']}: {round(distance.distance(client_coord, payload_coord).km)}km"
                )

    def on_publish(self, client, userdata, msg):
        print("Sent message")

    def bootstrap_mqtt(self):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_publish = self.on_publish

        aws_host = os.getenv("AWS_ENDPOINT")
        aws_port = 8883

        ca_path = "./credentials/root-CA.crt"
        cert_path = "./credentials/Thing.cert.pem"
        private_key_path = "./credentials/Thing.private.key"

        self.client.tls_set(
            ca_certs=ca_path,
            certfile=cert_path,
            keyfile=private_key_path,
            cert_reqs=ssl.CERT_REQUIRED,
            tls_version=ssl.PROTOCOL_TLS,
            ciphers=None,
        )

        connection_result = self.client.connect(aws_host, aws_port, keepalive=60)

        if connection_result == 0:
            print("Connected to AWS")
            self.connect = True

        return self

    def start(self):
        print("Client started!")
        self.client.loop_start()

        while True:
            sleep(1)
            if self.connect is True:
                self.client.publish(
                    self.topic,
                    json.dumps(
                        {
                            "lat": os.getenv("LAT"),
                            "lng": os.getenv("LNG"),
                            "id": os.getenv("ID"),
                        }
                    ),
                )
            else:
                print("This device is not connected. Please reconnect")


if __name__ == "__main__":
    IoTClient(
        topic="geolocation", lat=os.getenv("LAT"), lng=os.getenv("LNG")
    ).bootstrap_mqtt().start()
