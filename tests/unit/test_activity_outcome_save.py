from datetime import datetime, timedelta

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
        lines = content.split('\n')
        assert lines[-1] == ''
        assert len(lines) == l + 2  # 0-indexed + empty line
