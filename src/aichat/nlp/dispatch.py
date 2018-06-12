"""
Module interprets agent commands and dispatches an action


How to extend NLP commands:

1. Import: `from nlp.dispatch import Dispatchable, dispatcher`
2. Subclass `Dispatchable`, implementing the action in `__call__`. Call takes in a python dictionary (the `payload`)
3. Expand the `displatcher` with a command: `dispatcher['<command>'] = <Subclass of Dispatchable>`
"""

import json
import os
import typing
import collections
import re
import time


import paho.mqtt.client as mqtt
from datetime import datetime
import queue

from object_detection.constants import logging, LOGGER_NAME, ObjectSeries
from object_detection import db
from nlp.video_manager import build_video_url, VideoManager
from nlp import transform
from cloud import vision


logger = logging.getLogger(LOGGER_NAME)


# MQTT Constants
DEFAULT_USER_ID = 1234
TOPIC_PATTERN = re.compile(r'dev/chloe/(?P<dest>\w*)/(?P<user_id>\w*)/(?P<command>\w*)(/\w*)*')
EXPLORER_TOPIC = 'dev/chloe/explorer/'
EXPLORER_SUB_TOPIC_TMPL = EXPLORER_TOPIC + '{user_id}/statement'
AGENT_TOPIC = 'dev/chloe/agent/'
AGENT_PUB_TOPIC_TMPL = AGENT_TOPIC + '{user_id}/response'


# Define event callbacks
def on_connect(client, userdata, flags, rc):
    logger.info("Connection to client! rc: " + str(rc))


def on_publish(client, obj, mid):
    logger.info("Publishing AI Response mid: " + str(mid))


