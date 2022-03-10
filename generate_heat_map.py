import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
import seaborn as sns

from envs.power.thirteen_bus import ThirteenBus
from envs.remote.client import RemoteEnv
from remote_server import ServerThread
from util.reusable_pool import ReusablePool

config = {
    'mode': 'all_control',
    'voltage_threshold': 0.05,

    # Search range around the default parameters
    'search_range': 2,

    # Length of history
    'history_size': 1,

    # Episode length
    'T': 12,

    # Repeat
    'repeat': 1,

    'window_size': 10,

    'change_threshold': 0.2,
}


class Tester:

    def __init__(self, config=None):
        super().__init__()
        engine_pool = ReusablePool(1, ServerThread.init_matlab, ServerThread.clean_matlab)
        self.env = ThirteenBus(engine_pool=engine_pool, env_config=config)

    def eval(self, alpha, beta, gamma, c):
        rewards = []
        obs = self.env.reset()
        done = False
        while not done:

            obs, reward, done, info = self.env.step(
                np.array([alpha, beta, gamma, c]))

            rewards.append(reward)

        return dict(episode_reward=sum(rewards))


if __name__ == '__main__':

    np.set_printoptions(precision=3)

    alpha = np.log10(0.002)
    beta = np.log10(0.5)
    gamma = np.log10(100)
    c = np.log10(1)

    alpha_range = np.linspace(-3, 0, 20)
    c_range = np.linspace(-1, 3, 20)
    values = np.zeros((len(alpha_range), len(c_range)))

    tester = Tester(config)

    for i, alpha in enumerate(tqdm(alpha_range)):
        for j, c in enumerate(c_range):
            result = tester.eval(alpha, beta, gamma, c)
            values[i][j] = result['episode_reward']

    ax = sns.heatmap(values,
                     cmap='YlGnBu',
                     xticklabels=[f'{i:.1f}' for i in alpha_range],
                     yticklabels=[f'{i:.1f}' for i in c_range])
    ax.set_xlabel('alpha')
    ax.set_ylabel('c')
    plt.show()