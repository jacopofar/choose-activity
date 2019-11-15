from unittest.mock import MagicMock
import pytest

from choose_activity.helpers import (
    get_answer,
    get_weight,
    enumerate_options,
    user_selection,
    )


def test_no_options():
    with pytest.raises(ValueError) as excinfo:
        user_selection(
            [],
            '')
    assert 'no options given' in str(excinfo.value)

    with pytest.raises(ValueError) as excinfo:
        user_selection(
            [],
            'bla')
    assert 'no options given' in str(excinfo.value)


def test_empty_choice():
    with pytest.raises(IndexError) as excinfo:
        user_selection(
            ['apple', 'banana', '🤠', 'blob'],
            '')
    assert 'no choice' in str(excinfo.value)

    with pytest.raises(IndexError) as excinfo:
        user_selection(
            ['apple', 'banana', '🤠', 'blob'],
            '\n')
    assert 'no choice' in str(excinfo.value)


def test_invalid_choice():
    with pytest.raises(IndexError) as excinfo:
        user_selection(
            ['apple', 'banana', '🤠', 'blob'],
            'orange')
    assert 'invalid choice' in str(excinfo.value)

    with pytest.raises(IndexError) as excinfo:
        user_selection(
            ['apple', 'banana', '🤠', 'blob'],
            '6')
    assert 'invalid choice' in str(excinfo.value)


def test_valid_choice():
    assert user_selection(
        ['apple', 'banana', '🤠', 'blob'],
        '1') == 'apple'

    assert user_selection(
        ['apple', 'banana', '🤠', 'blob'],
        'apple') == 'apple'

    assert user_selection(
        ['apple', 'banana', '🤠', 'blob'],
        'APPLE') == 'apple'

    assert user_selection(
        ['apple', 'banana', '🤠', 'blob'],
        '4') == 'blob'

    assert user_selection(
        ['apple', 'banana', '🤠', 'blob'],
        '🤠') == '🤠'


def test_get_answer():
    _input = MagicMock(return_value='blip')
    answer = get_answer(['blip', 'blop'], _input)

    # return the correct answer
    assert answer == 'blip'

    _input = MagicMock(return_value='blop')
    answer = get_answer(['blip', 'blop'], _input)

    # return the correct answer
    assert answer == 'blop'


def test_ambiguous_answer():
    answers = ['ble', 'bleep', 'blip', 'bleep 2', 'never reached']

    def input_function():
        return answers.pop(0)

    answer = get_answer(['bleep 1', 'bleep 2', 'extra option'], input_function)

    # return the correct answer
    assert answer == 'bleep 2'


def test_retry_to_get_answer():
    answers = ['blarp', '3', 'blip', 'never reached', 'blop']

    def input_function():
        return answers.pop(0)

    answer = get_answer(['blip', 'blop'], input_function)

    # return the correct answer
    assert answer == 'blip'


def test_enumerate_options():
    # not much to test here, just ensure it contains the option text
    assert len(['a', 'bb']) > 0
    assert 'duckburg' in enumerate_options(['a', 'duckburg']).lower()


def test_get_weight():
    _input = MagicMock(return_value='1.3')
    assert get_weight('hello', _input) == 1.3

    answers = ['blarp', '3', 'never reached']

    def input_function():
        return answers.pop(0)

    assert get_weight('hello', input_function) == 3.0
