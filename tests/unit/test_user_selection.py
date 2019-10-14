import pytest

from choose_activity.helpers import user_selection


def test_no_options():
    with pytest.raises(ValueError) as excinfo:
        user_selection(
            [],
            '')
        assert "no options given!" in str(excinfo.value)

    with pytest.raises(ValueError) as excinfo:
        user_selection(
            [],
            'bla')
        assert "no options given!" in str(excinfo.value)


def test_empty_choice():
    with pytest.raises(IndexError) as excinfo:
        user_selection(
            ['apple', 'banana', '🤠', 'blob'],
            '')
        assert "no choice" in str(excinfo.value)

    with pytest.raises(IndexError) as excinfo:
        user_selection(
            ['apple', 'banana', '🤠', 'blob'],
            '\n')
        assert "no choice" in str(excinfo.value)


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

