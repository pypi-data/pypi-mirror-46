# TODO ask to be mentioned on https://stable-baselines.readthedocs.io/en/master/misc/projects.html
# TODO what do these metrics from baselines mean:
# --------------------------------------
# | approxkl           | 0.00069229305 | 0.1 -> small, 10 -> large
# | clipfrac           | 0.00390625    |
# | ep_rewmean         | nan           | mean episode reward!
# | eplenmean          | nan           | mean episode length
# | explained_variance | 0.847         | when 0 -> tune hyper-parameters of neural network
# | fps                | 142           |
# | nupdates           | 782           | number of updates
# | policy_entropy     | 3.3405766     | when too big -> policy too random, should go down
# | policy_loss        | -0.011813248  |
# | serial_timesteps   | 100096        |
# | time_elapsed       | 656           | time elapsed in seconds from start
# | total_timesteps    | 100096        |
# | value_loss         | 0.4478733     | loss of the value function
# --------------------------------------

# TODO add random search for hyperparameters

# TODO experiment with different nn sizes

# TODO make pyminijass work for easier experimentation -> ultra simple implementation: 1 suit 12 values distributed to 4 players

# TODO consider different random seeds!

# TODO make experiments with different reward functions

# TODO try Lstm policy

# TODO program evaluation of rl player strength!

# TODO try rules with trump


import sys
import threading


print("Importing modules", file=sys.stderr)

import logging

from datetime import datetime

import numpy as np

from stable_baselines import PPO2
from stable_baselines.bench import load_results
from stable_baselines.results_plotter import ts2xy

import jass_bot.hyper_parameters as hp

from jass_bot import util
from jass_bot.jass_policy import JassPolicy
import os

print("Setting up experiment", file=sys.stderr)

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"  # disable gpu usage because this apparently slows down training
logger = logging.getLogger(__name__)

# Create log dir
log_dir = "log/"
# this enables multiple experiments to be run in parallel --> there is one monitor file for each experiment
console_log_dir = log_dir + "console/" + hp.experiment_name + "/"
models_log_dir = log_dir + "models/"
tensorboard_log_dir = log_dir + "tensorboard/"
os.makedirs(log_dir, exist_ok=True)
os.makedirs(console_log_dir, exist_ok=True)
os.makedirs(models_log_dir, exist_ok=True)

env_name = 'Schieber-v0'
# time improvement is not very big with multiple cores
n_cpu = 1  # there are 8 cores on my local machine (MacBook Pro) and 16 on the server (Ubuntu 16.04)

env = util.init_env(log_dir=console_log_dir, n_cpu=n_cpu, reward_function=hp.reward_function, trumps=hp.trumps)

policy = "MlpLstmPolicy"
policy = "MlpLnLstmPolicy"
policy = "MlpPolicy"
policy = JassPolicy

model = PPO2(policy, env, n_steps=hp.n_steps, gamma=hp.gamma, nminibatches=hp.nminibatches,
             learning_rate=hp.learning_rate, verbose=1,
             tensorboard_log=tensorboard_log_dir)

# model_name = "stich-higher-learning-rate_env=Schieber-v0_gamma=0.89_nsteps=90_learning_rate=0.001_policy=JassPolicy_model=PPO2_time=2019-01-13_12:08:28_final.pkl"
# model = PPO2.load(models_log_dir + model_name, env=env, policy=JassPolicy)

model_name = model.__class__.__name__

time = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')

log_name = f"{hp.experiment_name}_env={env_name}_reward_function={hp.reward_function}_trumps={hp.trumps}" \
    f"_gamma={hp.gamma}_nsteps={hp.n_steps}_learning_rate={hp.learning_rate}" \
    f"_policy={policy.__name__}_model={model_name}_time={time}"

training_log = open(f"{console_log_dir}/{log_name}.log", "a")
sys.stdout = training_log
logging.basicConfig(level=logging.INFO, filename=f"{console_log_dir}/{log_name}.log", datefmt='%H:%M:%S',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s')

best_mean_reward, n_steps = -np.inf, 0
model_file_name = f"{models_log_dir}{log_name}_best.pkl"


# open(model_file_name, 'a').close()  # create empty file here because otherwise saving does not work in the callback


def callback(_locals, _globals):
    """
    Callback called at each step (for DQN an others) or after n steps (see ACER or PPO2)
    :param _locals: (dict)
    :param _globals: (dict)
    """
    global n_steps, best_mean_reward, console_log_dir, model_file_name, log_name

    # This is invoked in every 10th update
    if (n_steps + 1) % 10 == 0:
        # Evaluate policy performance
        x, y = ts2xy(load_results(console_log_dir), 'timesteps')
        if len(x) > 0:
            mean_reward = np.mean(y[-100:])
            print(x[-1], 'timesteps', file=sys.stderr)
            print(
                "Best mean reward: {:.2f} - Last mean reward per episode: {:.2f}".format(best_mean_reward, mean_reward),
                file=sys.stderr)

            # New best model, you could save the agent here
            if mean_reward > best_mean_reward:
                best_mean_reward = mean_reward
                # Example for saving best model
                print("Saving new best model", file=sys.stderr)
                _locals['self'].save(model_file_name)
    n_steps += 1
    return True


start = datetime.now()

print("Learning model", file=sys.stderr)
model.learn(total_timesteps=hp.total_timesteps, tb_log_name=log_name, callback=callback)

training_time = datetime.now() - start
print(f"Training time: {training_time}", file=sys.stderr)

print("Saving final model", file=sys.stderr)
model.save(f"{models_log_dir}{log_name}_final.pkl")

print("Evaluating model", file=sys.stderr)
if n_cpu > 0:
    env = env.envs[0]  # we only need one environment for the evaluation
util.evaluate(env, model, n_games=10)

print(threading.enumerate(), file=sys.stderr)

env.close()
sys.exit()
