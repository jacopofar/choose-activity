from pathlib import Path

from choose_activity.helpers import (
    get_answer,
    get_weight,
    load_state,
    save_state,
    )

ACTIVITIES_STATE_FILE_PATH = Path.home() / '.choose_activity.activities'


def main():
    activities_state = load_state(ACTIVITIES_STATE_FILE_PATH)
    # if an activity is going on, ask for a feedback to quit it
    if activities_state.current_activity is not None:
        # if an activity was started, can only ask for feedback and close it
        raise NotImplementedError('manage activity closing!')
        return

    # one can always add an activity
    choices = ['add a new type of activity', 'exit']
    if len(activities_state.activities) > 0:
        choices.append('delete activity')
        choices.append('change the weight of an activity')
        choices.append('DO SOMETHING!')

    choice = get_answer(choices)

    if choice == 'exit':
        print('Bye.')
        return

    if choice == 'delete activity':
        delete_candidates = list(activities_state.activities)
        delete_candidates += ['Exit']
        choice = get_answer(delete_candidates)

        if choice == 'Exit':
            print('Exiting without changes')
            return

        del activities_state[choice]
        save_state(ACTIVITIES_STATE_FILE_PATH, activities_state)
        print(f'Activity deleted: {choice}')
        return

    if choice == 'change the weight of an activity':
        change_candidates = list(activities_state.activities)
        change_candidates += ['Exit']
        choice = get_answer(change_candidates)

        if choice == 'Exit':
            print('Exiting without changes')
            return

        new_weight = get_weight(f'New weight for the activity {choice}', input)
        activities_state[choice] = new_weight
        save_state(ACTIVITIES_STATE_FILE_PATH, activities_state)
        print(f'Activity updated: {choice} has now weight {new_weight}')
        return

    raise NotImplementedError(f'Choice {choice} not implemented!')



