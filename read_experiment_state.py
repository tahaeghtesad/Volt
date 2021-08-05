import json
import math

import numpy as np


def read_experiment_state(path, count):
    with open(path) as fd:
        experiment_state = json.load(fd)
        checkpoints = list()

        for c in experiment_state['checkpoints']:
            checkpoints.append(json.loads(c))

        experiment_state['checkpoints'] = checkpoints

        max_reward = -500
        best_config = dict()
        in_order = sorted(experiment_state['checkpoints'], key=lambda c: 100 if 'episode_reward' not in c['metric_analysis'] else -c['metric_analysis']['episode_reward']['max'])
        for i in range(count):
            config = dict(alpha=in_order[i]['config']['alpha'],
                          beta=in_order[i]['config']['beta'],
                          gamma=in_order[i]['config']['gamma'],
                          c=in_order[i]['config']['c'])
            print(f'reward: {in_order[i]["metric_analysis"]["episode_reward"]["max"]} - config: {config}')
        return config


if __name__ == '__main__':
    # path = 'C:/users/taha/desktop/experiment_state-2021-08-04_12-37-37.json' # grid search
    path = 'C:/users/taha/desktop/experiment_state-2021-08-04_17-19-44.json'

    read_experiment_state(path, 20)