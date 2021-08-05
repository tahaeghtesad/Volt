import logging

import ray
import ray.rllib.agents.ppo as ppo
from ray import tune
from ray.rllib.agents import DefaultCallbacks
from ray.rllib.agents.trainer import COMMON_CONFIG
from ray.rllib.evaluation.collectors.simple_list_collector import SimpleListCollector
from ray.tune import register_env
from ray.tune.stopper import MaximumIterationStopper

from envs.remote.client import RemoteEnv

register_env("volt", lambda config: RemoteEnv('localhost', 6985, config))

config = dict()

config.update(COMMON_CONFIG)
config.update(ppo.DEFAULT_CONFIG)

# My config!
config.update({

    'env': 'volt',
    'env_config': {
        # Index of trained node -> [0, env.n]
        # 'index': 0,

        # Default hyper parameters for nodes not trained.
        'defaults': {
            'alpha': 0.001,
            'beta': 5.0,
            'gamma': 200.0,
            'c': 1,
        },

        # Search range around the default parameters
        'search_range': 5,

        # Length of history
        'history_size': 1,

        # Episode length
        'T': 350,
    },

    "lr": 5e-5,

    "num_workers": 12,
    # Whether to compute priorities on workers.

    # Number of GPU
    "num_gpus": 1 / 1,

    'log_level': logging.INFO
})

if __name__ == '__main__':
    try:
        result = tune.run(
            ppo.PPOTrainer,
            # stop=TrialPlateauStopper(metric='episode_reward_mean', std=0.01, num_results=100, grace_period=500_000),
            stop=MaximumIterationStopper(1500),
            config=config,
            checkpoint_freq=10,
            checkpoint_at_end=True
        )
    except KeyboardInterrupt:
        ray.shutdown()
