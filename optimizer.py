import math

import numpy as np
import pandas as pd
import ray
from ray import tune
from ray.tune import Trainable
from ray.tune.suggest.bayesopt import BayesOptSearch
from ray.tune.utils.log import Verbosity

from envs.remote.client import RemoteEnv
from config import env_config


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
points_to_evaluate = [dict(alpha=math.log10(0.002), beta=math.log10(0.5), gamma=math.log10(100), c=math.log10(1)),
                      dict(alpha=-1.8364731991542713, beta=0.1779756936264951, gamma=1.5929615253821736, c=0.1865771965876492),
                      dict(alpha=-1.6145001260743783, beta=1.1579715364588790, gamma=1.4101386575517729, c=-1.730091534553142)]

# from the best of experiment state
# points_to_evaluate = read_experiment_state('/home/teghtesa/ray_results/hyperparameter_check_bo/experiment_state-2021-08-04_22-01-59.json', 24)


search_space = {
    'alpha': (-env_config['search_range'], env_config['search_range']),
    'beta': (-env_config['search_range'], env_config['search_range']),
    'gamma': (-env_config['search_range'], env_config['search_range']),
    'c': (-env_config['search_range'], env_config['search_range']),
}

if __name__ == '__main__':
    ray.init(num_cpus=6)
    pd.set_option("display.precision", 16)
    analysis = tune.run(
        VC,
        config=env_config,
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
        verbose=Verbosity.V3_TRIAL_DETAILS
    )

    with open('log.log', 'a') as fd:
        fd.write(str(analysis.results_df.sort_values(by=['episode_reward'], ascending=False).head(30)[['config.alpha', 'config.beta', 'config.gamma', 'config.c', 'episode_reward']]))

    print(analysis.results_df.sort_values(by=['episode_reward'], ascending=False).head(30)[['config.alpha', 'config.beta', 'config.gamma', 'config.c', 'episode_reward']])