from typing import Callable, Dict, List
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

    If the choice is a number, it's used as 1-based index.

    If it's a string, the first option containing it as a substring is
    returned, using the

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
        raise ValueError('no options given')
    if choice.strip() == '':
        raise IndexError('no choice')
    try:
        choice_index = int(choice)
        if choice_index > len(options):
            raise IndexError('invalid choice')
        return options[choice_index - 1]

    except ValueError:
        for option in options:
            if choice.lower() in option.lower():
                return option

    raise IndexError('invalid choice')


def get_answer(
    options: List[str],
    input: Callable[..., str],
        ) -> str:
    """Ask for an answer until it gets one.

    The input function will be invoked until the user provides an answer
    within the options.
    Parameters
    ----------
    options : List[str]
        List of possible options
    input : Callable[..., str]
        Function to be invoked, possibly multiple times,
        to get the input from the user

    Returns
    -------
    str
        The valid choice from the user
    """
