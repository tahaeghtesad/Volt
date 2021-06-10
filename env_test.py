import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt

from envs.power.thirteen_bus import ThirteenBus

# Data.alpha = 0.001*ones(n,1);
# Data.beta = 5*ones(n,1);
# Data.gamma = 200*ones(n,1);
# Data.c=1*ones(n,1);

alpha = 0.001
beta = 5
gamma = 200
c = 1

env = ThirteenBus(env_config={
    'T': 10000
})

q_table = np.zeros((29, env.T))

obs = env.reset()
done = False
rewards = []
while not done:
    obs, reward, done, info = env.step(np.concatenate((
        alpha * np.ones(env.n),
        beta * np.ones(env.n),
        gamma * np.ones(env.n),
        c * np.ones(env.n),
    )))

    q_table[:, env.step_number - 1] = info['q'].reshape((29, ))
    rewards.append(reward)

plt.plot(q_table.T)
plt.show()

plt.plot(rewards)
plt.show()