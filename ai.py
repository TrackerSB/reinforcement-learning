from typing import Callable

import gym
import numpy as np
import os
from drivebuildclient.AIExchangeService import AIExchangeService
from drivebuildclient.aiExchangeMessages_pb2 import SimulationID, VehicleID
from lxml.etree import _Element, Element

from training_gym.envs.drivebuild_sim import Simulation
from algos import DDPG
from stable_baselines.common import set_global_seeds
from utils.utils import create_test_env, get_saved_hyperparams
from config import LEVEL_NAME

STATS_PATH = os.path.join(os.path.dirname(__file__), "logs", "ddpg", "BeamNG-0_1", "BeamNG-0")


class DDPGAI(object):
    def __init__(self, service: AIExchangeService):
        set_global_seeds(0)

        hyperparams, stats_path = get_saved_hyperparams(STATS_PATH, norm_reward=False)
        hyperparams["vae_path"] = LEVEL_NAME.vae()
        self.service = service
        self.simulation = Simulation(service)
        self.env = create_test_env(
            stats_path=stats_path,
            seed=0,
            log_dir=None,
            hyperparams=hyperparams,
            simulation=self.simulation,
        )
        self.model = DDPG.load(LEVEL_NAME.model())

    def start(self, sid: SimulationID, vid: VehicleID, dynamic_stats_callback: Callable[[], None]) -> None:
        from drivebuildclient.aiExchangeMessages_pb2 import SimStateResponse

        self.simulation.sid = sid
        self.simulation.vid = vid

        running_reward = 0.0
        ep_len = 0

        sim_state = self.simulation.wait()
        if sim_state is SimStateResponse.SimState.RUNNING:
            obs = self.env.reset()

        while True:
            print(sid.sid + ": Test status: " + self.service.get_status(sid))
            print(vid.vid + ": Wait")

            sim_state = self.simulation.wait()
            if sim_state is SimStateResponse.SimState.RUNNING:
                dynamic_stats_callback()
                action, _ = self.model.predict(obs, deterministic=True)
                # Clip Action to avoid out of bound errors
                if isinstance(self.env.action_space, gym.spaces.Box):
                    action = np.clip(
                        action, self.env.action_space.low, self.env.action_space.high
                    )
                obs, reward, _, _ = self.env.step(action)

                running_reward += reward[0]
                ep_len += 1

            else:
                # clean up
                # self.env.reset()  # FIXME This call requests data that may be not available anymore
                break

    @staticmethod
    def add_data_requests(parent: _Element):
        camera_node = Element("camera")
        camera_node.set("id", "egoFrontCamera")
        camera_node.set("width", "160")
        camera_node.set("height", "120")
        camera_node.set("direction", "FRONT")
        camera_node.set("fov", "60")
        parent.append(camera_node)


class DDPGAILocal(object):
    def __init__(self):
        set_global_seeds(0)

        hyperparams, stats_path = get_saved_hyperparams(STATS_PATH, norm_reward=False)
        hyperparams["vae_path"] = LEVEL_NAME.vae()
        self.env = create_test_env(
            stats_path=stats_path,
            seed=0,
            log_dir=None,
            hyperparams=hyperparams,
        )
        self.model = DDPG.load(LEVEL_NAME.model())

    def start(self, sid: SimulationID, vid: VehicleID) -> None:

        running_reward = 0.0
        ep_len = 0
        obs = self.env.reset()

        while True:
                action, _ = self.model.predict(obs, deterministic=True)
                # Clip Action to avoid out of bound errors
                if isinstance(self.env.action_space, gym.spaces.Box):
                    action = np.clip(
                        action, self.env.action_space.low, self.env.action_space.high
                    )
                obs, reward, _, _ = self.env.step(action)

                running_reward += reward[0]
                ep_len += 1
