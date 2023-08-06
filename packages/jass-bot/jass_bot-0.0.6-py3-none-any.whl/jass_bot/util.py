import logging

from gym_jass.envs import SchieberEnv
from schieber.card import from_card_to_index
from schieber.player.random_player import RandomPlayer
from stable_baselines.bench import Monitor
from stable_baselines.common.vec_env import DummyVecEnv, SubprocVecEnv

logger = logging.getLogger(__name__)


def delete_invalid_actions(probabilities, obs_dict):
    """
    Set action probabilities of invalid cards to 0
    :param probabilities:
    :param obs_dict:
    :return:
    """
    logger.info(f"action probabilities of all actions: {probabilities}")
    hand_cards = obs_dict["cards"]
    allowed_cards = RandomPlayer().allowed_cards_with_hand_cards(obs_dict, hand_cards)
    # subtract one because in the observation here we have indices from 0 to 35 and not from 1 to 36
    allowed_indices = [from_card_to_index(card) - 1 for card in allowed_cards]
    for j in range(probabilities.size):
        if j not in allowed_indices:
            probabilities[0][j] = 0
    logger.info(f"action probabilities of valid actions: {probabilities}")
    return probabilities


def get_action_with_highest_probability(probabilities):
    """
    Choose the action which should be taken in the end
    :param probabilities:
    :return:
    """
    return [int(probabilities.argmax())]


def init_env(log_dir, n_cpu=False, reward_function='play', trumps='all'):
    """
    Initializes the environment by a given name
    :param trumps: determines if there is any restriction to the available trumps ('all' or 'obe_abe')
    :param reward_function: the chosen reward function ('play' or 'rules')
    :param log_dir:
    :param n_cpu: set a number to enable multiprocessing. Does not work yet for the gym-jass env!
    :return:
    """
    env = SchieberEnv(reward_function=reward_function, trumps=trumps)
    # The file monitor.csv which this Monitor creates is used in the callback.
    env = Monitor(env, log_dir, allow_early_resets=True)
    if n_cpu > 1:
        # return SubprocVecEnv([lambda: env for _ in range(n_cpu)])
        return DummyVecEnv(
            [lambda: env for _ in range(n_cpu)])  # TODO not sure if this does not result in threading problems!!!
    else:
        return DummyVecEnv([lambda: env])


def evaluate(env, model, n_games=10):
    """
    Evaluates the learned model.
    TODO in a later steps invalid actions could be removed so that only valid actions can be chosen.
    :param env:
    :param model:
    :param n_games:
    :return:
    """
    for i in range(n_games):
        obs = env.reset()
        for j in range(9):
            action = model.predict(obs)[0]  # the prediction is a tuple with the next state as the second entry
            obs, rewards, dones, info = env.step(action)
            print(f"Reward: {rewards}")
            env.render()
