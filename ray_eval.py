import ray
import ray.rllib.agents.ddpg as ddpg
from tqdm import tqdm

from envs.remote.client import RemoteEnv
from ray_train import config
import numpy as np
import os
import matplotlib.pyplot as plt

# checkpoint_path = 'C:\\Users\\Taha\\ray_results\\DDPG_2021-07-09_17-27-33\\DDPG_volt_dab9d_00003_3_actor_hidden_activation=tanh,buffer_size=50000,critic_hidden_activation=tanh,final_scale=0.01,ou_base_scal_2021-07-09_17-28-37\\checkpoint_000350\\\\checkpoint-350'

# assert os.path.exists(checkpoint_path + '.tune_metadata')

# ray.init(address='auto', _redis_password='5241590000000000')

config = {
    'index': 3,

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
    'T': 500,
}


# trainer = ddpg.DDPGTrainer(config=config, env='volt')
# trainer.restore(checkpoint_path)

env = RemoteEnv('localhost', 6985, config=config)


for i in tqdm(range(1)):
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
        # action = trainer.compute_action(obs, explore=False)
        action = np.log10(np.array([config['defaults']['alpha'], config['defaults']['beta'], config['defaults']['gamma'], config['defaults']['c']]))

        values['alpha'].append(action[0])
        values['beta'].append(action[1])
        values['gamma'].append(action[2])
        values['c'].append(action[3])

        obs, reward, done, info = env.step(action)

        values['reward'].append(-reward * reward)

        step += 1

    # plt.plot(values['alpha'], label='$\\alpha$')
    # plt.plot(values['beta'], label='$\\beta$')
    # plt.plot(values['gamma'], label='$\\gamma$')
    # plt.plot(values['c'], label='$\\c$')
    plt.plot(values['reward'], label='$\\reward$')

    print(sum(values['reward']))
    plt.show()
    env.close()

