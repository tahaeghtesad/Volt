from ray.tune import ExperimentAnalysis

if __name__ == '__main__':
    analysis = ExperimentAnalysis(
        '~/ray_results/hyperparameter_check_bo_full_range/experiment_state-2022-06-13_19-56-22.json')

    analysis.results_df.sort_values(by=['epoch_reward_mean'], ascending=True).head(64)[
        ['config.alpha', 'config.beta', 'config.gamma', 'config.c',
         'epoch_reward_mean', 'epoch_reward_std', 'epoch_reward_min', 'epoch_reward_max',
         'epoch_reward_q25', 'epoch_reward_q75']].to_csv('hyperparameter_check_bo_full_range.csv')