import numpy as np
import simpleaudio as sa

def generate_sine_wave(frequency, duration, sample_rate=44100):
    """
    Generate a sine wave for a given frequency and duration.
    
    Parameters:
        frequency: Frequency of the sine wave in Hz
        duration: Duration of the sine wave in seconds
        sample_rate: Sample rate for the waveform generation (default is 44100 Hz)
    
    Returns:
        wave: NumPy array containing the waveform
    """
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = 0.5 * np.sin(2 * np.pi * frequency * t)
    return wave

def play_melody(melody, speed=1.0, sample_rate=44100):
    """
    Play a melody containing notes and durations with a speed factor.
    
    Parameters:
        melody: List of notes and durations, e.g., [[57, 4], [60, 4], ...]
        speed: Multiplicative factor to adjust the playback speed (default is 1.0)
        sample_rate: Sample rate for audio playback (default is 44100 Hz)
    """
    audio_data = np.array([])

    for note, duration in melody:
        # Convert MIDI note number to frequency
        frequency = 440.0 * 2.0**((note - 69) / 12.0)
        # Adjust duration by the speed factor
        adjusted_duration = (duration / 4.0) / speed
        # Generate the waveform for the current note
        wave = generate_sine_wave(frequency, adjusted_duration, sample_rate)
        # Append the waveform to the audio data
        audio_data = np.concatenate((audio_data, wave))

    # Convert the audio data to 16-bit PCM format
    audio_data = np.int16(audio_data * 32767)
    
    # Play the audio data
    play_obj = sa.play_buffer(audio_data, 1, 2, sample_rate)
    play_obj.wait_done()

# # Example usage
# melody = [
#     [57, 7], [60, 7], [62, 7], [64, 6], [67, 6], [69, 4], [71, 5], [73, 5],
#     [76, 4], [78, 4], [80, 4], [82, 4], [85, 4], [87, 4], [89, 4], [91, 4],
#     [94, 4], [96, 4], [94, 4], [91, 4], [89, 4], [87, 4], [85, 4], [82, 4],
#     [80, 4], [78, 4], [76, 4], [73, 4], [71, 4], [69, 4], [67, 4], [64, 4]
# ]

# play_melody(melody, speed=2)  # Play melody with 1.5x speed
