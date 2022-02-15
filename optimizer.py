import math

import numpy as np
import ray
from ray import tune
from ray.tune import Trainable
from ray.tune.schedulers import FIFOScheduler, AsyncHyperBandScheduler
from ray.tune.suggest.bayesopt import BayesOptSearch
from tqdm import tqdm
import pandas as pd

from envs.remote.client import RemoteEnv

config = {
    'mode': 'all_control',
    'voltage_threshold': 0.05,

    # Search range around the default parameters
    'search_range': 5,

    # Length of history
    'history_size': 1,

    # Episode length
    'T': 1000,

    # Repeat
    'repeat': 1,

    'epochs': 1
}


class VC(Trainable):

    def __init__(self, config=None, logger_creator=None):
        super().__init__(config, logger_creator)
        self.env = RemoteEnv('localhost', 6985, self.config)

    def step(self):
        rewards = []

        for epoch in range(self.config['epochs']):
            obs = self.env.reset()
            done = False
            # for step in range(self.config['T'] // self.config['repeat']):
            while not done:
                # action = np.array([0, 0, 0, 0])
                # action = env.action_space.low
                # np.concatenate((
                #         alpha * np.ones(env.n),
                #         beta * np.ones(env.n),
                #         gamma * np.ones(env.n),
                #         c * np.ones(env.n),
                #     ))
                obs, reward, done, info = self.env.step(
                    np.repeat(np.array([self.config['alpha'], self.config['beta'], self.config['gamma'], self.config['c']]), self.env.n))

                # print(f'Step: {step} - Obs: {obs} - Action: {action} - Reward: {reward}')


                # obs, reward, done, info = env.step(10000 * np.random.random((4 * env.n,)) - 5000)
                # tune.report(reward=reward)
                rewards.append(reward)
                # tune.report(reward=reward, episode_reward=sum(rewards))

        return dict(episode_reward=sum(rewards)/self.config['epochs'])

    def reset_config(self, new_config):
        return True

    def setup(self, config):
        super().setup(config)

    def cleanup(self):
        self.env.close()


# These happened to be the best hyper-parameters. Reward: -0.785176
# points_to_evaluate = [
#     {'alpha': -2.6989700043360187, 'beta': 0.0, 'gamma': 2.2518119729937998, 'c': -0.3010299956639812},
#     {'alpha': -2.6989700043360187, 'beta': 0.3590219426416679, 'gamma': 2.2518119729937998, 'c': -0.3010299956639812},
#     {'alpha': -2.6989700043360187, 'beta': 0.5528419686577808, 'gamma': 2.2518119729937998, 'c': -0.3010299956639812}
# ]
points_to_evaluate = [dict(alpha=math.log10(0.002), beta=math.log10(0.5), gamma=math.log10(100), c=math.log10(1))]

# from the best of experiment state
# points_to_evaluate = read_experiment_state('/home/teghtesa/ray_results/hyperparameter_check_bo/experiment_state-2021-08-04_22-01-59.json', 24)


search_space = {
    'alpha': (-config['search_range'], config['search_range']),
    'beta': (-config['search_range'], config['search_range']),
    'gamma': (-config['search_range'], config['search_range']),
    'c': (-config['search_range'], config['search_range']),
}

if __name__ == '__main__':
    ray.init(num_cpus=6)
    analysis = tune.run(
        VC,
        config=config,
        name='hyperparameter_check_bo_full_range',
        search_alg=BayesOptSearch(space=search_space,
                                  points_to_evaluate=points_to_evaluate,
                                  metric="episode_reward", mode="max", verbose=0, random_search_steps=4),
        # scheduler=AsyncHyperBandScheduler(metric='reward', mode='max'),
        # scheduler=FIFOScheduler(),
        stop={
            'training_iteration': 1,
        },
        num_samples=512,
        reuse_actors=True,
        verbose=2
    )

    pd.set_option("display.precision", 16)
    with open('log.log', 'a') as fd:
        fd.write(str(analysis.results_df.sort_values(by=['episode_reward'], ascending=False).head(10)[['config.alpha', 'config.beta', 'config.gamma', 'config.c', 'episode_reward']]))

    print(analysis.results_df.sort_values(by=['episode_reward'], ascending=False).head(10)[['config.alpha', 'config.beta', 'config.gamma', 'config.c', 'episode_reward']])