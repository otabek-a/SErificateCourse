import wordy
import PIL

def solution(board: PIL.Image) -> str:
    """Generates a valid next guess for the WordyPy game."""
    
    # Extract game state from the board (Check available functions in wordy)
    try:
        state = wordy.get_state_from_image(board)  # Change this if necessary
    except AttributeError:
        print("Error: wordy module does not have 'get_state_from_image'. Check available functions.")
        return "error"

    # Get previously played words
    played_words = state.get("previous_guesses", [])  # Adjust if the key is different

    # Get a list of valid words
    try:
        valid_words = wordy.get_valid_words()  # Ensure this function exists
    except AttributeError:
        print("Error: wordy module does not have 'get_valid_words'. Check available functions.")
        return "error"

    # Remove words that have already been played
    possible_words = [word for word in valid_words if word not in played_words]

    # Pick the first valid word
    if possible_words:
        return possible_words[0]

    return "error"

# Running the game loop
for i in range(5):
    try:
        # Get the current board state as an image
        image = wordy.get_board_state()  
        
        # Generate a new valid guess
        new_guess = solution(image)  
        
        # Submit the guess to wordy
        wordy.make_guess(new_guess)
    except Exception as e:
        print(f"An error occurred: {e}")
        break
