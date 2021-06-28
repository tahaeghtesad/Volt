import logging

import ray
from ray import tune
import ray.rllib.agents.ddpg as ddpg
from ray.tune import register_env
from ray.tune.logger import pretty_print
from tqdm import tqdm

from envs.remote.client import RemoteEnv

register_env("volt", lambda config: RemoteEnv('localhost', 6985, config))

config = ddpg.DEFAULT_CONFIG.copy()
config.update(dict(
    env='volt',
    log_level=logging.INFO,
    framework='tfe',
    num_workers=8,
    num_gpus=0,
))

tune.run(ddpg.DDPGTrainer, config=config)