from datetime import datetime
from pathlib import Path
from textwrap import dedent

from choose_activity.helpers import (
    ActivityOutcome,
    get_answer,
    get_weight,
    load_state,
    save_state,
    weighted_choice,
    log_activity_result,
    latest_outcome_for_activity,
    )

ACTIVITIES_STATE_FILE_PATH = Path.home() / '.choose_activity.activities'
ACTIVITIES_LOG_FILE_PATH = Path.home() / '.choose_activity.log'

TXT_NEW_ACTIVITY = 'Add a new type of activity'
TXT_CHANGE_WEIGHT = 'Change the weight of an activity'
TXT_DELETE_ACTIVITY = 'Delete activity'
TXT_EXIT = 'Exit'
TXT_DO_ACTIVITY = 'DO SOMETHING!'
TXT_DONE = 'Done that'
TXT_SKIPPED = 'Skipped'


def main():
    activities_state = load_state(ACTIVITIES_STATE_FILE_PATH)
    # if an activity is going on, ask for a feedback to quit it
    if activities_state.current_activity is not None:
        # if an activity was started, can only ask for feedback and close it
        print(f'The activity was: {activities_state.current_activity}')
        print('Did you do it?')
        is_done = get_answer([TXT_DONE, TXT_SKIPPED], input) == TXT_DONE
        print(':)' if is_done else ':(')
        feedback = input('How do you feel about it?\n')
        log_activity_result(
            ACTIVITIES_LOG_FILE_PATH,
            ActivityOutcome(
                activity=activities_state.current_activity,
                start_at=activities_state.current_activity_start,
                end_at=datetime.now().astimezone(),
                is_done=is_done,
                feedback=feedback
            ))
        activities_state.current_activity = None
        activities_state.current_activity_start = None
        save_state(ACTIVITIES_STATE_FILE_PATH, activities_state)
        print('Bye.')
        return
    # one can always add an activity
    choices = [TXT_NEW_ACTIVITY]
    if activities_state.activities:
        choices.append(TXT_DELETE_ACTIVITY)
        choices.append(TXT_CHANGE_WEIGHT)
        choices.append(TXT_DO_ACTIVITY)
    # It's nicer to have exit at the end of the list
    choices.append(TXT_EXIT)
    choice = get_answer(choices, input)

    if choice == TXT_EXIT:
        print('Bye.')
        return

    if choice == TXT_DELETE_ACTIVITY:
        delete_candidates = list(activities_state.activities)
        delete_candidates += [TXT_EXIT]
        choice = get_answer(delete_candidates, input)

        if choice == TXT_EXIT:
            print('Exiting without changes')
            return

        del activities_state.activities[choice]
        save_state(ACTIVITIES_STATE_FILE_PATH, activities_state)
        print(f'Activity deleted: {choice}')
        return

    if choice == TXT_NEW_ACTIVITY:
        activity_name = input('What is the name of the new activity? ')
        activity_weight = get_weight('Weight for this activity', input)
        activities_state.activities[activity_name] = activity_weight
        print('Activity inserted!')
        save_state(ACTIVITIES_STATE_FILE_PATH, activities_state)
        return

    if choice == TXT_CHANGE_WEIGHT:
        change_candidates = list(activities_state.activities)
        change_candidates += [TXT_EXIT]
        choice = get_answer(change_candidates, input)

        if choice == TXT_EXIT:
            print('Exiting without changes')
            return

        new_weight = get_weight(f'New weight for the activity {choice}', input)
        activities_state.activities[choice] = new_weight
        save_state(ACTIVITIES_STATE_FILE_PATH, activities_state)
        print(f'Activity updated: {choice} has now weight {new_weight}')
        return

    if choice == TXT_DO_ACTIVITY:
        activity = weighted_choice(activities_state.activities)
        print(dedent(f'''
        The chosen activity is:

          👉  {activity}

        Go!
        '''))
        latest = latest_outcome_for_activity(
            ACTIVITIES_LOG_FILE_PATH,
            activity,
        )
        if latest is not None:
            print(dedent(f'''
            This activity has already been done, the latest outcome was:

              📖 {latest}

            '''))
        activities_state.current_activity = activity
        activities_state.current_activity_start = datetime.now().astimezone()
        save_state(ACTIVITIES_STATE_FILE_PATH, activities_state)
        return

    raise NotImplementedError(f'Choice {choice} not implemented!')


if __name__ == '__main__':
    main()
