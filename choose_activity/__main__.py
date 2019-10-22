from pathlib import Path

from choose_activity.helpers import (
    get_answer,
    get_weight,
    load_state,
    save_state,
    )

ACTIVITIES_STATE_FILE_PATH = Path.home() / '.choose_activity.activities'

TXT_NEW_ACTIVITY = 'add a new type of activity'
TXT_CHANGE_WEIGHT = 'change the weight of an activity'
TXT_DELETE_ACTIVITY = 'delete activity'


def main():
    activities_state = load_state(ACTIVITIES_STATE_FILE_PATH)
    # if an activity is going on, ask for a feedback to quit it
    if activities_state.current_activity is not None:
        # if an activity was started, can only ask for feedback and close it
        raise NotImplementedError('manage activity closing!')

    # one can always add an activity
    choices = [TXT_NEW_ACTIVITY, 'exit']
    if activities_state.activities:
        choices.append(TXT_DELETE_ACTIVITY)
        choices.append(TXT_CHANGE_WEIGHT)
        choices.append('DO SOMETHING!')

    choice = get_answer(choices, input)

    if choice == 'exit':
        print('Bye.')
        return

    if choice == TXT_DELETE_ACTIVITY:
        delete_candidates = list(activities_state.activities)
        delete_candidates += ['Exit']
        choice = get_answer(delete_candidates, input)

        if choice == 'Exit':
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
        change_candidates += ['Exit']
        choice = get_answer(change_candidates, input)

        if choice == 'Exit':
            print('Exiting without changes')
            return

        new_weight = get_weight(f'New weight for the activity {choice}', input)
        activities_state.activities[choice] = new_weight
        save_state(ACTIVITIES_STATE_FILE_PATH, activities_state)
        print(f'Activity updated: {choice} has now weight {new_weight}')
        return

    raise NotImplementedError(f'Choice {choice} not implemented!')


if __name__ == '__main__':
    main()
