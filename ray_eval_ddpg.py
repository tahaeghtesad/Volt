import logging
import sys

import matplotlib.pyplot as plt
import numpy as np
import ray
import ray.rllib.agents.ddpg as ddpg
from ray.rllib.agents.trainer import COMMON_CONFIG
from ray.rllib.models import MODEL_DEFAULTS
from ray.tune import register_env
from tqdm import tqdm

from config import model_config, ppo_training_config, env_config, ddpg_training_config
from envs.remote.client import RemoteEnv

logging.basicConfig(stream=sys.stdout, format='%(asctime)s - %(name)s - %(threadName)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

model = MODEL_DEFAULTS.copy()
config = dict()

config.update(COMMON_CONFIG)
config.update(ddpg.DEFAULT_CONFIG)

model.update(model_config)
config.update(ddpg_training_config)
# model.update({
#     'fcnet_hiddens': [512, 512],
# })

environment_config = dict()
environment_config.update(env_config)
environment_config.update({
    'system': 'ieee13',
    'mode': 'all_control',
    'reward_mode': 'steps'
})

config.update({

    'env': 'volt',
    'env_config': environment_config,

    "num_workers": 1,

    "num_gpus": 1 / 1,

    'log_level': logging.INFO,

    "normalize_actions": True,

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
    trainer = ddpg.DDPGTrainer(config=config, env=None)
    trainer.restore(remote_path)
    return trainer


register_env("volt", lambda config: RemoteEnv('localhost', 6985, config))


def eval_trainer():
    checkpoint = 368
    env = RemoteEnv('localhost', 6985, config=config['env_config'])
    trainer = load_trainer(
        f'/home/teghtesa/ray_results/'
        f'DDPGTrainer_2022-06-10_12-59-15/DDPGTrainer_volt_0ab15_00000_0_2022-06-10_12-59-15'
        f'/checkpoint_{checkpoint:06d}/checkpoint-{checkpoint}')

    values = {
        'alpha': [],
        'beta': [],
        'gamma': [],
        'c': [],
        'reward': []
    }
    q_table = np.zeros((config['env_config']['epochs'], env.n, env.T // config['env_config']['repeat']))
    v_table = np.ones((config['env_config']['epochs'], env.n, env.T // config['env_config']['repeat']))

    fs = []
    cs = []
    vd = []

    reward_list = []

    for i in tqdm(range(config['env_config']['epochs'])):
        step = 0
        done = False
        obs = env.reset()
        action = np.zeros(4)
        reward = 0

        rewards = 0

        # for step in range(env.T // config['env_config']['repeat']):
        while not done:
            try:
                # if step < 4:
                #     action = np.log10(np.array(list(config['env_config']['defaults'].values())))
                # else:
                action = trainer.compute_single_action(obs, unsquash_action=True, clip_action=True, explore=False)
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
                rewards += reward
                # print(f'obs: {obs}')
                # print(f'reward: {reward}')
                q_table[i, :, env.step_number - 1] = info['q'].reshape((env.n,))
                v_table[i, :, env.step_number - 1] = info['v'].reshape((env.n,))
                # print(f'action: {action}')

                values['reward'].append(reward)
                # print(action_info[2]['vf_preds'], reward)

                fs.append(info['f'])
                cs.append(info['changes'])
                vd.append(info['voltage_deviations'])

                step += 1
            except KeyboardInterrupt:
                break

        reward_list.append(rewards)

    reward_list = np.array(reward_list)

    print(dict(
        epoch_reward_min=np.min(reward_list),
        epoch_reward_max=np.max(reward_list),
        epoch_reward_mean=np.mean(reward_list),
        epoch_reward_std=np.std(reward_list),
        epoch_reward_q25=np.quantile(reward_list, 0.25),
        epoch_reward_q75=np.quantile(reward_list, 0.75),
    ))


    q_table = np.concatenate([q_table[i, :, :].T[:env.step_number, :] for i in range(config['env_config']['epochs'])], axis=1)

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
    ax.plot(values['reward'], '-o', label='reward')
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

    eval_trainer()
    plt.show()
    # for checkpoint in [40, 50, 60, 70, 80, 90, 100]:
    #     eval_trainer(checkpoint)
