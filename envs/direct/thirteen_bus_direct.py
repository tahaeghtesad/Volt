import logging
import math

import gym
import opendssdirect as dss
import numpy as np


class ThirteenBusDirect(gym.Env):

    def __init__(self, config) -> None:
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.config = config

        self.step_count = 0

    def step(self, action: np.ndarray):
        self.step_count += 1

        dss.run_command('clearall')
        dss.run_command('Set DataPath =C:\\Users\\teghtesa\\PycharmProjects\\Volt\\envs\\power\\matlab')
        dss.run_command('Compile IEEE13Nodeckt.dss')

        dss.run_command(f'set mode =snap loadmult={self.config["loading"]}')

        dss.run_command(f'New Generator.DG632a phases=1 bus1=632.1 kV=2.4  Kw=0 kvar={action[0]}')
        dss.run_command(f'New Generator.DG632b phases=1 bus1=632.2 kV=2.4  Kw=0 kvar={action[1]}')
        dss.run_command(f'New Generator.DG632c phases=1 bus1=632.3 kV=2.4  Kw=0 kvar={action[2]}')

        dss.run_command(f'New Generator.DG633a phases=1 bus1=633.1 kV=2.4  Kw=0 kvar={action[3]}')
        dss.run_command(f'New Generator.DG633b phases=1 bus1=633.2 kV=2.4  Kw=0 kvar={action[4]}')
        dss.run_command(f'New Generator.DG633c phases=1 bus1=633.3 kV=2.4  Kw=0 kvar={action[5]}')

        dss.run_command(f'New Generator.DG634a phases=1 bus1=634.1 kV=2.4 Kw=0 kvar={action[6]}')
        dss.run_command(f'New Generator.DG634b phases=1 bus1=634.2 kV=2.4  Kw=0 kvar={action[7]}')
        dss.run_command(f'New Generator.DG634c phases=1 bus1=634.3 kV=2.4 Kw=0 kvar={action[8]}')

        dss.run_command(f'New Generator.DG645b phases=1 bus1=645.2 kV=2.4  Kw=0 kvar={action[9]}')
        dss.run_command(f'New Generator.DG645c phases=1 bus1=645.3 kV=2.4  Kw=0 kvar={action[10]}')

        dss.run_command(f'New Generator.DG646b phases=1 bus1=646.2 kV=2.4  Kw=0 kvar={action[11]}')
        dss.run_command(f'New Generator.DG646c phases=1 bus1=646.3 kV=2.4  Kw=0 kvar={action[12]}')

        dss.run_command(f'New Generator.DG671a phases=1 bus1=671.1 kV=2.4  Kw=0 kvar={action[13]}')
        dss.run_command(f'New Generator.DG671b phases=1 bus1=671.2 kV=2.4  Kw=0 kvar={action[14]}')
        dss.run_command(f'New Generator.DG671c phases=1 bus1=671.3 kV=2.4  Kw=0 kvar={action[15]}')

        dss.run_command(f'New Generator.DG692a phases=1 bus1=692.1 kV=2.4  Kw=0 kvar={action[16]}')
        dss.run_command(f'New Generator.DG692b phases=1 bus1=692.2 kV=2.4  Kw=0 kvar={action[17]}')
        dss.run_command(f'New Generator.DG692c phases=1 bus1=692.3 kV=2.4  Kw=0 kvar={action[18]}')

        dss.run_command(f'New Generator.DG675a phases=1 bus1=675.1 kV=2.4  Kw=0 kvar={action[19]}')
        dss.run_command(f'New Generator.DG675b phases=1 bus1=675.2 kV=2.4  Kw=0 kvar={action[20]}')
        dss.run_command(f'New Generator.DG675c phases=1 bus1=675.3 kV=2.4  Kw=0 kvar={action[21]}')

        dss.run_command(f'New Generator.DG684a phases=1 bus1=684.1 kV=2.4  Kw=0 kvar={action[22]}')
        dss.run_command(f'New Generator.DG684c phases=1 bus1=684.3 kV=2.4  Kw=0 kvar={action[23]}')

        dss.run_command(f'New Generator.DG611c phases=1 bus1=611.3 kV=2.4  Kw=0 kvar={action[24]}')

        dss.run_command(f'New Generator.DG652a phases=1 bus1=652.1 kV=2.4  Kw=0 kvar={action[25]}')

        dss.run_command(f'New Generator.DG680a phases=1 bus1=680.1 kV=2.4  Kw=0 kvar={action[26]}')
        dss.run_command(f'New Generator.DG680b phases=1 bus1=680.2 kV=2.4  Kw=0 kvar={action[27]}')
        dss.run_command(f'New Generator.DG680c phases=1 bus1=680.3 kV=2.4  Kw=0 kvar={action[28]}')

        dss.Solution.Solve()
        voltages_pu = []

        for phase in range(1, 4):
            voltages_pu += dss.Circuit.AllNodeVmagPUByPhase(phase)

        loss = 0
        for i in range(len(voltages_pu)):
            loss += math.pow(max(0, math.fabs(voltages_pu[i] - 1) - self.config['voltage_threshold']), 2)

        reward = - loss

        done = self.step_count == self.config['T']

        return np.array(voltages_pu), reward, done, {}

    def reset(self):
        self.step_count = 0

        dss.run_command('clearall')
        dss.run_command('Set DataPath =C:\\Users\\teghtesa\\PycharmProjects\\Volt\\envs\\power\\matlab')
        dss.run_command('Compile IEEE13Nodeckt.dss')

        dss.run_command(f'set mode =snap loadmult={self.config["loading"]}')

        voltages_pu = []

        for phase in range(1, 4):
            voltages_pu += dss.Circuit.AllNodeVmagPUByPhase(phase)

        return np.array(voltages_pu)

    def render(self, mode='human'):
        raise NotImplementedError()

    def close(self):
        raise NotImplementedError()
