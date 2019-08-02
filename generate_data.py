from beamngpy import BeamNGpy, Scenario, Vehicle, Road
from beamngpy.sensors import Camera
from config import CAMERA_HEIGHT, CAMERA_WIDTH, FOV
import numpy as np
import cv2
from donkey_gym.envs.beamng_sim import TrainingRoad, ASFAULT_PREFAB, update_prefab, RoadPoint

road = TrainingRoad(ASFAULT_PREFAB)
road.calculate_road_line(back=True)

bng = BeamNGpy('localhost', 64256, home='C:\\Users\\Tim\\Documents\\BeamNG.research')
scenario = Scenario('train', 'train')
scenario.add_road(road.asphalt)
scenario.add_road(road.mid_line)
scenario.add_road(road.left_line)
scenario.add_road(road.right_line)


vehicle = Vehicle('ego_vehicle', model='etk800', licence='PYTHON')
front_camera = Camera(pos=(-0.2, 1.4, 1.6), direction=(0, 1, -0.35), fov=FOV, resolution=(CAMERA_WIDTH, CAMERA_HEIGHT),
                                   colour=True, depth=False, annotation=False)
vehicle.attach_sensor("front_camera", front_camera)

# Add it to our scenario at this position and rotation

spawn_point = road.spawn_point()
scenario.add_vehicle(vehicle, pos=spawn_point.pos(), rot=spawn_point.rot())
# Place files defining our scenario for the simulator to read
scenario.make(bng)

prefab_path = scenario.get_prefab_path()
update_prefab(prefab_path)
bng.open()

bng.set_nondeterministic()
bng.set_steps_per_second(60)
# Load and start our scenario
bng.load_scenario(scenario)

bng.start_scenario()
#vehicle.ai_set_mode('span')
#vehicle.ai_set_speed(5)
#vehicle.ai_set_line([{'pos': node.pos(), 'speed': 10} for node in road.road_line])
number_of_images = 2778
while number_of_images < 9000:
    number_of_images += 1
    print(number_of_images)
    bng.step(1)
    sensors = bng.poll_sensors(vehicle)
    image = sensors['front_camera']['colour'].convert('RGB')
    image = np.array(image)
    image = image[:, :, ::-1]
    cv2.imwrite('C:\\Users\\Tim\\PycharmProjects\\reinforcement-learning\\datasets\\{}.jpg'.format(number_of_images), image)

bng.close()