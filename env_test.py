import logging
import sys

import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt

from envs.power.onetwentythree_bus import OneTwentyThreeBus

# Data.alpha = 0.001*ones(n,1);
# Data.beta = 5*ones(n,1);
# Data.gamma = 200*ones(n,1);
# Data.c=1*ones(n,1);
from envs.power.thirteen_bus import ThirteenBus
from remote_server import ServerThread
from util.reusable_pool import ReusablePool

# alpha = np.log10(0.002)
# beta = np.log10(0.5)
# gamma = np.log10(100)
# c = np.log10(1)


# alpha = 10 ** -4.069457373049808
# beta = 10 ** 3.9795074542061593
# gamma = 10 ** 3.507641819850809
# c = 10 ** 1.0328233759129137

# alpha, beta, c, gamma = {'alpha': -2.2329853389581658, 'beta': 0.12929655914177918, 'c': 0.25154342834675436, 'gamma': 2.3418920409325708}.values()
# alpha, beta, gamma, c = (-1., 3.041845, 1.963370, 0.488047)
# alpha, beta, gamma, c =  (-4.7603732969850086, -5.0000000000000000,  3.1174591404670213,  1.5842818460532611)
# alpha, beta, gamma, c = (-1.6145001260743783, 1.1579715364588790, 1.4101386575517729, -1.730091534553142)
# alpha, beta, gamma, c = (1e-2, 1e0, 1e1, 1e-2)
alpha, beta, gamma, c = (-1.6145001260743783, 1.1579715364588790, 1.4101386575517729, -1.7300915345531420)

engine_pool = ReusablePool(1, ServerThread.init_matlab, ServerThread.clean_matlab)
logging.basicConfig(stream=sys.stdout,
                    format='%(asctime)s - %(name)s - %(threadName)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

env = ThirteenBus(engine_pool, env_config={
    'mode': 'all_control',
    'search_range': 2.3,
    'voltage_threshold': 0.05,
    'T': 3500,
    'repeat': 10,
    'window_size': 10,
    'change_threshold': 0.2,
    'reward_mode': 'steps'
})

rs = []

if __name__ == '__main__':
    for epoch in range(1):
        q_table = np.zeros((env.n, env.T // env.env_config['repeat']))
        v_table = np.zeros((env.n, env.T // env.env_config['repeat']))
        v_c_table = np.zeros((env.n, env.T // env.env_config['repeat']))
        lambda_bar_table = np.zeros((env.n, env.T // env.env_config['repeat']))
        lambda_un_table = np.zeros((env.n, env.T // env.env_config['repeat']))
        xi_table = np.zeros((env.n, env.T // env.env_config['repeat']))
        q_hat_table = np.zeros((env.n, env.T // env.env_config['repeat']))

        _ = env.reset()
        done = False
        rewards = []
        fs = []
        cs = []
        fes = []
        vd = []
        pbar = tqdm(total=env.env_config['T'] / env.env_config['repeat'])
        # for step in tqdm(range(env.T // env.env_config['repeat'])):
        while not done:
            _, reward, done, info = env.step(np.concatenate((
                alpha * np.ones(env.n),
                beta * np.ones(env.n),
                gamma * np.ones(env.n),
                c * np.ones(env.n),
            )))

            q_table[:, env.step_number - 1] = info['q'].reshape((env.n,))
            v_table[:, env.step_number - 1] = info['v'].reshape((env.n,))
            v_c_table[:, env.step_number - 1] = info['v_c'].reshape((env.n,))
            lambda_bar_table[:, env.step_number - 1] = info['lambda_bar'].reshape((env.n,))
            lambda_un_table[:, env.step_number - 1] = info['lambda_un'].reshape((env.n,))
            xi_table[:, env.step_number - 1] = info['xi'].reshape((env.n,))
            q_hat_table[:, env.step_number - 1] = info['q_hat'].reshape((env.n,))

            rewards.append(reward)
            fs.append(info['f'])
            cs.append(info['changes'])
            vd.append(info['voltage_deviations'])

            fes.append(info['fes'])

            pbar.update(1)

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
        ax.plot(rewards, '-o', label='converged')
        ax.plot(-np.array(cs), '-', label='changes')
        ax.plot(-np.array(vd), '-', label='voltage_deviations')
        # ax.plot(0.1 * np.ones(len(vd)), '-', label='0.1')
        ax.legend()
        ax.grid()
        fig.savefig('r.png')

        # plt.title('f')
        # plt.plot(fs[:-1])
        # plt.savefig('f.png')
        # plt.show()

        # plt.title('fes')
        # plt.plot(fes[:-1])
        # plt.savefig('fes.png')
        # plt.show()

        # plt.title('q_hat')
        # plt.plot(q_hat_table.T[1:-1, :])
        # plt.savefig('q_hat.png')
        # plt.show()
        #
        # plt.title('lambda_bar')
        # plt.plot(lambda_bar_table.T[1:-1, :])
        # plt.savefig('lambda_bar.png')
        # plt.show()
        #
        # plt.title('lambda_un')
        # plt.plot(np.clip(lambda_un_table.T[1:-1, :], None, 2))
        # plt.savefig('lambda_un.png')
        # plt.show()
        #
        # plt.title('xi')
        # plt.plot(xi_table.T[1:-1, :])
        # plt.savefig('xi.png')
        # plt.show()
        #
        # plt.title('v_c')
        # plt.plot(v_c_table.T[1:-1, :])
        # plt.savefig('v_c.png')
        # plt.show()
        plt.show()

        print(sum(rewards))
        rs.append(sum(rewards))

    print(sum(rs) / len(rs))
