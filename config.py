env_config = {
    'system': 'ieee123',
    'mode': 'fixed_control',
    'load_var': 1.0,
    'voltage_threshold': 0.05,
    # Search range around the default parameters
    'search_range': 3.3,
    # Length of history
    'history_size': 1,
    # Episode length
    'T': 3000,
    'repeat': 10,
    'window_size': 10,
    'change_threshold': 0.2,
    'reward_mode': 'continuous',
    'voltage_convergence_grace_period': 50,  # in case reward_mode is continuous
}

model_config = {
    "fcnet_hiddens": [512, 512],
    "vf_share_layers": True,
}

ppo_training_config = {
    "gamma": 0.96,
    "rollout_fragment_length": 64,
    "batch_mode": "truncate_episodes",
    # "batch_mode": "complete_episodes",
    "train_batch_size": 1024,
    # Coefficient of the value function loss. IMPORTANT: you must tune this if
    # you set vf_share_layers=True inside your model's config.
    "vf_loss_coeff": 1.0,
    # "lr": 5e-5,

    # Clip param for the value function. Note that this is sensitive to the
    # scale of the rewards. If your expected V is large, increase this.
    # "vf_clip_param": 400.0,
}