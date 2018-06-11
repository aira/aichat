import object_detection.constants as constants
from nlp import describe_scene
from nlp.dispatch import Dispatchable

from object_detection import db


class DescribeScene(Dispatchable):

    def __init__(self, state_q, confidence):
        self.state_q = state_q
        self.confidence = confidence

    def respond(self, command_payload, user_id):

        state = self.get_state()

        failed_resp = "I heard you, but I don't recognize any of the objects in the scene."

        failure_kwargs = {
            # 'status_message': "Unable to identify any objects in the image.",
            # 'status_code': 'ch-vis-001',
        }

        # Send fail response if no state found
        if not state:
            self.say(
                command_payload=command_payload,
                text=failed_resp,
                confidence=0,
                user_id=user_id,
                **failure_kwargs)
            return

        vecs = constants.to_object_series_list(state)
        db.append(vecs, command=self.__class__.__name__)

        # Get the average confidence to pass into the payload
        conf_scores = map(lambda vec: vec['confidence'], vecs)
        final_conf = sum(conf_scores) / len(vecs)

        # get scene description
        description = describe_scene(vecs, min_conf=self.confidence / 100.)

        # handle failed description
        if description is '':
            description = failed_resp
            final_conf = 0

        # respond
        self.say(
            command_payload=command_payload,
            text=description,
            confidence=final_conf,
            user_id=user_id)
