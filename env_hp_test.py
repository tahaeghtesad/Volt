import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
from datetime import datetime

from envs.power.thirteen_bus import ThirteenBus

# Data.alpha = 0.001*ones(n,1);
# Data.beta = 5*ones(n,1);
# Data.gamma = 200*ones(n,1);
# Data.c=1*ones(n,1);

# alpha = 0.001
# beta = 5
# gamma = 200
# c = 1
from envs.remote.client import RemoteEnv


def eval(params):
    alpha, beta, gamma, c = params
    start = datetime.now()

    env = RemoteEnv('localhost', 6985, None)

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

        # obs, reward, done, info = env.step(10000 * np.random.random((4 * env.n,)) - 5000)
        rewards.append(reward)

    print(f'Took {datetime.now()-start:} (s).')
    return rewards

# plt.plot(q_table.T)
# plt.show()
#
# plt.plot(rewards)
# plt.show()


if __name__ == '__main__':
    params = list()

    for alpha in [.00001, 0.001, 0.1]:
        for beta in [.05, 5, 500]:
            for gamma in [.2, 200, 2000]:
                for c in [0.01, 1, 100]:

                    params.append((alpha, beta, gamma, c))

    from multiprocessing import Pool

    with Pool(16) as pool:
        result = pool.map(eval, params)

    for i in range(len(params)):
        print(f'a={params[i][0]}\tb={params[i][1]}\tg={params[i][2]}\tc={params[i][3]}\t\t{sum(result[i]):.2f}')