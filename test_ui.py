import song

# ui
melody1 = [
    [60, 3], [60, 3], [62, 3], [60, 3], [65, 3], [64, 3],  # C4, C4, D4, C4, F4, E4
    [60, 3], [60, 3], [62, 3], [60, 3], [67, 3], [65, 3],  # C4, C4, D4, C4, G4, F4
    [60, 3], [60, 3], [72, 3], [69, 3], [65, 3], [64, 3], [62, 3],  # C4, C4, C5, A4, F4, E4, D4
    [70, 3], [70, 3], [69, 3], [65, 3], [67, 3], [65, 3]   # Bb4, Bb4, A4, F4, G4, F4
]
song1 = song.Song(
    artist='No artist', 
    title='Feliz cumpleaños',
    speed=99,
    melody=melody1
    )

print(song1)