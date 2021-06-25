import logging

import ray
from ray import tune
import ray.rllib.agents.ddpg as ddpg
from ray.tune import register_env
from ray.tune.logger import pretty_print
from tqdm import tqdm

from envs.power.thirteen_bus import ThirteenBus

register_env("volt", lambda config: ThirteenBus(config))

# tune.run(DDPGTrainer, config={"env": "volt",
#                               "log_level": "INFO",
#                               # 'buffer_size': 5000,
#                               "num_gpus": 0,
#                               "num_workers": 12,
#                               "framework": 'tfe'
#                               })

ray.init(
    # memory=8 * 1024 * 1024 * 1024,
    object_store_memory=16_000_000_000,
    # driver_object_store_memory=128 * 1024 * 124,
    # 'buffer_size': 5000,
    num_gpus=0,
    num_cpus=8,
    logging_level=logging.DEBUG,
)
config = ddpg.DEFAULT_CONFIG.copy()
config.update(dict(
    log_level=logging.INFO,
    framework='tfe',
    num_workers=7,
    num_gpus=0,
))

trainer = ddpg.DDPGTrainer(config=config, env='volt')

for i in tqdm(range(1000)):
    result = trainer.train()
    print(pretty_print(result))
    checkpoint = trainer.save()
    print(f'checkpoint saved at {checkpoint}')
