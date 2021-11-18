import logging
import os
import sys

import matplotlib.pyplot as plt
import numpy as np
import ray
import ray.rllib.agents.ppo as ppo
from ray.rllib.agents.trainer import COMMON_CONFIG
from ray.tune import register_env
from tqdm import tqdm

from envs.remote.client import RemoteEnv

logging.basicConfig(stream=sys.stdout, format='%(asctime)s - %(name)s - %(threadName)s - %(levelname)s - %(message)s', level=logging.INFO)

config = dict()

config.update(COMMON_CONFIG)
config.update(ppo.DEFAULT_CONFIG)

# My config!
config.update({

    'env': 'volt',
    'env_config': {
        # Index of trained node -> [0, env.n]
        # 'index': 0,
        'voltage_threshold': 0.05,
        # 'power_injection_cost': 0.2,

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
        'T': 10,
        'repeat': 1,
    },

    # "lr": 5e-5,

    # Clip param for the value function. Note that this is sensitive to the
    # scale of the rewards. If your expected V is large, increase this.
    # "vf_clip_param": 400.0,

    "num_workers": 1,

    # Number of GPU
    # "num_gpus": 1 / 1,

    'log_level': logging.INFO,

    'evaluation_config': {
        'explore': False
    },

    'explore': False,
})


def load_trainer(remote_path):
    destination = os.environ['TMPDIR'] + 'checkpoint'
    print(f'Copying checkpoint file from {remote_path} to {destination}')
    os.system(f'scp teghtesa@rnslab2.hpcc.uh.edu:{remote_path} {destination}')
    os.system(f'scp teghtesa@rnslab2.hpcc.uh.edu:{remote_path}.tune_metadata {destination}.tune_metadata')
    print(f'Restoring trainer.')
    trainer = ppo.PPOTrainer(config=config, env=None)
    trainer.restore(destination)
    return trainer


register_env("volt", lambda config: RemoteEnv('localhost', 6985, config))
remote_path = '~/ray_results/PPO_2021-11-17_16-54-17/PPO_volt_4b36b_00000_0_2021-11-17_16-54-17/checkpoint_000092/checkpoint-92'

ray.init(address='auto', _redis_password='5241590000000000')

env = RemoteEnv('localhost', 6985, config=config['env_config'])
trainer = load_trainer(remote_path)

values = {
    'alpha': [],
    'beta': [],
    'gamma': [],
    'c': [],
    'reward': []
}

for i in tqdm(range(1)):
    step = 0
    done = False
    obs = env.reset()

    while not done:
        action = trainer.compute_single_action(obs, explore=False)
        # action = trainer.get_policy()
        print(np.power(10, action))
        # action = np.log10(np.array([config['env_config']['defaults']['alpha'],
        #                             config['env_config']['defaults']['beta'],
        #                             config['env_config']['defaults']['gamma'],
        #                             config['env_config']['defaults']['c']]))

        values['alpha'].append(action[0])
        values['beta'].append(action[1])
        values['gamma'].append(action[2])
        values['c'].append(action[3])

        obs, reward, done, info = env.step(action)

        values['reward'].append(reward)

        step += 1


plt.plot(values['alpha'], label='$\\alpha$')
plt.plot(values['beta'], label='$\\beta$')
plt.plot(values['gamma'], label='$\\gamma$')
plt.plot(values['c'], label='$c$')
plt.plot(values['reward'], label='$r$')
plt.legend()
plt.show()
env.close()

