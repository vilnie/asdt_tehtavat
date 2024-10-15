
import threading
import random
import winsound
from PIL import Image, ImageTk

class Apina:
    def __init__(self, canvas, image_path, position):
        self.canvas = canvas
        self.image_path = image_path
        self.position = position
        self.image = self.load_image()
        self.id = self.canvas.create_image(self.position[0], self.position[1], image=self.image)
        self.alive = True  # Indicates if the monkey is alive

    def load_image(self):
        """Load and resize the monkey image."""
        image = Image.open(self.image_path)
        image = image.resize((30, 30), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(image)

    def make_sound(self):
        """Play a sound for the monkey."""
        taajuus = random.randint(400, 2000)
        winsound.Beep(taajuus, 500)

    def start_sound_thread(self):
        """Start a thread for the monkey's sound."""
        if self.alive:
            threading.Thread(target=self.make_sound).start()

    def is_alive(self):
        """Check if the monkey is alive."""
        return self.alive