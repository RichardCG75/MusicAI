# import model
import play
import data
import numpy as np


seq_length = 16

seed_sequence = [
    [89,4], [88,4], [89,4], [88,4], [89,4], [88,4], [86,8], [88,4],
    [84,4], [86,4], [88,4], [89,8], [86,4], [89,4], [88,4], [86,8]
    ] 
# num_notes_to_generate = 20
# melody = model.generate_melody(model, seed_sequence, seq_length, num_notes_to_generate)
# play.play_melody(melody, 3)

play.play_melody(seed_sequence, 3)