import os
import requests
import json
from dotenv import load_dotenv
import paho.mqtt.client as mqtt

def main():
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    load_dotenv(env_path)

    BBT_HOST = os.environ.get("BBT_HOST")
    BBT_PORT = os.environ.get("BBT_PORT")
    BBT_TOKEN = os.environ.get("BBT_TOKEN")
    BBT_TOPIC = os.environ.get("BBT_TOPIC")
    BBT_CA_CERTS = os.environ.get("BBT_CA_CERTS")

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set('token:%s' % BBT_TOKEN)
    client.tls_set(BBT_CA_CERTS)
    client.connect(BBT_HOST, port=int(BBT_PORT), keepalive=60)
    client.subscribe(BBT_TOPIC)
    client.loop_forever()


def on_connect(client, userdata, flags, respons_code):
    print('Connect to Beebotte: status {0}'.format(respons_code))


def on_message(client, userdata, message):
    try:
        print('on_message from Beebotte -> ' + message.topic + ' ' + str(message.payload))
        data = json.loads(message.payload.decode("utf-8"))["data"]
        _message = data
        notify(_message)
    except Exception as e:
        print(e)


def notify(message):
    GOOGLEHOME_NOTIFIER_IP = os.environ.get("GOOGLEHOME_NOTIFIER_IP")
    GOOGLEHOME_NOTIFIER_PORT = os.environ.get("GOOGLEHOME_NOTIFIER_PORT")

    url = "http://" + GOOGLEHOME_NOTIFIER_IP + ":" + GOOGLEHOME_NOTIFIER_PORT + "/google-home-notifier"
    data = [("text", message),]
    req = requests.post(url, data=data)


if __name__ == '__main__':
    main()
