import io
import numpy as np
from PIL import Image
from drivebuildclient.AIExchangeService import AIExchangeService

from config import CRASH_SPEED_WEIGHT, REWARD_CRASH, ROI
from drivebuildclient.aiExchangeMessages_pb2 import Control, DataRequest


class Simulation(object):

    def __init__(self, service: AIExchangeService) -> None:
        super().__init__()

        self.last_action = (0, 0)
        self.service = service
        self.sid = None
        self.vid = None

    def take_action(self, action):
        steering, throttle = action
        steering = steering.item()
        throttle = throttle.item()
        self.last_action = action

        control = Control()
        control.avCommand.accelerate = throttle
        control.avCommand.steer = steering
        control.avCommand.brake = 0
        self.service.control(self.sid, self.vid, control)

    def _reward(self):
        throttle = self.last_action[1]
        reward = REWARD_CRASH - CRASH_SPEED_WEIGHT * throttle
        return reward

    def observe(self):
        request = DataRequest()
        request.request_ids.extend(["egoFrontCamera_" + self.vid.vid])
        data = self.service.request_data(self.sid, self.vid, request)
        camera_data = data.data["egoFrontCamera_" + self.vid.vid]
        if camera_data.HasField("camera"):
            byte_im = data.data['egoFrontCamera_' + self.vid.vid].camera.color
            image = Image.open(io.BytesIO(byte_im))
            image = image.convert("RGB")
            image = np.array(image)
            r = ROI

            # Cut to the relevant region
            image = image[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]

            # Convert to BGR
            state = image[:, :, ::-1]
        else:
            print("Request for egoFrontCamera returned an error: " + camera_data.error.message)
            state = None  # FIXME Is it allowed to be None?

        reward = self._reward()
        return state, reward, False, {}

    def close_connection(self):
        pass

    def reset(self):
        pass

    def wait(self, vid):
        return self.service.wait_for_simulator_request(self.sid, vid)
