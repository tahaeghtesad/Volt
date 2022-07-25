import gym
import numpy as np

from envs.power.matlab_wrapper_single_param import MatlabWrapperEnvSingleParam


class MatlabWrapperAlphaGammaEnv(MatlabWrapperEnvSingleParam):
    def __init__(self, env_id, engine_pool, config):
        super().__init__(env_id, engine_pool, config)

        self.action_space = gym.spaces.Box(low=np.array([-0.5]),
                                           high=np.array([0.5]),
                                           shape=(1,))

        self.alpha = config['default_params']['alpha']
        self.beta = config['default_params']['beta']
        self.c = config['default_params']['c']

    def reset(self):
        return super().reset()

    def step(self, action: np.ndarray):
        gamma = action[0] - self.alpha
        return super().step(np.array([self.alpha, self.beta, gamma, self.c]))

    def close(self):
        super().close()

    def render(self, mode='human'):
        super().render(mode)
