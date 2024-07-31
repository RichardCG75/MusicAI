import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, TimeDistributed
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.losses import MeanSquaredError
import data
import play

# Define custom loss function with specific penalties for undesired tone differences
def custom_loss(y_true, y_pred):
    mse_loss = MeanSquaredError()(y_true, y_pred)
    y_true_tones = y_true[:, :, 0]
    y_pred_tones = y_pred[:, :, 0]
    tone_diffs = tf.abs(y_true_tones - y_pred_tones)
    
    penalties = tf.where(
        tone_diffs == 1, 10.0, 
        tf.where(
            tone_diffs == 2, 10.0, 
            tf.where(
                tone_diffs == 10, 10.0, 
                tf.where(
                    tone_diffs == 11, 10.0, 
                    tf.where(
                        tone_diffs <= 4, 1.0, 
                        tf.where(
                            tone_diffs <= 6, 0.5, 
                            tf.where(
                                tone_diffs <= 8, 0.2, 
                                0.1
                            )
                        )
                    )
                )
            )
        )
    )
    
    weighted_mse_loss = mse_loss * penalties
    return tf.reduce_mean(weighted_mse_loss)

# Function to create sequences from data
def create_sequences(data, seq_length):
    X, y = [], []
    for i in range(len(data) - seq_length):
        X.append(data[i:i+seq_length])
        y.append(data[i+seq_length])
    return np.array(X), np.array(y)

# Example data preprocessing
songs = data.songs
notes = [note for song in songs for note in song]
notes = np.array(notes)

notes[:, 0] = (notes[:, 0] - 36) / (120 - 36)
durations = to_categorical(notes[:, 1], num_classes=8)
notes = np.hstack((notes[:, [0]], durations))

seq_length = 10
X, y = create_sequences(notes, seq_length)
X = X.reshape((X.shape[0], seq_length, X.shape[2]))
y = y.reshape((y.shape[0], 1, y.shape[1]))

model = Sequential([
    LSTM(128, input_shape=(seq_length, X.shape[2]), return_sequences=True),
    LSTM(128, return_sequences=True),
    TimeDistributed(Dense(9, activation='linear'))
])

model.compile(optimizer='adam', loss=custom_loss)
model.summary()
model.fit(X, y, epochs=5, batch_size=64)

def preprocess_seed_sequence(seed_sequence):
    seed_sequence = np.array(seed_sequence)
    seed_sequence[:, 0] = (seed_sequence[:, 0] - 36) / (120 - 36)

    valid_durations = seed_sequence[:, 1].astype(int)
    if np.any(valid_durations < 0) or np.any(valid_durations > 7):
        raise ValueError("Seed sequence durations must be in the range 0-7.")

    durations = to_categorical(valid_durations, num_classes=8)
    seed_sequence = np.hstack((seed_sequence[:, [0]], durations))

    return seed_sequence

def generate_melody(model, seed_sequence, seq_length, num_notes_to_generate):
    generated_notes = []
    current_sequence = preprocess_seed_sequence(seed_sequence).copy()

    for _ in range(num_notes_to_generate):
        predictions = model.predict(np.expand_dims(current_sequence, axis=0))
        next_note = predictions[0, -1]

        tone_normalized = np.clip(next_note[0], 0, 1)
        next_note[0] = tone_normalized

        generated_notes.append(next_note)
        current_sequence = np.roll(current_sequence, shift=-1, axis=0)
        current_sequence[-1] = next_note

    melody = []
    for note in generated_notes:
        tone = int(note[0] * (120 - 36) + 36)
        duration = np.argmax(note[1:])
        melody.append([tone, duration])
    
    return melody

seed_sequence = [
    [89, 4], [88, 4], [89, 4], [88, 4], [89, 4], [88, 4], [86, 4], [88, 4],
    [84, 4], [86, 4]
]
num_notes_to_generate = 20
melody = generate_melody(model, seed_sequence, seq_length, num_notes_to_generate)
print(melody)
play.play_melody(melody, 3)
