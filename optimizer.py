import math
import time
from datetime import datetime

import ray
from ray import tune
import numpy as np
from ray.tune.schedulers import AsyncHyperBandScheduler
from ray.tune.suggest.bayesopt import BayesOptSearch

from envs.remote.client import RemoteEnv
from read_experiment_state import read_experiment_state

config = {
    # 'index': 3,
    'voltage_threshold': 0.05,
    'power_injection_cost': 0.25,

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
    'T': 3000,

    # Repeat
    'repeat': 1
}


def eval(config):
    env = RemoteEnv('localhost', 6985, config)

    rewards = []

    for i in range(config['repeat']):
        obs = env.reset()
        done = False
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

    env.close()
    avg_reward = sum(rewards) / len(rewards)
    return tune.report(avg_reward=avg_reward)


# These happened to be the best hyper-parameters. Reward: -0.785176
# points_to_evaluate = [
#     {'alpha': -2.6989700043360187, 'beta': 0.0, 'gamma': 2.2518119729937998, 'c': -0.3010299956639812},
#     {'alpha': -2.6989700043360187, 'beta': 0.3590219426416679, 'gamma': 2.2518119729937998, 'c': -0.3010299956639812},
#     {'alpha': -2.6989700043360187, 'beta': 0.5528419686577808, 'gamma': 2.2518119729937998, 'c': -0.3010299956639812}
# ]

# from the best of experiment state
# points_to_evaluate = read_experiment_state('/home/teghtesa/ray_results/hyperparameter_check_bo/experiment_state-2021-08-04_22-01-59.json', 24)


search_space = {
    'alpha': (-config['search_range'], config['search_range']),
    'beta': (-config['search_range'], config['search_range']),
    'gamma': (-config['search_range'], config['search_range']),
    'c': (-config['search_range'], config['search_range']),
}

if __name__ == '__main__':
    ray.init(num_cpus=12)
    analysis = tune.run(
        eval,
        config=config,
        name='hyperparameter_check_bo_full_range',
        search_alg=BayesOptSearch(space=search_space,
                                  # points_to_evaluate=points_to_evaluate,
                                  metric="avg_reward", mode="max", verbose=1, random_search_steps=12),
        scheduler=AsyncHyperBandScheduler(metric='avg_reward', mode='max'),
        num_samples=1440,
    )

    print("Best config: ", analysis.get_best_config(
        metric="avg_reward", mode="max"))

    print(analysis.results_df)
