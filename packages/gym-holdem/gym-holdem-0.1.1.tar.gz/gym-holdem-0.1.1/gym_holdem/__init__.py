from gym.envs.registration import register

register(
    id='poker_ai_gym-v0',
    entry_point='gym_holdem.envs:HoldemEnv',
)
