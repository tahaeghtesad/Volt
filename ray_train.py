import logging

import ray
import ray.rllib.agents.ppo as ppo
from ray import tune
from ray.rllib.agents.trainer import COMMON_CONFIG
from ray.tune import register_env
from ray.rllib.models import MODEL_DEFAULTS

from envs.remote.client import RemoteEnv

register_env("volt", lambda config: RemoteEnv('localhost', 6985, config))

model = MODEL_DEFAULTS.copy()
config = dict()

config.update(COMMON_CONFIG)
config.update(ppo.DEFAULT_CONFIG)
# model.update({
#     "fcnet_hiddens": [25, 25, 25]
# })


# My config!
config.update({

    'env': 'volt',
    'env_config': {
        'mode': 'all_control',
        'voltage_threshold': 0.05,

        # Search range around the default parameters
        'search_range': 2.3,

        # Length of history
        'history_size': 1,

        # Episode length
        'T': 2500,
        'repeat': 10,
        'window_size': 10,

        'change_threshold': 0.20,
    },

    "model": model,

    # "lr": 5e-5,

    "normalize_actions": True,

    "rollout_fragment_length": 128,

    "batch_mode": "complete_episodes",

    "train_batch_size": 350,

    # Clip param for the value function. Note that this is sensitive to the
    # scale of the rewards. If your expected V is large, increase this.
    # "vf_clip_param": 400.0,

    # "vf_loss_coeff": 0.1,

    "gamma": 0.93,

    "num_workers": 9,

    # Number of GPU
    "num_gpus": 1 / 1,

    'log_level': logging.INFO
})

if __name__ == '__main__':
    try:
        ray.init(num_cpus=config['num_workers']+1)
        result = tune.run(
            ppo.PPOTrainer,
            config=config,
            checkpoint_freq=50,
            checkpoint_at_end=True
        )
    except KeyboardInterrupt:
        ray.shutdown()
