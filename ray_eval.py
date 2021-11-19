import logging
import multiprocessing.pool
import os
import random
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
    destination = os.environ['TMPDIR'] + 'checkpoint' + f'{random.randint(1, 10000):06d}'
    print(f'Copying checkpoint file from {remote_path} to {destination}')
    os.system(f'scp teghtesa@rnslab2.hpcc.uh.edu:{remote_path} {destination}')
    os.system(f'scp teghtesa@rnslab2.hpcc.uh.edu:{remote_path}.tune_metadata {destination}.tune_metadata')
    print(f'Restoring trainer.')
    trainer = ppo.PPOTrainer(config=config, env=None)
    trainer.restore(destination)
    return trainer


register_env("volt", lambda config: RemoteEnv('localhost', 6985, config))

def eval_trainer(checkpoint):
    env = RemoteEnv('localhost', 6985, config=config['env_config'])
    trainer = load_trainer(f'~/ray_results/PPO_2021-11-18_16-46-03/PPO_volt_4ee23_00000_0_2021-11-18_16-46-03'
                 f'/checkpoint_000{checkpoint:03d}/checkpoint-{checkpoint}')

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
        action = np.zeros(4)
        reward = 0

        while not done:
            action = trainer.compute_single_action(obs, explore=False)
            # action_info = trainer.get_policy().compute_single_action(obs, prev_action=action, prev_reward=reward, explore=False)
            # action = action_info[0]
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
            # print(action_info[2]['vf_preds'], reward)

            step += 1

    fig, ax = plt.subplots()
    ax.set_title(f'Trainer {checkpoint}')
    ax.plot(values['alpha'], label='$\\alpha$')
    ax.plot(values['beta'], label='$\\beta$')
    ax.plot(values['gamma'], label='$\\gamma$')
    ax.plot(values['c'], label='$c$')
    ax.plot(values['reward'], label='$r$')
    ax.legend()
    logging.getLogger(f'Trainer_{checkpoint}').info(sum(values['reward']))
    env.close()


if __name__ == '__main__':
    ray.init(address='auto', _redis_password='5241590000000000')
    with multiprocessing.pool.ThreadPool(4) as p:
        p.map(eval_trainer, range(10, 101, 10))
    plt.show()
    # for checkpoint in [40, 50, 60, 70, 80, 90, 100]:
    #     eval_trainer(checkpoint)
