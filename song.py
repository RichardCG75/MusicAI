class Song:
    artist = ''
    title = ''
    speed = 0
    melody = []
    def __init__(self, artist, title, speed, melody):
        self.artist = artist
        self.title = title
        self.speed = speed
        self.melody = melody
    
    def print_melody(self):
        for note in self.melody:
            print(note)
    
    def __str__(self):
        return f'{self.artist} - {self.title}\nspeed: {self.speed}\n{self.melody}'