def on_subscribe(client, obj, mid, granted_qos):
    logger.info("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_log(client, obj, level, string):
    logger.info(string)


def on_message(client, user_data, msg):
    """MQTT Message Handler: Responsible for starting and stopping video stream and statement dispatcher

    This function will parse the incoming topic. If a `start` command is initiated with a `user_id`,
    the object detector app will ingest a video stream corresponding to that `user_id`. In addition,
    the dispatcher will respond to commands issued from `+/<user_id>/statement`.

    If a `stop` command is initiated with a `user_id`, the video stream and statement/command dispatch
    handler will cease responding to that user.

    Args:
        client: The current MQTT client
        user_data:  The private user data set in Client()
        msg: An instance of a MQTT message; a dictionary that contains `payload`, `topic`, `qos`,
         and `retain`.

    Returns:
        None

    """
    # Extract fields from topic into dictionary
    topic = str(msg.topic)
    logger.info('On Message. Topic %s \t\t', topic)

    params = _parse_topic(topic)

    if params is None:
        return

    if params['user_id'] is None:
        return

    # Set subscription and publication topics based on User ID
    current_user_subtopic = EXPLORER_SUB_TOPIC_TMPL.format(**params)

    video_manager = VideoManager.Instance()

    # Handle Start/Stop Commands
    cmd = params['command']
    if 'start' == cmd:
        try:
            # Start video ingestion
            if video_manager is not None:
                video_manager.start(build_video_url(params['user_id']))

            # Init explorer command dispatch handler
            client.message_callback_add(current_user_subtopic, on_statement_message)
        except ValueError as e:
            logger.error('Video URL/User ID is invalid {}', e.with_traceback())
            
    elif 'stop' == cmd:
        # Stop video stream
        if video_manager is not None:
            video_manager.stop()

        # Remove command dispatch handler
        client.message_callback_remove(current_user_subtopic)

    filename = time.strftime('object_vectors-%Y%m%d-%H-partial.csv')
    db.dump(filename=filename)


def _get_mqtt_payload(msg): # -> typing.Optional[typing.Dict]:
    """Extract payload from message while logging the topic

    Args:
        msg: An instance of a MQTT message; a dictionary that contains `payload`, `topic`, `qos`,
         and `retain`.

    Returns:
        None -- On error
        Dictionary -- JSON payload

    Side Effects:
        Logs to `info` on every call -- unless there is an error, then it logs to `error`.
    """
    try:
        topic_str = str(msg.topic)
        json_string = str(msg.payload, 'utf-8')
        logger.info('On message. Topic: %s \t\t: %s', topic_str, json_string)
        payload = json.loads(json_string)
        return payload
    except json.decoder.JSONDecodeError:
        logger.error('On message. Topic: %s \t\t: JSON Decode error of message on topic.', topic_str)
        return None


def _parse_topic(topic: str) -> typing.Optional[typing.Dict]:
    """
    Parse a MQTT topic for key parameters. Namely, the `dest`, `user_id`, and `command`.

    Args:
        topic: A MQTT topic in the format `dev/chloe/<dest>/<user_id>/<command>

    Returns:
        Dictionary with keys `dest`, `user_id`, and `command`.
        None if the topic is malformed


    """
    m = re.match(TOPIC_PATTERN, topic)

    try:
        params = m.groupdict()
        return params
    except Exception:
        logger.error('Topic is malformed: %s', topic)
        return None


def on_statement_message(client, user_data, msg):
    """Explorer Command Dispatcher: Translates MQTT payloads into AI Server Actions

    Args:
        client: current MQTT client
        user_data: Data initialized in MQTT client
        msg: An instance of a MQTT message; a dictionary that contains `payload`, `topic`, `qos`,
         and `retain`.

    Returns:
        None

    """
    topic = str(msg.topic)

    params = _parse_topic(topic)

    if params is None:
        return

    payload = _get_mqtt_payload(msg)
    if payload is None:
        return

    cmd = payload.get('statement', 'default').lower()

    action = interp_command(cmd, list(reversed(dispatcher.keys())))

    logger.info('calling ' + action)
    dispatcher.get(action, NotFound()).respond(payload, params['user_id'])


mqttc = mqtt.Client()


# Assign event callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe
mqttc.on_log = on_log

url_str = os.environ.get('AIRAMQTT_URL', 'preprod-mqtt.aira.io')
port = int(os.environ.get('AIRAMQTT_PORT', '1883'))

logger.info('mqtt connection info: {}:{}'.format(url_str, port))

try:
    mqttc.connect(url_str, port, 15)
    mqttc.subscribe(EXPLORER_TOPIC + '#', 0)
    logger.info('Successfully connected to MQTT server: {}:{}'.format(url_str, port))
except:
    logger.error('Unable to connect to MQTT server: {}:{}'.format(url_str, port))


def interp_command(cmd_str: str, actions: typing.List[str]) -> str:
    """Output a discrete action to take from a user command in natural language.

    Args:
        cmd_str: user command
        actions: list of commands available from dispatcher

    Returns:
        str: single command for dispatcher to execute

    Examples:
        >>> interp_command('describe what is around me', ['describe','count'])
        'describe'
        >>> interp_command('count the number of objects in view', ['describe', 'count'])
        'count'
    """

    # faster, but less readable
    # return next((axn for axn in actions if axn in cmd_str), 'default')

    for axn in actions:
        if axn in cmd_str:
            return axn
    return 'default'


class Dispatchable:
    client = mqttc
    message_id = 0

    def get_state(self, timeout=0.05) -> typing.Optional[typing.List[ObjectSeries]]:
        try:
            state, image = self.state_q.get(timeout=timeout)

            new_labels = vision.reclassify(image,
                                           [transform.distance_to_bbox(vec) for vec in state],
                                           [vec['category'] for vec in state])

            for vec, new_label in zip(state, new_labels):
                if new_label:
                    vec['category'] = new_label[0]
                    vec['confidence'] = (new_label[1] + vec['confidence'] + 1) / 3.
                    logger.info('Using GCV Label for state vector: category {cat}, confidence {conf}'.format(
                        cat=vec['category'],
                        conf=vec['confidence']))

            return state
        except queue.Empty:
            return None

    def say(self,
            command_payload=None,
            text='', confidence=-1, source="chloe",
            status_code='ch-vis-000',
            status_message='success',
            user_id=DEFAULT_USER_ID,
            **kwargs):
        """ Send a say command to the MQTT server with response text for the mobile client and dashboard. """

        command_payload = command_payload or {}
        kwargs['text'] = text
        kwargs['confidence'] = float(confidence)
        kwargs['source'] = source

        timestamp = int((datetime.utcnow() - datetime(1970, 1, 1, 0, 0, 0, 0)).total_seconds() * 1000)

        Dispatchable.message_id += 1

        response_payload = {
            "messageId": Dispatchable.message_id,
            # FIXME: update with actual id from Android App
            "statementId": command_payload.get('messageId', -1),
            "timestamp": timestamp,
            "status":
            {
                "code": status_code,
                "message": status_message
            },
            "action": "say",
            "args": [],
            "kwargs": kwargs,
        }

        payload_json = json.dumps(response_payload)
        self.client.publish(AGENT_PUB_TOPIC_TMPL.format(user_id=user_id), payload=payload_json)


class Echo(Dispatchable):
    def respond(self, command_payload, user_id, **kwargs):
        self.say(command_payload=command_payload, user_id=user_id, **kwargs)


class NoOp(Dispatchable):
    def respond(self, command_payload, user_id):
        pass


class NotFound(Dispatchable):
    def respond(self, command_payload, user_id):
        failed_resp = 'I do not understand that command.'
        self.say(text=failed_resp, command_payload=command_payload, user_id=user_id)


dispatcher = collections.OrderedDict()

if __debug__:
    dispatcher['debug'] = Echo()


def _test_mqtt_loop():
    rc = 0
    while rc == 0:
        rc = mqttc.loop()
    logger.info('rc: ' + str(rc))


if __name__ == '__main__':
    _test_mqtt_loop()
