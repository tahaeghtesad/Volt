import numpy as np

from envs.power.thirteen_bus import ThirteenBus

env = ThirteenBus()

obs = env.reset()
done = False
while not done:
    obs, reward, done, info = env.step(env.action_space.sample())
    print(obs)