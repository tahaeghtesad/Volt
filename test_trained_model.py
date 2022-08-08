import numpy as np

from config import env_config
from custom_ddpg import create_actor, create_critic
from envs.remote.client import RemoteEnv

import matplotlib.pyplot as plt


env = RemoteEnv('localhost', 6985, env_config)
actor = create_actor(env)
critic = create_critic(env)

trial_name = '20220727-171740'

actor.load_weights(f'logs/ddpg/{trial_name}/actor.h5')
critic.load_weights(f'logs/ddpg/{trial_name}/critic.h5')

space = 100

# for x in np.linspace(0.8, 1.2, 10):
x = np.linspace(-1, 1, space)
y = critic([np.zeros((space, 58)), x])
    # print(actor(x * np.ones((space, 58))))
plt.plot(x, y)

plt.show()
