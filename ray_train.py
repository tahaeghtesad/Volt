import logging

import ray
import ray.rllib.agents.ppo as ppo
from ray import tune
from ray.rllib.agents.trainer import COMMON_CONFIG
from ray.rllib.models import MODEL_DEFAULTS
from ray.tune import register_env

from config import model_config, ppo_training_config, env_config
from envs.remote.client import RemoteEnv

register_env("volt", lambda config: RemoteEnv('localhost', 6985, config))

model = MODEL_DEFAULTS.copy()
config = dict()

config.update(COMMON_CONFIG)
config.update(ppo.DEFAULT_CONFIG)

model.update(model_config)
config.update(ppo_training_config)

# My config!
config.update({

    'env': 'volt',
    'env_config': env_config,
    "model": model,

    "num_workers": 16,

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
            checkpoint_freq=10,
            stop={
                'training_iteration': 200,
            },
            checkpoint_at_end=True
        )
    except KeyboardInterrupt:
        ray.shutdown()
