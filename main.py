# import model
import utils
import play
import data
import random
import model
import numpy as np

# Generate aset of songs melody with AI
seq_length = 32
melody = model.generate_melody(model.model_pitch, model.model_duration, model.seed_sequence_pitch, model.seed_sequence_duration, seq_length)
play.play_melody(melody)

# Apply important counterpoint rules
melody = random.choice(data.songs)
melody = utils.apply_counterpoint_melodic_rules(random_melody)
melody = utils.apply_counterpoint_rythm_rules(random_melody)

# Play the melody
play.play_melody(random.choice(data.songs), speed=2)