from PIL import Image

class Letter:
    def __init__(self, char: str, in_correct_place: bool = False, in_word: bool = False):
        self.char = char
        self.in_correct_place = in_correct_place  # Default is False
        self.in_word = in_word  # Default is False

    def __repr__(self):
        return f"Letter('{self.char}', {self.in_correct_place}, {self.in_word})"

class Bot:
    def __init__(self, display_spec):
        self.display_spec = display_spec
    
    @staticmethod
    def _tuple_to_str(pixels: tuple) -> str:
        """Converts an RGB(A) tuple into a hex string in uppercase."""
        return f"#{pixels[0]:02X}{pixels[1]:02X}{pixels[2]:02X}"
    
    def _process_image(self, guess: str, guess_image: Image) -> list[Letter]:
        """Processes an image and returns a list of Letter objects based on pixel colors."""
        letters = []
        width, height = guess_image.size
        box_width = width // len(guess)  # Assuming equal spacing for letters
        
        for i, char in enumerate(guess):
            pixel_x = (i * box_width) + (box_width // 2)  # Sampling in the middle of each letter box
            pixel_y = height // 2  # Sampling vertically at the middle
            pixel_color = guess_image.getpixel((pixel_x, pixel_y))
            hex_color = self._tuple_to_str(pixel_color)
            
            # Determine letter status based on color
            in_correct_place = hex_color == self.display_spec.correct_location_color
            in_word = hex_color == self.display_spec.incorrect_location_color  # Letter exists but in the wrong place
            
            letters.append(Letter(char, in_correct_place, in_word))
        
        return letters
