from gym.envs.registration import register

register(
    id='Volt-v0',
    entry_point='envs.power:ThirteenBus',
)