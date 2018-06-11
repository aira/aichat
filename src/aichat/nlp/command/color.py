from nlp.dispatch import Dispatchable
import object_detection.constants as constants
from object_detection import db


class DescribeObjectColor(Dispatchable):

    color_tmpl = 'The {obj_name} is primarily {color}'

    def __init__(self, state_q):
        self.state_q = state_q

    def respond(self, command_payload, user_id):

        failure_kwargs = {
            # 'status_message': "Unable to identify any objects in the image.",
            # 'status_code': 'ch-vis-001',
        }

        state = self.get_state()

        if not state:
            self.say(
                command_payload=command_payload,
                text="I don't see any objects in front of you.",
                confidence=0,
                user_id=user_id,
                **failure_kwargs)
            return

        vecs = constants.to_object_series_list(state)
        db.append(vecs, command=self.__class__.__name__)

        def color_score(vec):
            """Objective function: rewards high confidence and penalizes objects who are not centered"""
            score = vec['confidence']

            x_center = vec['x']

            score -= 2 * abs(0.5 - x_center)

            return score

        # Prefer the most confident, centrally located object
        obj_vec = max(vecs, key=color_score)

        # format color description template with chosen object
        max_color = obj_vec.obj_primary_color
        obj_name = obj_vec['category']

        self.say(
            command_payload=command_payload,
            text=self.color_tmpl.format(obj_name=obj_name, color=max_color),
            confidence=obj_vec['confidence'],
            user_id=user_id)


class DescribeSceneColor(Dispatchable):
    # TODO: implement

    def get_scene_color(self):
        pass
