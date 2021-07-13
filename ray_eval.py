import ray
import ray.rllib.agents.ddpg as ddpg
from tqdm import tqdm

from envs.remote.client import RemoteEnv
from ray_train import config
import numpy as np
import os
import matplotlib.pyplot as plt

checkpoint_path = 'C:\\Users\\Taha\\ray_results\\DDPG_2021-07-09_17-27-33\\DDPG_volt_dab9d_00003_3_actor_hidden_activation=tanh,buffer_size=50000,critic_hidden_activation=tanh,final_scale=0.01,ou_base_scal_2021-07-09_17-28-37\\checkpoint_000350\\\\checkpoint-350'

assert os.path.exists(checkpoint_path + '.tune_metadata')

ray.init(address='auto', _redis_password='5241590000000000')


trainer = ddpg.DDPGTrainer(config={}, env='volt')
trainer.restore(checkpoint_path)

env = RemoteEnv('localhost', 6985, {})


for i in tqdm(range(100)):
    step = 0
    done = False
    obs = env.reset()

    values = {
        'alpha': [],
        'beta': [],
        'gamma': [],
        'c': [],
        'reward': []
    }

    while not done:
        action = trainer.compute_action(obs)

        values['alpha'].append(action[0])
        values['beta'].append(action[1])
        values['gamma'].append(action[2])
        values['c'].append(action[3])

        obs, reward, done, info = env.step(action)

        values['reward'].append(reward)

        step += 1

    # plt.plot(values['alpha'], label='$\\alpha$')
    # plt.plot(values['beta'], label='$\\beta$')
    # plt.plot(values['gamma'], label='$\\gamma$')
    # plt.plot(values['c'], label='$\\c$')
    plt.plot(values['reward'], label='$\\reward$')

    plt.show()

