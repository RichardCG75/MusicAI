from pydub import AudioSegment
from pydub.generators import Sine
import simpleaudio as sa

# Función para convertir frecuencia a tono
def frequency_to_tone(freq, duration_ms):
    return Sine(freq).to_audio_segment(duration=duration_ms)

# Notas y duraciones
notes = [
    (261.626, 500), (261.626, 500), (293.665, 500), (261.626, 500), (349.228, 500), (329.628, 500),
    (261.626, 500), (261.626, 500), (293.665, 500), (261.626, 500), (392.000, 500), (349.228, 500),
    (261.626, 500), (261.626, 500), (523.251, 500), (440.000, 500), (349.228, 500), (329.628, 500), (293.665, 500),
    (466.164, 500), (466.164, 500), (440.000, 500), (349.228, 500), (392.000, 500), (349.228, 500)
]

# Generar y reproducir
song = AudioSegment.silent(duration=0)

for note, duration in notes:
    tone = frequency_to_tone(note, duration)
    song += tone

play_obj = sa.play_buffer(song.raw_data, num_channels=1, bytes_per_sample=2, sample_rate=song.frame_rate)
play_obj.wait_done()
