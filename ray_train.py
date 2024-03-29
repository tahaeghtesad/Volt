import logging

import ray
import ray.rllib.agents.ppo as ppo
from ray import tune
from ray.rllib.agents.trainer import COMMON_CONFIG
from ray.rllib.models import MODEL_DEFAULTS
from ray.tune import register_env
import tensorflow as tf

from config import model_config, ppo_training_config, env_config, trainer_config
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


def set_gpu_memory_limit():
    try:
        physical_devices = tf.config.list_physical_devices('GPU')
        tf.config.set_logical_device_configuration(physical_devices[0], [tf.config.LogicalDeviceConfiguration(memory_limit=1024)])
    except:
        print("Couldn't set GPU memory limit!")


if __name__ == '__main__':

    set_gpu_memory_limit()

    try:
        ray.init(num_cpus=config['num_workers']+1)
        result = tune.run(
            ppo.PPOTrainer,
            config=config,
            checkpoint_freq=trainer_config['checkpoint_freq'],
            stop={
                'training_iteration': trainer_config['training_iteration']
            },
            checkpoint_at_end=True
        )
    except KeyboardInterrupt:
        ray.shutdown()
