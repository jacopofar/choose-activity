from typing import Dict
from random import random


def weighted_choice(choices_and_weights: Dict[str, float]) -> str:
    """Choose a key with a probability proportional to the value.

    Parameters
    ----------
    choices_and_weights : Dict[str, float]
        Dictionary of choices and corresponding weights. Weights are
        expected to be strictly greater than 0, or the behavior of
        the function is undefined

    Returns
    -------
    str
        One of the keys of the dictionary, None if it's empty
    """
    if choices_and_weights is None:
        return None

    chosen_weight = random() * sum(choices_and_weights.values())
    for k, v in choices_and_weights.items():
        chosen_weight -= v
        if chosen_weight < 0:
            return k
