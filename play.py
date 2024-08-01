import numpy as np
import simpleaudio as sa

# Define the function to generate a sine wave
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
