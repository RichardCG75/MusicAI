import random


def apply_counterpoint_rythm_rules(arr):
    for sublist in arr:
        sublist[1] = random.choice([4, 6, 8, 3,2])
    return arr


def apply_counterpoint_melodic_rules(arr):

    arr[0][0] = random.randint(48, 72)
    notes_moves = [7, 5, 4, 2,-5, -7, -4, -2]

    last_note = arr[0][0]
    for sublist in arr:
        random_note = random.choice(notes_moves)
        new_note = last_note + random_note

        while (last_note + random_note >= 96 or last_note + random_note <= 48):
            random_note = random.choice(notes_moves)
            new_note = last_note + random_note
        sublist[0] = new_note
        last_note = sublist[0]
    return arr
