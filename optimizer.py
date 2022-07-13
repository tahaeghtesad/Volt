import numpy as np
import pandas as pd
import ray
from ray import tune
from ray.tune import Trainable
from ray.tune.suggest.bayesopt import BayesOptSearch
from ray.tune.utils.log import Verbosity

from config import env_config
from envs.remote.client import RemoteEnv
from util.env_util import get_rewards


class VC(Trainable):

    def __init__(self, config=None, logger_creator=None):
        super().__init__(config, logger_creator)
        self.env = RemoteEnv('localhost', 6985, self.config)

    def step(self):
        epoch_rewards = []

        for epoch in range(self.config['epochs']):
            states = []
            rewards = []
            next_states = []
            dones = []

            observation = self.env.reset()
            done = False

            while not done:

                new_obs, reward, done, info = self.env.step(np.array([
                        self.config['alpha'],
                        self.config['beta'],
                        self.config['gamma'],
                        self.config['c']]
                    ))

                states.append(observation)
                rewards.append(reward)
                next_states.append(new_obs)
                dones.append(done)

                observation = new_obs

            rewards = get_rewards(env_config, np.array(states), np.array(rewards))
            convergence_time = np.where(rewards == 1)[0]
            if len(np.where(rewards == 1)[0]) > 0:
                convergence_time = convergence_time[0]
            else:
                if len(np.where(rewards == -1)[0]) > 0:
                    convergence_time = 10 * env_config['T']
                else:
                    convergence_time = env_config['T']

            epoch_rewards.append(convergence_time)

        return dict(
            epoch_reward_min=np.min(epoch_rewards),
            epoch_reward_max=np.max(epoch_rewards),
            epoch_reward_mean=np.mean(epoch_rewards),
            epoch_reward_std=np.std(epoch_rewards),
            epoch_reward_q25=np.quantile(epoch_rewards, 0.25),
            epoch_reward_q75=np.quantile(epoch_rewards, 0.75),
        )

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
points_to_evaluate = [
    # dict(alpha=0.002, beta=0.5, gamma=100, c=1)
    dict(alpha=-2.69, beta=-0.3, gamma=2, c=0),
    dict(alpha=-1.6, beta=1.2, gamma=1.4, c=-1.7)
    # dict(alpha=-1.6145001260743783, beta=1.1579715364588790, gamma=1.4101386575517729, c=-1.730091534553142),
    # dict(alpha=math.log10(0.002), beta=math.log10(0.5), gamma=math.log10(100), c=math.log10(1)),
    # dict(alpha=-1.8364731991542713, beta=0.1779756936264951, gamma=1.5929615253821736, c=0.1865771965876492),
    # dict(alpha=-2.9193837505821483,  beta=2.9019963354642995,  gamma=0.1124016114593602, c=-0.9624645269455172),
]

# from the best of experiment state
# points_to_evaluate = read_experiment_state('/home/teghtesa/ray_results/hyperparameter_check_bo/experiment_state-2021-08-04_22-01-59.json', 24)


search_space = {
    'alpha': (env_config['range']['low'][0], env_config['range']['high'][0]),
    'beta': (env_config['range']['low'][1], env_config['range']['high'][1]),
    'gamma': (env_config['range']['low'][2], env_config['range']['high'][2]),
    'c': (env_config['range']['low'][3], env_config['range']['high'][3]),
}

if __name__ == '__main__':
    ray.init(num_cpus=8)
    pd.set_option("display.precision", 16)
    env_config.update()
    analysis = tune.run(
        VC,
        config=env_config,
        name='hyperparameter_check_bo_full_range',
        search_alg=BayesOptSearch(space=search_space,
                                  points_to_evaluate=points_to_evaluate,
                                  metric="epoch_reward_mean", mode="min", verbose=1, patience=64,
                                  random_search_steps=32),
        # scheduler=AsyncHyperBandScheduler(metric='reward', mode='max'),
        # scheduler=FIFOScheduler(),
        stop={
            'training_iteration': 1,
        },
        num_samples=512,
        reuse_actors=True,
        verbose=Verbosity.V3_TRIAL_DETAILS,
        resources_per_trial={'gpu': 1}
    )

    with open('log.log', 'a') as fd:
        fd.write(str(analysis.results_df.sort_values(by=['epoch_reward_mean'], ascending=True).head(64)[
                         ['config.alpha', 'config.beta', 'config.gamma', 'config.c',
                          'epoch_reward_mean', 'epoch_reward_std', 'epoch_reward_min', 'epoch_reward_max',
                          'epoch_reward_q25', 'epoch_reward_q75']]))

    analysis.results_df.sort_values(by=['epoch_reward_mean'], ascending=True).head(16)[
        ['config.alpha', 'config.beta', 'config.gamma', 'config.c',
         'epoch_reward_mean', 'epoch_reward_std', 'epoch_reward_min', 'epoch_reward_max',
         'epoch_reward_q25', 'epoch_reward_q75']].to_csv(
        f'hyperparameter_{env_config["system"]}_{env_config["mode"]}.csv')
