from datetime import datetime, timedelta
from pathlib import Path

from choose_activity.helpers import ActivityOutcome, log_activity_result


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
        assert len(content.split('\n')) == l + 1
