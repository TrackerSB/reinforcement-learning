# Learning to Drive Smoothly in Minutes

This is a version of [araffin's](https://github.com/araffin) reinforcement learning approach using deep deterministic policy gradient (DDPG) with a variational encoder (VAE) adopted and trained on BeamNG.research.



## Using trained AI with DriveBuild
0. Import the ```DDPGAI``` class from ai.py in the root directory
1. Instantiate an object and execute the ```.start(sid, vid)``` method

```
from ai import DDPGAI
from client.aiExchangeMessages_pb2 import SimulationID, VehicleID

ai = DDPGAI()

sid = SimulationID()
sid.sid = "some simulation id"

vid = VehicleID()
vid.vid = "ego"

ai.start(sid, vid)
```
 
### Modes
There are two pretrained variational encoders and models which were trained on roads generated by [AsFault](https://github.com/alessiogambi/AsFault).
However, different environments were used:

1. Pure smallgrid level (the world does not contain anything but the road)
2. Smallgrid level filled with gras

For both environments the same road materials were used:
0. Asphalt: ```a_asphalt_01_a```
1. Mid line marking: ```line_yellow```
2. Left and right line markings: ```line_white```

Pure smallgrid        | Smallgrid filled with gras
:-------------------------:|:-------------------------:
![result](content/pure_mode.gif)  | ![result](content/gras_mode.gif)
```LEVEL_NAME = Level.PURE``` | ```LEVEL_NAME = Level.GRAS``` 

By default a VAE and an agent trained on in gras mode are used.
In ```config.py``` it is defined as ```LEVEL_NAME = Level.GRAS```.
Change it to ```LEVEL_NAME = Level.PURE``` in order to use the VAE and the agent which were trained in the pure smallgrid environment. 
Make sure to use the correct mode, otherwise you may encounter some weird behavior. **(Note: the agent which was trained in the pure smallgrid environment performs much worse than the ones trained in the gras environment)**

### Camera properties
During the training the front camera was used with these properties:
1. Position: ```(0, 1.4, 1.8)``` 
2. Direction: ```(0, 1, -0.23)``` 
3. Field of view (FOV): ```120```
4. Resolution (Width, Height): ```(160, 120)```

## Credits
Related Paper: ["Learning to Drive in a Day"](https://arxiv.org/pdf/1807.00412.pdf).

- [r7vme](https://github.com/r7vme/learning-to-drive-in-a-day) Author of the original implementation
- [Wayve.ai](https://wayve.ai) for idea and inspiration.
- [Tawn Kramer](https://github.com/tawnkramer) for Donkey simulator and Donkey Gym.
- [Stable-Baselines](https://github.com/hill-a/stable-baselines) for DDPG/SAC and PPO implementations.
- [RL Baselines Zoo](https://github.com/araffin/rl-baselines-zoo) for training/enjoy scripts.
- [S-RL Toolbox](https://github.com/araffin/robotics-rl-srl) for the data loader
- [Racing robot](https://github.com/sergionr2/RacingRobot) for the teleoperation
- [World Models Experiments](https://github.com/hardmaru/WorldModelsExperiments) for VAE implementation.
