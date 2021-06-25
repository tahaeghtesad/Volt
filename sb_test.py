from stable_baselines import DDPG
from stable_baselines.common.noise import NormalActionNoise
from stable_baselines.ddpg import LnMlpPolicy

from envs.power.thirteen_bus import ThirteenBus

import tensorflow as tf

env = ThirteenBus(None)


def get_policy_class(policy_params):
    # policy params must have 'act_fun' and 'layers'
    class CustomPolicy(LnMlpPolicy):
        def __init__(self, *args, **_kwargs):
            super().__init__(*args, **_kwargs, **policy_params)

    return CustomPolicy


def callback(locals_, globals_):
    self_ = locals_['self']

    # variables = ['u', 'x', 'dx', 'a', 'o', 'd']
    #
    # if 'info' in locals_:
    #     for var in variables:
    #         if var in locals_['info']:
    #             for i in range(len(locals_['info'][var])):
    #                 if 'writer' in locals_ and locals_['writer'] is not None:
    #                     summary = tf.Summary(
    #                         value=[tf.Summary.Value(tag=f'env/{var}{i}', simple_value=locals_['info'][var][i])])
    #                     locals_['writer'].add_summary(summary, self_.num_timesteps)

    return True


model = DDPG(
    policy=get_policy_class({
        'act_fun': tf.tanh,
        'layers': [128, 128, 128]
    }),
    env=env,
    action_noise=NormalActionNoise(0, 0.5),
    # gamma=0.99,
    verbose=2,
    tensorboard_log=f'tb_logs',
    full_tensorboard_log=True
)


model.learn(
            total_timesteps=1_000_000,
            callback=callback
        )