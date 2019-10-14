from typing import Dict, List
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


def user_selection(options: List[str], choice: str) -> str:
    """Choose a value from the user input answer.

    >>> user_selection(['apple', 'banana', 'orange'], 'banana')
    'banana'

    >>> user_selection(['apple', 'banana', 'orange'], '1')
    'apple'

    Parameters
    ----------
    options : List[str]
        List of options
    choice : str
        The user input, can be an 1-based index or a string to match

    Returns
    -------
    str
        An element from the options list corresponding to the choice
    """
    if not len(options):
        raise ValueError('No options given')
