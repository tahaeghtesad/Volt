import numpy as np
from tqdm import tqdm

from envs.power.thirteen_bus import ThirteenBus

env = ThirteenBus()

obs = env.reset()
done = False
for i in tqdm(range(10000)):
    obs, reward, done, info = env.step(env.action_space.sample())

    if done:
        obs = env.reset()
