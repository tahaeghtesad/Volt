import time
from datetime import datetime

import ray
from ray import tune
import numpy as np

from envs.remote.client import RemoteEnv


def eval(config):
    time.sleep(np.random.rand() * 10)
    start = datetime.now()

    env = RemoteEnv('localhost', 6985, config)
    print(f'Env created. Action Space: {env.action_space}, Observation Space: {env.observation_space}')

    obs = env.reset()
    done = False
    rewards = []
    step = 0
    while not done:
        # action = np.array([0, 0, 0, 0])
        # action = env.action_space.low
        obs, reward, done, info = env.step(np.array([config['alpha'], config['beta'], config['gamma'], config['c']]))

        # print(f'Step: {step} - Obs: {obs} - Action: {action} - Reward: {reward}')

        # obs, reward, done, info = env.step(10000 * np.random.random((4 * env.n,)) - 5000)
        # tune.report(reward=reward)
        rewards.append(reward)
        step += 1

    tune.report(episode_reward=sum(rewards))

    print(f'Took {datetime.now()-start:} (s).')
    env.close()

config = {
        # 'index': 3,

        # Default hyper parameters for nodes not trained.
        'defaults': {
            'alpha': 0.001,
            'beta': 5.0,
            'gamma': 200.0,
            'c': 1,
        },

        'alpha': tune.grid_search(np.linspace(0.0005, 0.002, 15).tolist()),
        'beta': tune.grid_search(np.linspace(1, 10, 15).tolist()),
        'gamma': tune.grid_search(np.linspace(150, 250, 15).tolist()),
        'c': tune.grid_search(np.linspace(0.5, 10, 15).tolist()),

        # Search range around the default parameters
        'search_range': 5,

        # Length of history
        'history_size': 1,

        # Episode length
        'T': 500,
    }

if __name__ == '__main__':
    ray.init(num_cpus=8)
    analysis = tune.run(
        eval,
        config=config,)

    print("Best config: ", analysis.get_best_config(
        metric="episode_reward", mode="max"))

    print(analysis.results_df)