import logging
import os
import json
import paho.mqtt.client as mqtt

Parameters = {}

def setParameters():
  Parameters["log_level"]         = str(os.getenv("FORWARDER_LOGLEVEL", default = "WARNING"))
  Parameters["mqtt_broker_host"]  = str(os.getenv("MQTT_BROKER_HOST", default = "localhost"))
  Parameters["mqtt_broker_port"]  = int(os.getenv("MQTT_BROKER_PORT", default = 1883))
  Parameters["mqtt_source_topic"] = str(os.getenv("MQTT_SOURCE_TOPIC", default = "domoticz/out"))
  Parameters["mqtt_target_topic"] = str(os.getenv("MQTT_TARGET_TOPIC", default = "domoticz/switches"))

def onConnect(client, userdata, flags, rc):
  logger = logging.getLogger(__name__)
  logger.info("Connected to broker " + Parameters['mqtt_broker_host'] + ":" + str(Parameters['mqtt_broker_port']) + " with result code " + str(rc))
  client.subscribe(Parameters["mqtt_source_topic"])
  logger.info("Subscribed topic: " + Parameters["mqtt_source_topic"])

def onMessage(client, userdata, msg):
  json_msg = json.loads(msg.payload.decode('utf-8'))
  logger.debug("Publish message: " + json.dumps(json_msg))
  client.publish(Parameters["mqtt_target_topic"], json.dumps(json_msg))

def main(p):
  setParameters()

  logging.basicConfig(format = "%(asctime)s [%(levelname)s]: %(message)s")

  logger = logging.getLogger(__name__)
  logger.setLevel(p['log_level'])

  client = mqtt.Client()
  client.connect(p["mqtt_broker_host"], p["mqtt_broker_port"])

  client.on_connect = onConnect
  client.on_message = onMessage

  client.loop_forever()


if __name__ == '__main__':
    main(Parameters)
