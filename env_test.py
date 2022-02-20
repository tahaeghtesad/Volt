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
from envs.power.thirteen_bus import ThirteenBus
from remote_server import ServerThread
from util.reusable_pool import ReusablePool

# alpha = np.log10(0.002)
# beta = np.log10(0.5)
# gamma = np.log10(100)
# c = np.log10(1)


# alpha = 10 ** -4.069457373049808
# beta = 10 ** 3.9795074542061593
# gamma = 10 ** 3.507641819850809
# c = 10 ** 1.0328233759129137

# alpha, beta, c, gamma = {'alpha': -2.2329853389581658, 'beta': 0.12929655914177918, 'c': 0.25154342834675436, 'gamma': 2.3418920409325708}.values()
# alpha, beta, gamma, c = (-1., 3.041845, 1.963370, 0.488047)
# alpha, beta, gamma, c =  (-4.7603732969850086, -5.0000000000000000,  3.1174591404670213,  1.5842818460532611)
alpha, beta, gamma, c = (-1.6145001260743783, 1.1579715364588790, 1.4101386575517729, -1.730091534553142)

engine_pool = ReusablePool(1, ServerThread.init_matlab, ServerThread.clean_matlab)
logging.basicConfig(stream=sys.stdout,
                    format='%(asctime)s - %(name)s - %(threadName)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

env = ThirteenBus(engine_pool, env_config={
    'mode': 'all_control',
    'search_range': 4,
    'voltage_threshold': 0.05,
    'T': 500,
    'repeat': 1,
    'window_size': 150,
})

rs = []

if __name__ == '__main__':
    for epoch in range(1):

        q_table = np.zeros((env.n, env.T // env.env_config['repeat']))
        v_table = np.zeros((env.n, env.T // env.env_config['repeat']))

        obs = env.reset()
        done = False
        rewards = []
        fs = []
        mqs = []
        fes = []
        for step in tqdm(range(env.T // env.env_config['repeat'])):
            obs, reward, done, info = env.step(np.concatenate((
                alpha * np.ones(env.n),
                beta * np.ones(env.n),
                gamma * np.ones(env.n),
                c * np.ones(env.n),
            )))

            q_table[:, env.step_number - 1] = info['q'].reshape((env.n,))
            v_table[:, env.step_number - 1] = info['v'].reshape((env.n,))
            rewards.append(reward)
            fs.append(info['f'])
            if not np.isnan(info['max_q_slope']):
                mqs.append(info['max_q_slope'])

            fes.append(info['fes'])

        plt.title('q')
        plt.plot(q_table.T[1:-1, :])
        plt.savefig('q.png')
        plt.show()

        plt.title('v')
        plt.plot(v_table.T[1:-1, :])
        plt.savefig('v.png')
        plt.show()

        plt.title('r')
        plt.plot(rewards[:-1])
        plt.savefig('r.png')
        plt.show()

        plt.title('f')
        plt.plot(fs[:-1])
        plt.savefig('f.png')
        plt.show()

        plt.title('fes')
        plt.plot(fes[:-1])
        plt.savefig('fes.png')
        plt.show()

        plt.title('max-slope')
        plt.plot(np.log10(mqs[:-1]))
        plt.savefig('max-slope.png')
        plt.show()

        print(sum(rewards))
        rs.append(sum(rewards))

    print(sum(rs) / len(rs))
