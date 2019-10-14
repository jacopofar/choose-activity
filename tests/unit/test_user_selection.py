from unittest.mock import MagicMock
import pytest

from choose_activity.helpers import user_selection, get_answer


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

    # asked the user for it
    assert _input.call_args_list == [
        ({}, (['blip', 'blop'], 'blip'))
    ]

    _input = MagicMock(return_value='blop')
    answer = get_answer(['blip', 'blop'], _input)

    # return the correct answer
    assert answer == 'blop'

    # asked the user for it
    assert _input.call_args_list == [
        ({}, (['blip', 'blop'], 'blop'))
    ]


def test_retry_to_get_answer():
    answers = [False, False, True]

    def input_function():
        if answers.pop():
            return 'blip'
        else:
            return 'not really there'

    answer = get_answer(['blip', 'blop'], input_function)

    # return the correct answer
    assert answer == 'blip'

    # asked the user for it 3 times
    assert len(input_function.call_args_list) == 3
