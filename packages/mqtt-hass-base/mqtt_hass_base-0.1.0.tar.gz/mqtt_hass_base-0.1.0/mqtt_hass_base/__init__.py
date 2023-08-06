import os
import uuid
import signal
import logging

import paho.mqtt.client as mqtt


VERSION = "0.1.0"


class MqttDevice():

    def __init__(self, name=None):
        if name:
            self.name = name
        else:
            self.name = os.environ.get('MQTT_NAME', "mqtt-device-" + str(uuid.uuid1()))
        self.must_run = False
        self.mqtt_client = None
        # Get logger
        self.logger = self._get_logger()
        self.logger.info('Initializing...')
        self.read_base_config()
        self.read_config()

    def _get_logger(self):
        """Build logger."""
        logging_level = logging.DEBUG
        logger = logging.getLogger(name=self.name)
        logger.setLevel(logging_level)
        console_handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        return logger

    def read_config(self):
        raise NotImplementedError

    def read_base_config(self):
        self.mqtt_username = os.environ['MQTT_USERNAME']
        self.mqtt_password = os.environ['MQTT_PASSWORD']
        self.mqtt_host = os.environ['MQTT_HOST']
        try:
            self.mqtt_port = int(os.environ['MQTT_PORT'])
        except ValueError:
            raise Exception("Bad MQTT port")
        self.mqtt_root_topic = os.environ.get('ROOT_TOPIC', "homeassistant")
        self._loglevel = os.environ.get('LOG_LEVEL', 'DEBUG').upper()
        self.logger.setLevel(getattr(logging, self._loglevel))

    def _mqtt_connect(self):
        """Connecto to the MQTT server."""
        self.logger.info("Connecting to mqtt server")
        client = mqtt.Client(client_id=self.name)
        client.username_pw_set(self.mqtt_username, self.mqtt_password)

        client.on_message = self._base_on_message
        client.on_connect = self._base_on_connect
        client.on_publish = self._base_on_publish

        client.connect(self.mqtt_host, self.mqtt_port, 60)

        client.loop_start()
        self.logger.info("Connected to mqtt server")
        return client

    def _base_on_connect(self, client, userdata, flags, rc):  # pylint: disable=W0613,C0103
        """MQTT on_connect callback."""
        self.logger.debug("Connected with result code %s", str(rc))

        self._on_connect(client, userdata, flags, rc)
        self._mqtt_subscribe(client, userdata, flags, rc)
        self.logger.debug("Subscribing done")

    def _on_connect(self, client, userdata, flags, rc):
        raise NotImplementedError

    def _mqtt_subscribe(self, client, userdata, flags, rc):
        raise NotImplementedError

    def _base_on_message(self, client, userdata, msg):
        """MQTT on_message callback."""
        self.logger.info("Message received: %s %s", msg.topic, str(msg.payload))
        self._on_message(client, userdata, msg)

    def _on_message(self, client, userdata, msg):
        raise NotImplementedError

    def _base_on_publish(self, client, userdata, mid):
        self.logger.debug("PUBLISH")
        self._on_publish(client, userdata, mid)

    def _on_publish(self, client, userdata, mid):
        raise NotImplementedError

    def _base_signal_handler(self, signal_, frame):
        """Signal handler."""
        self.logger.info("SIGINT received")
        self.logger.debug("Signal %s in frame %s received", signal_, frame)
        self.must_run = False
        self.mqtt_client.loop_stop()
        self._signal_handler(signal_, frame)
        self.logger.info("Exiting...")

    async def async_run(self):
        """Loop."""
        self.logger.info("Start main process")
        self.must_run = True
        # Add signal handler
        signal.signal(signal.SIGINT, self._base_signal_handler)
        # Mqtt client
        self.mqtt_client = self._mqtt_connect()
        await self._init_main_loop()
        while self.must_run:
            self.logger.debug("We are in the main loop")
            await self._main_loop()
        self.logger.info("Main loop stopped")
        self.mqtt_client.loop_stop()
        await self._loop_stopped()

    def _signal_handler(self, signal_, frame):
        raise NotImplementedError

    async def _init_main_loop(self):
        raise NotImplementedError

    async def _main_loop(self):
        raise NotImplementedError

    async def _loop_stopped(self):
        raise NotImplementedError
