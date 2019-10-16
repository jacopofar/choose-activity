from datetime import datetime
from random import choice

from choose_activity.helpers import load_state, save_state, ActivitiesState


def test_activities_state():
    # simple activity state
    activities = {
        'bla': 2.3,
        'blop blep': 1.3,
        'ssss blep': 90992.13,
    }
    state = ActivitiesState(activities)

    assert state.activities == activities
    assert state.current_activity is None
    assert state.current_activity_start is None

    state.current_activity = 'bla'
    now = datetime.now()
    state.current_activity_start = now

    assert state.activities == activities
    assert state.current_activity == 'bla'
    assert state.current_activity_start == now


def test_load_empty():
    # load a non-existing file and check the empty state
    fname = ''.join(choice('qwertyuioplkjhgfdsa') for k in range(40))
    new_state = load_state(fname)
    assert new_state.activities == {}
    assert new_state.current_activity is None
    assert new_state.current_activity_start is None

