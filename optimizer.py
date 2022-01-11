import math

import numpy as np
import ray
from ray import tune
from ray.tune import Trainable
from ray.tune.schedulers import FIFOScheduler, AsyncHyperBandScheduler
from ray.tune.suggest.bayesopt import BayesOptSearch

from envs.remote.client import RemoteEnv

config = {
    # 'index': 3,
    'voltage_threshold': 0.05,

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
    'T': 20,

    # Repeat
    'repeat': 1,

    'epochs': 30
}


class VC(Trainable):

    def __init__(self, config=None, logger_creator=None):
        super().__init__(config, logger_creator)
        self.env = RemoteEnv('localhost', 6985, self.config)

    def step(self):
        rewards = []

        obs = self.env.reset()
        done = False
        for epoch in range(self.config['epochs']):
            for step in range(self.config['T']):
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
points_to_evaluate = [dict(alpha=math.log10(0.001), beta=math.log10(5), gamma=math.log10(200), c=math.log10(1))]

# from the best of experiment state
# points_to_evaluate = read_experiment_state('/home/teghtesa/ray_results/hyperparameter_check_bo/experiment_state-2021-08-04_22-01-59.json', 24)


search_space = {
    'alpha': (-config['search_range'], config['search_range']),
    'beta': (-config['search_range'], config['search_range']),
    'gamma': (-config['search_range'], config['search_range']),
    'c': (-config['search_range'], config['search_range']),
}

if __name__ == '__main__':
    ray.init(num_cpus=4)
    analysis = tune.run(
        VC,
        config=config,
        name='hyperparameter_check_bo_full_range',
        search_alg=BayesOptSearch(space=search_space,
                                  points_to_evaluate=points_to_evaluate,
                                  metric="episode_reward", mode="max", verbose=1, random_search_steps=12),
        # scheduler=AsyncHyperBandScheduler(metric='reward', mode='max'),
        # scheduler=FIFOScheduler(),
        stop={
            'training_iteration': 1,
        },
        num_samples=-1,
        reuse_actors=True,
    )

    print("Best config: ", analysis.get_best_config(
        metric="episode_reward", mode="max"))

    print(analysis.results_df)
