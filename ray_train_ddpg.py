import logging

import ray
import ray.rllib.agents.ddpg as ddpg
from ray import tune
from ray.rllib.agents.trainer import COMMON_CONFIG
from ray.rllib.models import MODEL_DEFAULTS
from ray.tune import register_env

from config import model_config, env_config, trainer_config, ddpg_training_config
from envs.remote.client import RemoteEnv

register_env("volt", lambda config: RemoteEnv('localhost', 6985, config))

model = MODEL_DEFAULTS.copy()
config = dict()

config.update(COMMON_CONFIG)
config.update(ddpg.DEFAULT_CONFIG)

model.update(model_config)
config.update(ddpg_training_config)

# My config!
config.update({

    'env': 'volt',
    'env_config': env_config,
    # "model": model,

    "num_workers": 10,

    # Number of GPU
    "num_gpus": 1 / 1,

    'log_level': logging.INFO
})


if __name__ == '__main__':

    try:
        ray.init(num_cpus=config['num_workers']+1)
        result = tune.run(
            ddpg.DDPGTrainer,
            config=config,
            checkpoint_freq=trainer_config['checkpoint_freq'],
            stop={
                'training_iteration': trainer_config['training_iteration']
            },
            checkpoint_at_end=True
        )
    except KeyboardInterrupt:
        ray.shutdown()
