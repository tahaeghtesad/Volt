gamma = 0.90

env_config = {
    'system': 'ieee13',
    'mode': 'all_control',
    'load_var': 'dynamic',  # can be floating point (between 0.8 and 1.2) or 'dynamic'
    'voltage_threshold': 0.05,  # ([0.95, 1.05])
    'range': {  # alpha, beta, gamma, c, respectively
        'low': [-10, -10, -10, -10],
        'high': [10, 10, 10, 10]
        # 'low': [-3, -3, -3, -3],
        # 'high': [3, 3, 3, 3]
        # 'low': [0.001, 0.01, 1, 0.1],
        # 'high': [0.1, 1000, 10000, 1000]
    },
    # Length of history
    'history_size': 1,
    # Episode length
    'T': 50,
    'repeat': 1,
    'epochs': 32,  # for optimizer.py to average the episode reward over n epochs
    'window_size': 500,
    'change_threshold': 0.05,
    'gamma': gamma,

    'default_params': {
        'alpha': -10,
        'beta': -10,
        'gamma': 10,
        'c': 4.039414574158694
    }
}

custom_ddpg_config = {
    'actor_lr': 0.005,
    'critic_lr': 0.002,
    'tau': 0.001,
    'buffer_size': 10_000,
    'batch_size': 256,
    'cpu_count': 12,
    'OU_mean': 0,
    'OU_std': 0.5,
    'OU_theta': 0.15,
    'OU_dt': 0.01,
}

model_config = {
    "fcnet_hiddens": [64, 64, 64],
    "vf_share_layers": True,
}

ppo_training_config = {
    "gamma": gamma,
    "rollout_fragment_length": 64,  # This should be ppo_training_config['train_batch_size'] // num_workers(16)
    "batch_mode": "truncate_episodes",
    # "batch_mode": "complete_episodes",
    "train_batch_size": 1024,
    # Coefficient of the value function loss. IMPORTANT: you must tune this if
    # you set vf_share_layers=True inside your model's config.
    "vf_loss_coeff": 0.5,

    "lr": 5e-5,

    # "lr_schedule": [
    #     [0, 5e-5],
    #     [20480, 1e-6],
    # ],

    # "lr": lr_start,
    # "lr_schedule": [
    #     [0, lr_start],
    #     [lr_time, lr_end],
    # ],

    # Clip param for the value function. Note that this is sensitive to the
    # scale of the rewards. If your expected V is large, increase this.
    # "vf_clip_param": 10.0,

    # 'clip_param': 0.3,

    # 'framework': 'tfe',

    # Coefficient of the entropy regularizer.
    "entropy_coeff": 0.00,
    # Decay schedule for the entropy regularizer.
    # "entropy_coeff_schedule": None,

    # Initial coefficient for KL divergence.
    # "kl_coeff": 0.2,
    # "kl_coeff": 0.0001,

    "kl_target": 0.02,

    # "explore": False
}

trainer_config = {
    'training_iteration': 1024,  # Total training steps will be trainer_config['training_iteration'] * ppo_training_config['train_batch_size']
    'checkpoint_freq': 16,  # How often to save the model, measured in training iterations.
}

