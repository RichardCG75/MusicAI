import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.utils import to_categorical
import data

# Data preprocessing
songs = data.songs
# Normalize pitch (0 to 1) and one-hot encode duration (0 to 7)
def preprocess_data(songs):
    pitch_sequences = []
    duration_sequences = []
    for song in songs:
        for note, duration in song:
            pitch = (note - 36) / 60  # Normalize to 0-1 range
            duration_encoded = to_categorical(duration, num_classes=8)
            pitch_sequences.append([pitch])
            duration_sequences.append(duration_encoded)
    return np.array(pitch_sequences), np.array(duration_sequences)

pitch_sequences, duration_sequences = preprocess_data(songs)

# Prepare input and output sequences
X_pitch = []
X_duration = []
y_pitch = []
y_duration = []
sequence_length = 4

for i in range(len(pitch_sequences) - sequence_length):
    X_pitch.append(pitch_sequences[i:i + sequence_length])
    X_duration.append(duration_sequences[i:i + sequence_length])
    y_pitch.append(pitch_sequences[i + sequence_length])
    y_duration.append(duration_sequences[i + sequence_length])

X_pitch = np.array(X_pitch)
X_duration = np.array(X_duration)
y_pitch = np.array(y_pitch)
y_duration = np.array(y_duration)

# Build the model for pitch
model_pitch = Sequential([
    LSTM(128, input_shape=(sequence_length, 1), return_sequences=True),
    Dropout(0.2),
    LSTM(128),
    Dropout(0.2),
    Dense(128, activation='relu'),
    Dense(1, activation='linear')  # Output pitch
])

model_pitch.compile(optimizer='adam', loss='mse')

# Train the model for pitch
history_pitch = model_pitch.fit(X_pitch, y_pitch, epochs=100, batch_size=64, validation_split=0.2)

# Model for duration
model_duration = Sequential([
    LSTM(128, input_shape=(sequence_length, 8), return_sequences=True),
    Dropout(0.2),
    LSTM(128),
    Dropout(0.2),
    Dense(128, activation='relu'),
    Dense(8, activation='softmax')  # Output duration
])

model_duration.compile(optimizer='adam', loss='categorical_crossentropy')

# Train the model for duration
history_duration = model_duration.fit(X_duration, y_duration, epochs=100, batch_size=64, validation_split=0.2)

# Function to generate a new melody
def generate_melody(model_pitch, model_duration, seed_sequence_pitch, seed_sequence_duration, length):
    generated = []
    current_sequence_pitch = seed_sequence_pitch
    current_sequence_duration = seed_sequence_duration

    for _ in range(length):
        # Predict pitch
        pitch_pred = model_pitch.predict(np.array([current_sequence_pitch]))[0, -1]
        pitch_pred = np.squeeze(pitch_pred)  # Ensure pitch_pred is a scalar
        pitch_pred = pitch_pred * 60 + 36  # Denormalize

        # Predict duration
        duration_pred = model_duration.predict(np.array([current_sequence_duration]))[0, -1]
        duration_pred = np.argmax(duration_pred)  # Decode one-hot

        generated.append([int(pitch_pred), duration_pred])

        # Update current sequence
        pitch_norm = (pitch_pred - 36) / 60
        duration_encoded = to_categorical(duration_pred, num_classes=8)
        current_sequence_pitch = np.append(current_sequence_pitch[1:], [[pitch_norm]], axis=0)
        current_sequence_duration = np.append(current_sequence_duration[1:], [duration_encoded], axis=0)

    return generated

# Seed sequence (last part of a song)
seed_sequence_pitch = X_pitch[-1]
seed_sequence_duration = X_duration[-1]