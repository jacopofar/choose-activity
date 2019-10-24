from dataclasses import dataclass
from datetime import datetime
import json
from pathlib import Path
from random import random
from typing import Callable, Dict, List, Optional


@dataclass
class ActivitiesState:
    """Represent the available activities and state of the current one."""

    activities: Dict[str, float]
    current_activity: Optional[str] = None
    current_activity_start: Optional[datetime] = None


@dataclass
class ActivityOutcome:
    """Represent the result of an activity."""

    activity: str
    start_at: datetime
    is_done: bool
    feedback: str


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
    if not options:
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


def enumerate_options(options: List[str]) -> str:
    """Represent the options nicely.

    The returned value places the options in such a way that it's easy
    to distinguish them and associate them with the index starting from 1

    Parameters
    ----------
    options : List[str]
        List of options to enumerate

    Returns
    -------
    str
        A string representing the options to be printed
    """
    return '\n'.join([
        f'{i + 1}) {option}' for i, option in enumerate(options)
    ])


def get_answer(
    options: List[str],
    input_fun: Callable[..., str],
        ) -> str:
    """Ask for an answer until it gets one.

    The input function will be invoked until the user provides an answer
    within the options.
    Parameters
    ----------
    options : List[str]
        List of possible options
    input_fun : Callable[..., str]
        Function to be invoked, possibly multiple times,
        to get the input from the user

    Returns
    -------
    str
        The valid choice from the user
    """

    print(enumerate_options(options))
    print('\nChoose an option using the number or a word:')
    while True:
        choice = input_fun()
        try:
            return user_selection(options, choice)
        except IndexError as ie:
            print(ie.args[0])


def load_state(fname: Path) -> ActivitiesState:
    """Load the state from the activities file.

    If the file does not exist, an empty state is generated.

    Parameters
    ----------
    fname : Path
        file path from where to load

    Returns
    -------
    ActivitiesState
        The loaded activities or an initialised one
    """
    if not fname.exists():
        return ActivitiesState({})

    raw_obj = json.loads(open(fname).read())
    if raw_obj['current_activity_start'] is not None:
        raw_obj['current_activity_start'] = datetime.fromisoformat(
            raw_obj['current_activity_start'])
    return ActivitiesState(
        raw_obj['activities'],
        current_activity=raw_obj['current_activity'],
        current_activity_start=raw_obj['current_activity_start'],
    )


def save_state(fname: Path, state: ActivitiesState) -> None:
    """Save the state in a file.

    Parameters
    ----------
    fname : Path
        File path where to write
    state : ActivitiesState
        The activity state to write

    Returns
    -------
    None
    """
    write_date = None
    if state.current_activity_start is not None:
        write_date = state.current_activity_start.isoformat()
    raw_obj = dict(
        activities=state.activities,
        current_activity=state.current_activity,
        current_activity_start=write_date,
    )
    with open(fname, 'w') as f:
        f.write(json.dumps(raw_obj, indent=2))


def get_weight(prompt: str, input_fun: Callable[..., str]) -> float:
    """Prompt the user for a weight until a proper value is given.

    Parameters
    ----------
    prompt : str
        The prompt for the weight to be shown to the user
    input_fun : Callable[..., str]
        Function to be invoked, possibly multiple times,
        to get the input from the user

    Returns
    -------
    float
        The first valid weight given
    """
    print(prompt)
    while True:
        candidate = input_fun()
        try:
            return float(candidate)
        except ValueError:
            print(f'Invalid value "{candidate}", use a number with dot as'
                  ' decimal separator')


def log_activity_result(fname: Path, outcome: ActivityOutcome):
    """Log the result of an activity.

    Parameters
    ----------
    fname : Path
        File path where to write
    outcome : ActivityOutcome
        The activity outcome to store
    """
    raise NotImplementedError('Implement activity log please')
