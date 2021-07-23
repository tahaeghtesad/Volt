import multiprocessing
from datetime import datetime
import matplotlib.pyplot as plt

import numpy as np

# alpha = 0.001
# beta = 5
# gamma = 200
# c = 1
from envs.remote.client import RemoteEnv


# Data.alpha = 0.001*ones(n,1);
# Data.beta = 5*ones(n,1);
# Data.gamma = 200*ones(n,1);
# Data.c=1*ones(n,1);


def eval(range):
    start = datetime.now()

    config = {
        'index': 3,

        # Default hyper parameters for nodes not trained.
        'alpha': 0.001,
        'beta': 5.0,
        'gamma': 200.0,
        'c': 1,

        # Search range around the default parameters
        'search_range': range,

        # Length of history
        'history_size': 1,

        # Episode length
        'T': 500,
    }
    env = RemoteEnv('localhost', 6985, config)

    print(f'Env created. Action Space: {env.action_space}, Observation Space: {env.observation_space}')

    obs = env.reset()
    done = False
    rewards = []
    step = 0
    while not done:
        # action = np.array([0, 0, 0, 0])
        action = env.action_space.sample()
        obs, reward, done, info = env.step(action)

        # print(f'Step: {step} - Obs: {obs} - Action: {action} - Reward: {reward}')

        # obs, reward, done, info = env.step(10000 * np.random.random((4 * env.n,)) - 5000)
        rewards.append(reward)
        step += 1

    print(f'Took {datetime.now()-start:} (s).')
    env.close()
    return rewards


if __name__ == '__main__':
    ranges = [0, .1, .3, .5, .7, .9, 1, 2, 3, 4]
    with multiprocessing.Pool(12) as p:
        responses = p.map(eval, ranges)
    for i in range(len(ranges)):
        print(f'range: {ranges[i]} - reward: {np.array(responses[i]).sum()}')
        plt.plot(responses[i][:-1], label=f'{ranges[i]}')
    plt.legend()
    plt.show()
