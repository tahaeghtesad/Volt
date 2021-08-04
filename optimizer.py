import math
import time
from datetime import datetime

import ray
from ray import tune
import numpy as np
from ray.tune.suggest.bayesopt import BayesOptSearch

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

    print(f'Took {datetime.now()-start:} (s).')
    env.close()
    return tune.report(episode_reward=sum(rewards))

config = {
        # 'index': 3,

        # Default hyper parameters for nodes not trained.
        'defaults': {
            'alpha': 0.001,
            'beta': 5.0,
            'gamma': 200.0,
            'c': 1,
        },

        # 'alpha': tune.grid_search(np.log10(np.linspace(0.0005, 0.002, 15)).tolist()),
        # 'beta': tune.grid_search(np.log10(np.linspace(1, 10, 15)).tolist()),
        # 'gamma': tune.grid_search(np.log10(np.linspace(150, 250, 15)).tolist()),
        # 'c': tune.grid_search(np.log10(np.linspace(0.5, 10, 15)).tolist()),

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
        config=config,
        name='hyperparameter_check_bo',
        search_alg=BayesOptSearch(space={
            'alpha': (math.log10(0.00005), math.log10(0.02)),
            'beta': (math.log10(0.00001), math.log10(1.5)),
            'gamma': (math.log10(100), math.log10(300)),
            'c': (math.log10(0.001), math.log10(1)),
            }, metric="episode_reward", mode="max")
        )

    print("Best config: ", analysis.get_best_config(
        metric="episode_reward", mode="max"))

    print(analysis.results_df)