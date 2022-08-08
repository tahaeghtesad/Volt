import logging
import sys

import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

from config import env_config

from envs.power.matlab_wrapper import MatlabWrapperEnv
from remote_server import ServerThread
from util.reusable_pool import ReusablePool

# alpha = np.log10(0.002)  # -2.69
# alpha = np.power(10, -9.0)
# beta = np.log10(0.5)  # -0.3
# beta = np.power(10, 1.2)
# gamma = np.log10(100)  # 2
# gamma = np.power(10, 1.3)
# c = np.log10(1)  # 0
# c = np.power(10, -1.7)

# alpha = -2
# beta = -0.3
# gamma = 2
# c = 0

# alpha = 0.002
# beta = 0.5
# gamma = 100
# c = 1

# alpha = -2
# beta = 1.2
# gamma = 1.4
# c = -1.7

# alpha=-3.780353565686756
# beta=-3.496333559465059
# gamma=2.751149427104263
# c=4.5921235667612805

alpha=-10
beta=-10
gamma=9.9
c=1.039414574158694


# alpha, beta, gamma, c = -2.8, -0.8, 1.2, 10

# alpha, beta, gamma, c = (-1.6145001260743783, 1.1579715364588790, 1.4101386575517729, -1.7300915345531420)
# alpha, beta, gamma, c = (-3.2027640280204990, 0.3850388369317503, 2.6828780880670804, -1.0737686447199004)

# best for ieee 123
# alpha, beta, gamma, c = (-1.6732751031990718, 0.2056065407251410, 0.9932268152460754, -2.2999999999999998)

# alpha, beta, gamma, c = (-10, )

engine_pool = ReusablePool(1, ServerThread.init_matlab, ServerThread.clean_matlab)
logging.basicConfig(stream=sys.stdout,
                    format='%(asctime)s - %(name)s - %(threadName)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

environment_config = env_config.copy()
environment_config.update({
    'system': 'ieee13',
    'mode': 'all_control',
    'T': 10,
    'reward_mode': 'steps',
    'load_var': 'dynamic',
    'repeat': 1,
})

env = MatlabWrapperEnv(1, engine_pool, env_config=environment_config)


if __name__ == '__main__':
    q_table = np.zeros((env.n, env.T // env.env_config['repeat']))
    v_table = np.zeros((env.n, env.T // env.env_config['repeat']))

    states = []

    obs = env.reset()
    done = False
    rewards = []
    fs = []
    cs = []
    fes = []
    vd = []
    pbar = tqdm(total=env.env_config['T'] // env.env_config['repeat'])
    # for step in range(env.T // env.env_config['repeat']):
    while not done:
        try:
            action = np.concatenate((
                alpha * np.ones(env.n),
                beta * np.ones(env.n),
                gamma * np.ones(env.n),
                c * np.ones(env.n),
            ))

            new_state, reward, done, info = env.step(action)

            states.append(obs)

            q_table[:, env.step_number - 1] = info['q'].reshape((env.n,))
            v_table[:, env.step_number - 1] = info['v'].reshape((env.n,))

            rewards.append(reward)
            fs.append(info['f'])
            vd.append(info['voltage_deviations'])

            fes.append(info['fes'])

            obs = new_state

            pbar.update(1)
            pbar.set_description(
                f'{sum(rewards):.2f}')
        except KeyboardInterrupt:
            break

    print(np.split(obs, 2)[0])

    pbar.close()

    fig, ax = plt.subplots()
    ax.set_title(f'a')
    ax.plot(alpha * np.ones(env.step_number), label='$\\alpha$')
    ax.plot(beta * np.ones(env.step_number), label='$\\beta$')
    ax.plot(gamma * np.ones(env.step_number), label='$\\gamma$')
    ax.plot(c * np.ones(env.step_number), label='$c$')
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
    ax.plot(rewards, '-o', label='reward')
    ax.plot(-np.array(vd), '-', label='voltage_deviations')
    ax.legend()
    ax.grid()
    fig.savefig('r.png')
    plt.show()

