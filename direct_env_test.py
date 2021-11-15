import numpy as np
from tqdm import tqdm

from envs.direct.thirteen_bus_direct import ThirteenBusDirect
import matplotlib.pyplot as plt

load = 1

config = {
    'T': 100,
    'loading': .5,
    'voltage_threshold': .05
}

env = ThirteenBusDirect(config)

steps = 10

obs = env.reset()
rewards = []

voltages = np.zeros((32, steps))

for step in tqdm(range(steps)):
    obs, reward, done, info = env.step(100 * np.random.rand(29))

    rewards.append(reward)
    voltages[:, step] = obs

plt.plot(rewards)
plt.show()

plt.plot(voltages.T)
plt.show()
