from ray import tune
from ray.rllib.agents.ddpg import DDPGTrainer
import envs.power
from envs.power.thirteen_bus import ThirteenBus
from ray.tune.registry import register_env

register_env("volt", lambda config: ThirteenBus(config))

tune.run(DDPGTrainer, config={"env": "volt",
                              "log_level": "INFO",
                              # 'buffer_size': 5000,
                              "num_gpus": 0,
                              "num_workers": 15,
                              "framework": 'tfe'
                              })

