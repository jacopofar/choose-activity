from collections import Counter

from choose_activity.helpers import weighted_choice


def test_no_choice():
    assert weighted_choice(None) is None
    assert weighted_choice({}) is None


def test_single_choice():
    assert weighted_choice({'only me!': 1.0}) == 'only me!'


def test_weighted_choice():
    SAMPLE_SIZE = 600
    c = Counter()
    for _ in range(SAMPLE_SIZE):
        chosen = weighted_choice({
            'choice a': 1.0,
            'choice b': 6.0,
            'choice c': 0.2,
            })
        c.update([chosen])
    assert c['choice a'] < c['choice b']
    assert c['choice a'] > c['choice c']
    assert sum(c.values()) == SAMPLE_SIZE
    assert len(c.keys()) == 3
