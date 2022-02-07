import logging
import sys

import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt

from envs.power.onetwentythree_bus import OneTwentyThreeBus

# Data.alpha = 0.001*ones(n,1);
# Data.beta = 5*ones(n,1);
# Data.gamma = 200*ones(n,1);
# Data.c=1*ones(n,1);
from remote_server import ServerThread
from util.reusable_pool import ReusablePool

# alpha = 0.002
# beta = 0.5
# gamma = 100
# c = 1

alpha = 10 ** -4.069457373049808
beta = 10 ** 3.9795074542061593
gamma = 10 ** 3.507641819850809
c = 10 ** 1.0328233759129137

engine_pool = ReusablePool(1, ServerThread.init_matlab, ServerThread.clean_matlab)
logging.basicConfig(stream=sys.stdout, format='%(asctime)s - %(name)s - %(threadName)s - %(levelname)s - %(message)s', level=logging.INFO)

env = OneTwentyThreeBus(engine_pool, env_config={
    'mode': 'all_control',
    'search_range': 5,
    'voltage_threshold': 0.05,
    'T': 10,
    'repeat': 1
})

rs = []

if __name__ == '__main__':
    for epoch in tqdm(range(128)):

        q_table = np.zeros((env.n, env.T))
        v_table = np.zeros((env.n, env.T))

        obs = env.reset()
        done = False
        rewards = []
        for _ in range(env.T):
            obs, reward, done, info = env.step(np.log10(np.concatenate((
                alpha * np.ones(env.n),
                beta * np.ones(env.n),
                gamma * np.ones(env.n),
                c * np.ones(env.n),
            ))))

            q_table[:, env.step_number - 1] = info['q'].reshape((env.n, ))
            v_table[:, env.step_number - 1] = info['v'].reshape((env.n, ))
            rewards.append(reward)

        # plt.plot(q_table.T[1:-1, :])
        # plt.show()

        plt.plot(v_table.T[1:-1, :])
        plt.show()

        # plt.plot(rewards[:-1])
        # plt.show()
        # print(sum(rewards))
        rs.append(sum(rewards))

    print(sum(rs)/len(rs))