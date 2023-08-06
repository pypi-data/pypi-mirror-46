import sys

DEBUG = False

# ====================   Adjust this every time before conducting an experiment   ====================
experiment_name = "play_obe_abe"  # give a descriptive and memorable name here
# ====================================================================================================

reward_function = 'play'  # 'play' or 'rules'

if reward_function == 'rules':
    gamma = 0  # only care about immediate reward
elif reward_function == 'play':
    gamma = 0.89  # care about rewards 9 steps into the future: 1 / (1 - gamma)
else:
    print('Specify a valid reward, you cabron!', file=sys.stderr)

trumps = 'obe_abe'  # 'obe_abe' or 'all'

n_steps = 90  # = 10 games, determines the batch size
nminibatches = 10  # must be a divisor of n_steps!

learning_rate = 1e-3

if DEBUG:
    total_timesteps = int(9e2)
else:
    total_timesteps = int(9e9)
