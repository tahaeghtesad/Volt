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


def eval(i):
    start = datetime.now()

    config = {
        'voltage_threshold': 0.05,

        # Default hyper parameters for nodes not trained.
        'defaults': {
            'alpha': 0.001,
            'beta': 5.0,
            'gamma': 200.0,
            'c': 1,
        },
        # 'defaults': {
        #     'alpha': -4.89428,
        #     'beta': -4.70154,
        #     'gamma': 4.87959,
        #     'c': -3.5647,
        # },

        # Search range around the default parameters
        'search_range': 5,

        # Length of history
        'history_size': 1,

        # Episode length
        'T': 20,
        'repeat': 1,
    }
    env = RemoteEnv('localhost', 6985, config)
    v_table = np.zeros((29, env.T))
    print(f'Env created. Action Space: {env.action_space}, Observation Space: {env.observation_space}')

    obs = env.reset()
    done = False
    rewards = []
    step = 0

    while not done:
        # action = np.array([0, 0, 0, 0])
        # action = env.action_space.low
        action = np.log10(np.array([config['defaults']['alpha'],
                           config['defaults']['beta'],
                           config['defaults']['gamma'],
                           config['defaults']['c']]))
        obs, reward, done, info = env.step(action)
        v_table[:, env.step_number - 1] = info['v'].reshape((29,))

        # print(f'Step: {step} - Obs: {obs} - Action: {action} - Reward: {reward}')

        # obs, reward, done, info = env.step(10000 * np.random.random((4 * env.n,)) - 5000)
        rewards.append(reward)
        step += 1

    print(f'Took {datetime.now() - start:} (s).')
    env.close()
    return rewards, v_table


if __name__ == '__main__':
    ranges = range(1, 2)
    with multiprocessing.Pool(12) as p:
        responses = p.map(eval, ranges)
    for i in range(len(ranges)):
        print(f'range: {ranges[i]} - reward: {np.array(responses[i][0]).sum()}')
        plt.plot(responses[i][0], label=f'{ranges[i]}')
        plt.show()

        plt.plot(responses[i][1].T)
        plt.show()
