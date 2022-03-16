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

logging.basicConfig(stream=sys.stdout, format='%(asctime)s - %(name)s - %(threadName)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

config = dict()

config.update(COMMON_CONFIG)
config.update(ppo.DEFAULT_CONFIG)

# My config!
config.update({

    'env': 'volt',
    'env_config': {

        'mode': 'all_control',

        'voltage_threshold': 0.05,
        # 'power_injection_cost': 0.2,

        # Search range around the default parameters
        'search_range': 3,

        # Length of history
        'history_size': 1,

        # Episode length
        'T': 3500,

        'repeat': 10,

        'window_size': 10,

        'change_threshold': 0.2,

        'reward_mode': 'steps',
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
    # destination = '/tmp/' + 'checkpoint' + f'{random.randint(1, 10000):06d}'
    # print(f'Copying checkpoint file from {remote_path} to {destination}')
    # os.system(f'scp teghtesa@rnslab2.hpcc.uh.edu:{remote_path} {destination}')
    # os.system(f'scp teghtesa@rnslab2.hpcc.uh.edu:{remote_path}.tune_metadata {destination}.tune_metadata')
    print(f'Restoring trainer.')
    trainer = ppo.PPOTrainer(config=config, env=None)
    trainer.restore(remote_path)
    return trainer


register_env("volt", lambda config: RemoteEnv('localhost', 6985, config))


def eval_trainer(checkpoint):
    env = RemoteEnv('localhost', 6985, config=config['env_config'])
    trainer = load_trainer(
        f'/home/teghtesa/ray_results/'
        # f'PPO_2022-03-08_17-47-41/PPO_volt_24e5a_00000_0_2022-03-08_17-47-41'
        f'PPO_2022-03-10_11-41-05/PPO_volt_4320a_00000_0_2022-03-10_11-41-06'
        f'/checkpoint_{checkpoint:06d}/checkpoint-{checkpoint}')

    values = {
        'alpha': [],
        'beta': [],
        'gamma': [],
        'c': [],
        'reward': []
    }
    q_table = np.zeros((env.n, env.T // config['env_config']['repeat']))
    v_table = np.ones((env.n, env.T // config['env_config']['repeat']))

    fs = []
    cs = []
    vd = []

    for i in range(1):
        step = 0
        done = False
        obs = env.reset()
        action = np.zeros(4)
        reward = 0
        pbar = tqdm(total=config['env_config']['T']/config['env_config']['repeat'])

        # for step in range(env.T // config['env_config']['repeat']):
        while not done:
            # if step < 4:
            #     action = np.log10(np.array(list(config['env_config']['defaults'].values())))
            # else:
            action = trainer.compute_single_action(obs, unsquash_action=True, clip_action=False, explore=True)
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
            # print(f'obs: {obs}')
            # print(f'reward: {reward}')
            q_table[:, env.step_number - 1] = info['q'].reshape((env.n,))
            v_table[:, env.step_number - 1] = info['v'].reshape((env.n,))
            # print(f'action: {action}')

            values['reward'].append(reward)
            # print(action_info[2]['vf_preds'], reward)

            fs.append(info['f'])
            cs.append(info['changes'])
            vd.append(info['voltage_deviations'])

            step += 1
            pbar.update(1)

    fig, ax = plt.subplots()
    ax.set_title(f'a')
    ax.plot(values['alpha'], label='$\\alpha$')
    ax.plot(values['beta'], label='$\\beta$')
    ax.plot(values['gamma'], label='$\\gamma$')
    ax.plot(values['c'], label='$c$')
    ax.grid()
    ax.legend()
    fig.savefig('a.png')

    fig, ax = plt.subplots()
    ax.set_title('q')
    ax.plot(q_table.T[:env.step_number, :])
    ax.grid()
    fig.savefig('q.png')

    fig, ax = plt.subplots()
    ax.set_title('v')
    ax.plot(v_table.T[:env.step_number, :])
    ax.grid()
    fig.savefig('v.png')

    fig, ax = plt.subplots()
    ax.set_title('r')
    ax.plot(values['reward'], '-o', label='converged')
    ax.plot(-np.array(cs), '-', label='changes')
    ax.plot(-np.array(vd), '-', label='voltage_deviations')
    # ax.plot(0.1 * np.ones(len(vd)), '-', label='0.1')
    ax.legend()
    ax.grid()
    fig.savefig('r.png')

    logging.getLogger(f'Trainer_{checkpoint}').info(sum(values['reward']))
    env.close()


if __name__ == '__main__':
    ray.init(num_cpus=1)
    # with multiprocessing.pool.ThreadPool(4) as p:
    #     p.map(eval_trainer, range(10, 101, 10))
    # eval_trainer(5500)
    eval_trainer(150)
    plt.show()
    # for checkpoint in [40, 50, 60, 70, 80, 90, 100]:
    #     eval_trainer(checkpoint)
