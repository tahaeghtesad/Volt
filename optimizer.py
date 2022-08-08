import multiprocessing.pool

import numpy as np
import pandas as pd
import ray
import pickle
import matplotlib.pyplot as plt
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
        return fitness(self.env,
                       self.config['alpha'],
                       self.config['beta'],
                       self.config['gamma'],
                       self.config['c'],
                       self.config['epochs'])

    def reset_config(self, new_config):
        return True

    def setup(self, config):
        super().setup(config)

    def cleanup(self):
        self.env.close()


class VCAlphaGamma(VC):

    def __init__(self, config=None, logger_creator=None):
        super().__init__(config, logger_creator)

    def step(self):
        return fitness(self.env,
                       -10.0,
                       -10.0,
                       self.config['ratio'] + 10.0,
                       4.039414574158694,
                       self.config['epochs'])


def get_trajectory(env, alpha, beta, gamma, c):

    states = []
    rewards = []
    next_states = []
    dones = []
    actions = []

    observation = env.reset()
    done = False

    while not done:
        action = np.array([
            alpha, beta, gamma, c
        ])
        new_obs, reward, done, info = env.step(action)

        states.append(observation)
        rewards.append(reward)
        next_states.append(new_obs)
        dones.append(done)
        actions.append(action)

        observation = new_obs

    rewards = get_rewards(env_config, np.array(states), np.array(rewards), dones)

    experiences = [dict(
        state=s,
        action=a,
        reward=r.numpy(),
        next_state=n,
        done=d
    ) for s, a, r, n, d in zip(states, actions, rewards, next_states, dones)]

    result = dict(
        status='',
        time=0,
        loading_condition=env.config['load_var'],
        alphagamma=alpha+gamma
    )

    convergence_time = np.where(rewards == 1)[0]
    if len(np.where(rewards == 1)[0]) > 0:
        convergence_time = convergence_time[0]
        result['status'] = 'converged'
        result['time'] = convergence_time
        experiences = experiences[:convergence_time + 1]
    else:
        if len(np.where(rewards == -1)[0]) > 0:
            result['status'] = 'diverged'
        else:
            result['status'] = 'running'

    return result, experiences


def fitness(envs, alpha, beta, gamma, c):
    print(f'Calculating fitness for alpha={alpha}, beta={beta}, gamma={gamma}, c={c}')

    with multiprocessing.pool.ThreadPool(processes=len(envs)) as pool:
        trajectories = pool.map(
            lambda env: get_trajectory(env, alpha, beta, gamma, c), envs)

    print(f'Converged Ratio: {sum([1 for t in trajectories if t[0]["status"] == "converged"])}/{env_config["epochs"]} - Average time: {np.mean([t[0]["time"] for t in trajectories if t[0]["status"] == "converged"])}')
    return pd.DataFrame([t[0] for t in trajectories]), [item for t in trajectories for item in t[1]]


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

search_space_ag = {
    'ratio': (-1, 1),
}


def main():
    ray.init(num_cpus=12)
    pd.set_option("display.precision", 16)
    env_config.update()
    analysis = tune.run(
        # VC,
        VCAlphaGamma,
        config=env_config,
        name='hyperparameter_check_bo_full_range',
        search_alg=BayesOptSearch(
            # space=search_space,
            space=search_space_ag,
            # points_to_evaluate=points_to_evaluate,
            metric="epoch_reward_mean", mode="min", verbose=1, patience=128,
            random_search_steps=8),
        # scheduler=AsyncHyperBandScheduler(metric='reward', mode='max'),
        # scheduler=FIFOScheduler(),
        stop={
            'training_iteration': 1,
        },
        num_samples=-1,
        reuse_actors=True,
        verbose=Verbosity.V3_TRIAL_DETAILS
    )
    # analysis.results_df.sort_values(by=['epoch_reward_mean'], ascending=True)[
    #     ['config.alpha', 'config.beta', 'config.gamma', 'config.c',
    #      'epoch_reward_mean', 'epoch_reward_std', 'epoch_reward_min', 'epoch_reward_max',
    #      'epoch_reward_q25', 'epoch_reward_q75']].to_csv(
    #     f'hyperparameter_{env_config["system"]}_{env_config["mode"]}.csv')

    analysis.results_df.sort_values(by=['epoch_reward_mean'], ascending=True)[
        ['config.ratio',
         'epoch_reward_mean']].to_csv(
        f'hyperparameter_{env_config["system"]}_{env_config["mode"]}_ratio.csv')


def plot():
    with multiprocessing.pool.ThreadPool(processes=env_config['epochs']) as pool:
        envs = pool.map(lambda loading: RemoteEnv('localhost', 6985, (lambda d: d.update(dict(load_var=loading)) or d)(env_config.copy())),
                        np.linspace(0.8, 1.2, env_config['epochs']))

    print('All envs created')
    n_points = 50
    ratios = np.linspace(-0.6, 0.6, n_points)
    trajectories = [fitness(envs, -10.0, -10.0, ratio + 10.0, 4.039414574158694) for ratio in ratios]

    results = pd.concat([t[0] for t in trajectories])
    experiences = [item for t in trajectories for item in t[1]]
    results.to_csv(f'hyperparameter_{env_config["system"]}_{env_config["mode"]}_results.csv')
    pickle.dump(experiences, open(f'hyperparameter_{env_config["system"]}_{env_config["mode"]}_experiences.pkl', 'wb'))


if __name__ == '__main__':
    plot()
