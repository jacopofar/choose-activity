from datetime import datetime, timedelta

from choose_activity.helpers import (
    ActivityOutcome,
    log_activity_result,
    latest_outcome_for_activity
)


def test_log_outcome(tmp_path):
    test_path = tmp_path / 'activities_state.log'
    for l in range(5):
        log_activity_result(test_path, ActivityOutcome(
            activity='勉強',
            start_at=datetime.now().astimezone(),
            end_at=datetime.now().astimezone() + timedelta(minutes=42),
            is_done=True,
            feedback='''some
            multiline
                    thing!

                    😬 😬 😬
                    ''',
        ))
        content = open(test_path).read()
        lines = content.split('\n')
        assert lines[-1] == ''
        assert len(lines) == l + 2  # 0-indexed + empty line


def test_get_latest_outcome(tmp_path):
    test_path = tmp_path / 'activities_state.log'
    for l in range(5):
        log_activity_result(test_path, ActivityOutcome(
            activity=f'activity type #{l}',
            start_at=datetime.now().astimezone(),
            end_at=datetime.now().astimezone() + timedelta(minutes=42),
            is_done=True,
            feedback=f'activity description {l}!',
        ))

    assert (
        latest_outcome_for_activity(test_path, 'activity type #1') ==
        'activity description 1!')
