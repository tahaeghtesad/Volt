import logging

import ray
import ray.rllib.agents.ppo as ppo
from ray import tune
from ray.rllib.agents.trainer import COMMON_CONFIG
from ray.tune import register_env

from envs.remote.client import RemoteEnv

register_env("volt", lambda config: RemoteEnv('localhost', 6985, config))

config = dict()

config.update(COMMON_CONFIG)
config.update(ppo.DEFAULT_CONFIG)

# My config!
config.update({

    'env': 'volt',
    'env_config': {
        'mode': 'all_control',
        'voltage_threshold': 0.05,

        # Search range around the default parameters
        'search_range': 4,

        # Length of history
        'history_size': 1,

        # Episode length
        'T': 400,
        'repeat': 10,
        'window_size': 10,

        'q_slope_threshold': 1e-2,
    },

    # "lr": 5e-5,

    # Clip param for the value function. Note that this is sensitive to the
    # scale of the rewards. If your expected V is large, increase this.
    # "vf_clip_param": 400.0,

    "gamma": 0.9,

    "num_workers": 6,

    # Number of GPU
    "num_gpus": 1 / 1,

    'log_level': logging.INFO
})

if __name__ == '__main__':
    try:
        ray.init(num_cpus=config['num_workers'] * config['num_gpus'])
        result = tune.run(
            ppo.PPOTrainer,
            stop={
                    "episode_reward_min": -150
            },
            # stop=MaximumIterationStopper(100),
            config=config,
            checkpoint_freq=1,
            checkpoint_at_end=True
        )
    except KeyboardInterrupt:
        ray.shutdown()