ddpg_training_config = {
    # === Twin Delayed DDPG (TD3) and Soft Actor-Critic (SAC) tricks ===
    # TD3: https://spinningup.openai.com/en/latest/algorithms/td3.html
    # In addition to settings below, you can use "exploration_noise_type" and
    # "exploration_gauss_act_noise" to get IID Gaussian exploration noise
    # instead of OU exploration noise.
    # twin Q-net
    "twin_q": False,
    # delayed policy update
    "policy_delay": 1,
    # target policy smoothing
    # (this also replaces OU exploration noise with IID Gaussian exploration
    # noise, for now)
    "smooth_target_policy": False,
    # gaussian stddev of target action noise for smoothing
    "target_noise": 0.2,
    # target noise limit (bound)
    "target_noise_clip": 0.5,

    # === Evaluation ===
    # Evaluate with epsilon=0 every `evaluation_interval` training iterations.
    # The evaluation stats will be reported under the "evaluation" metric key.
    # Note that evaluation is currently not parallelized, and that for Ape-X
    # metrics are already only reported for the lowest epsilon workers.
    "evaluation_interval": None,
    # Number of episodes to run per evaluation period.
    "evaluation_duration": 10,

    # === Model ===
    # Apply a state preprocessor with spec given by the "model" config option
    # (like other RL algorithms). This is mostly useful if you have a weird
    # observation shape, like an image. Disabled by default.
    "use_state_preprocessor": False,
    # Postprocess the policy network model output with these hidden layers. If
    # use_state_preprocessor is False, then these will be the *only* hidden
    # layers in the network.
    "actor_hiddens": [400, 300],
    # Hidden layers activation of the postprocessing stage of the policy
    # network
    "actor_hidden_activation": "relu",
    # Postprocess the critic network model output with these hidden layers;
    # again, if use_state_preprocessor is True, then the state will be
    # preprocessed by the model specified with the "model" config option first.
    "critic_hiddens": [400, 300],
    # Hidden layers activation of the postprocessing state of the critic.
    "critic_hidden_activation": "relu",
    # N-step Q learning
    "n_step": 1,

    # === Exploration ===
    "exploration_config": {
        # DDPG uses OrnsteinUhlenbeck (stateful) noise to be added to NN-output
        # actions (after a possible pure random phase of n timesteps).
        "type": "OrnsteinUhlenbeckNoise",
        # For how many timesteps should we return completely random actions,
        # before we start adding (scaled) noise?
        "random_timesteps": 1000,
        # The OU-base scaling factor to always apply to action-added noise.
        "ou_base_scale": 0.1,
        # The OU theta param.
        "ou_theta": 0.15,
        # The OU sigma param.
        "ou_sigma": 0.2,
        # The initial noise scaling factor.
        "initial_scale": 1.0,
        # The final noise scaling factor.
        "final_scale": 0.02,
        # Timesteps over which to anneal scale (from initial to final values).
        "scale_timesteps": 10000,
    },
    # Number of env steps to optimize for before returning
    "timesteps_per_iteration": 1000,
    # Extra configuration that disables exploration.
    "evaluation_config": {
        "explore": False
    },
    # === Replay buffer ===
    # Size of the replay buffer. Note that if async_updates is set, then
    # each worker will have a replay buffer of this size.
    "replay_buffer_config": {
        "type": "MultiAgentReplayBuffer",
        "capacity": 50000,
    },
    # Set this to True, if you want the contents of your buffer(s) to be
    # stored in any saved checkpoints as well.
    # Warnings will be created if:
    # - This is True AND restoring from a checkpoint that contains no buffer
    #   data.
    # - This is False AND restoring from a checkpoint that does contain
    #   buffer data.
    "store_buffer_in_checkpoints": False,
    # If True prioritized replay buffer will be used.
    # Whether to LZ4 compress observations
    "compress_observations": False,

    # The intensity with which to update the model (vs collecting samples from
    # the env). If None, uses the "natural" value of:
    # `train_batch_size` / (`rollout_fragment_length` x `num_workers` x
    # `num_envs_per_worker`).
    # If provided, will make sure that the ratio between ts inserted into and
    # sampled from the buffer matches the given value.
    # Example:
    #   training_intensity=1000.0
    #   train_batch_size=250 rollout_fragment_length=1
    #   num_workers=1 (or 0) num_envs_per_worker=1
    #   -> natural value = 250 / 1 = 250.0
    #   -> will make sure that replay+train op will be executed 4x as
    #      often as rollout+insert op (4 * 250 = 1000).
    # See: rllib/agents/dqn/dqn.py::calculate_rr_weights for further details.
    "training_intensity": None,

    # === Optimization ===
    # Learning rate for the critic (Q-function) optimizer.
    # "critic_lr": 1e-3,
    "critic_lr": 1e-2,
    # Learning rate for the actor (policy) optimizer.
    "actor_lr": 1e-3,
    # Update the target network every `target_network_update_freq` steps.
    "target_network_update_freq": 0,
    # Update the target by \tau * policy + (1-\tau) * target_policy
    "tau": 0.002,
    # If True, use huber loss instead of squared loss for critic network
    # Conventionally, no need to clip gradients if using a huber loss
    "use_huber": False,
    # Threshold of a huber loss
    "huber_threshold": 1.0,
    # Weights for L2 regularization
    "l2_reg": 1e-6,
    # If not None, clip gradients during optimization at this value
    "grad_clip": None,
    # Update the replay buffer with this many samples at once. Note that this
    # setting applies per-worker if num_workers > 1.
    "rollout_fragment_length": 1,
    # Size of a batched sampled from replay buffer for training. Note that
    # if async_updates is set, then each worker returns gradients for a
    # batch of this size.
    "train_batch_size": 256,

}