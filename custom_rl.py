import pickle
from datetime import datetime

import gym
import numpy as np
import tensorflow as tf
from tqdm import tqdm

from custom_ddpg import update_target
from envs.remote.client import RemoteEnv
from config import env_config, custom_ddpg_config


def create_critic(env: gym.Env):
    state_dim = env.observation_space.sample().shape
    action_dim = env.action_space.sample().shape

    # State as input
    state_input = tf.keras.layers.Input(shape=(state_dim))
    state_out = tf.keras.layers.Dense(16, activation="relu")(state_input)
    state_out = tf.keras.layers.Dense(32, activation="relu")(state_out)

    # Action as input
    action_input = tf.keras.layers.Input(shape=(action_dim))
    action_out = tf.keras.layers.Dense(32, activation="relu")(action_input)

    # Both are passed through seperate layer before concatenating
    concat = tf.keras.layers.Concatenate()([state_out, action_out])

    out = tf.keras.layers.Dense(256, activation="relu")(concat)
    out = tf.keras.layers.Dense(256, activation="relu")(out)
    outputs = tf.keras.layers.Dense(1, activation='linear')(out)

    # Outputs single value for give state-action
    model = tf.keras.Model([state_input, action_input], outputs, name="critic")

    return model


def create_actor(env: gym.Env):
    if env.action_space.__class__.__name__ == 'Box':
        action_dim = env.action_space.sample().shape[0]
    else:
        raise NotImplementedError(f'Action space of {env.action_space.__class__.__name__} not implemented')

    state_dim = env.observation_space.sample().shape

    inputs = tf.keras.layers.Input(shape=(state_dim))
    dense = tf.keras.layers.Dense(64, activation='relu')(inputs)
    dense = tf.keras.layers.Dense(64, activation='relu')(dense)
    output = tf.keras.layers.Dense(action_dim, activation='sigmoid')(dense)

    model = tf.keras.Model(inputs=inputs, outputs=output, name="actor")

    return model


@tf.function
def logit(x):
    return -tf.math.log(1. / x - 1.)


def reverse_action(env, action):
    # action * (env.action_space.high - env.action_space.low) + env.action_space.low
    return (action - env.action_space.low) / (env.action_space.high - env.action_space.low)


def scale_action(env, action):
    return action * (env.action_space.high - env.action_space.low) + env.action_space.low


def pre_train(env,
              actor_target, actor,
              critic_target, critic,
              actor_optimizer, critic_optimizer,
              experiences,
              tau):
    for i in (pbar := tqdm(range(len(experiences) // custom_ddpg_config['batch_size'] * 2048))):
        samples = np.random.choice(experiences, size=custom_ddpg_config['batch_size'])

        states = np.array([x['state'] for x in samples])
        actions = reverse_action(env, np.array([x['action'][0] + x['action'][2] for x in samples]))
        rewards = np.array([x['reward'] for x in samples])
        next_states = np.array([x['next_state'] for x in samples])
        dones = np.array([x['done'] for x in samples])

        y = (1 + critic_target([next_states, actor_target(next_states)])) * np.expand_dims((1 - dones), axis=1) + np.expand_dims(dones * (-rewards) * (1 - rewards) * env_config['T'], axis=1)

        with tf.GradientTape() as tape:
            critic_value = critic([states, actions])
            critic_loss = tf.reduce_mean(tf.square(y - critic_value))

        critic_gradients = tape.gradient(critic_loss, critic.trainable_variables)
        critic_optimizer.apply_gradients(zip(critic_gradients, critic.trainable_variables))

        tf.summary.scalar('critic_loss', critic_loss, step=i)
        pbar.set_description(f'{critic_loss.numpy():.4f}')

        with tf.GradientTape() as tape:
            critic_value = critic([states, actor(states)])
            actor_loss = tf.reduce_mean(critic_value)

        tf.summary.scalar('action_mean', tf.reduce_mean(scale_action(env, actor(states))), step=i)

        actor_gradients = tape.gradient(actor_loss, actor.trainable_variables)
        actor_optimizer.apply_gradients(zip(actor_gradients, actor.trainable_variables))

        update_target(actor_target.weights, actor.weights, tau)
        update_target(critic_target.weights, critic.weights, tau)


def main(logdir):
    experiences = pickle.load(open('hyperparameter_ieee13_all_control_experiences.pkl', 'rb'))

    env = RemoteEnv('localhost', 6985, env_config)
    actor = create_actor(env)
    critic = create_critic(env)
    actor_target = create_actor(env)
    critic_target = create_critic(env)

    for (a, b) in zip(actor_target.trainable_variables, actor.trainable_variables):
        a.assign(b)
    for (a, b) in zip(critic_target.trainable_variables, critic.trainable_variables):
        a.assign(b)

    actor_optimizer = tf.keras.optimizers.Adam(learning_rate=custom_ddpg_config['actor_lr'])
    critic_optimizer = tf.keras.optimizers.Adam(learning_rate=custom_ddpg_config['critic_lr'])

    try:
        pre_train(env,
                  actor_target, actor,
                  critic_target, critic,
                  actor_optimizer, critic_optimizer,
                  experiences,
                  custom_ddpg_config['tau'])
    except KeyboardInterrupt:
        pass

    print('Saving actor and critic weights...')
    actor.save(logdir + '/actor.h5')
    critic.save(logdir + '/critic.h5')
    print(f'Actor and Critic Saved to {logdir}')


if __name__ == '__main__':
    try:
        gpus = tf.config.experimental.list_physical_devices('GPU')
        if gpus:
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)

        logdir = "logs/custom_rl/" + datetime.now().strftime("%Y%m%d-%H%M%S")
        file_writer = tf.summary.create_file_writer(logdir + "/metrics")
        file_writer.set_as_default()

        main(logdir)
    except RuntimeError as e:
        print(f'Failed to set GPU growth: {e}')
