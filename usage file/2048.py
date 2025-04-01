import random
from sense_hat import SenseHat
import call

ROWS = 4
COLS = 4

sense = SenseHat()

COLOR_MAP = {
0:		(0, 0, 0),
2:      (255, 0, 0),
4:      (0, 255, 0),
8:      (0, 0, 255),
16:     (255, 255, 0),
32:     (255, 0, 255),
64:     (0, 255, 255),
128:    (128, 128, 128),
256:    (255, 160, 97),
512:    (255, 165, 0),
1024:   (255, 105, 180),
2048:   (255, 255, 255),
4096:   (238, 228, 218),
}

def initialize_game():
    """Initialize the game matrix with two starting tiles."""
    matrix = [[0] * COLS for _ in range(ROWS)]  # Create a 4x4 grid filled with 0s
    a = add_new_tile(matrix)
    a = add_new_tile(matrix)
    a = add_new_tile(matrix)
    a = add_new_tile(matrix)
    a = add_new_tile(matrix)
    a = add_new_tile(matrix)
    return matrix


def add_new_tile(matrix):
    """Add a new tile (2 or 4) to a random empty position in the matrix."""
    empty_positions = [(r, c) for r in range(ROWS) for c in range(COLS) if matrix[r][c] == 0]
    if not empty_positions:
        return False
    row, col = random.choice(empty_positions)
    matrix[row][col] = random.choice([2,4])
    return True


def print_matrix(matrix):
    """Print the matrix in a formatted way."""
    print("-" * 25)
    for row in matrix:
        print("|", end="")
        for val in row:
            print(f"{val:^5}" if val != 0 else "     ", end="|")  # Center-align numbers
        print("\n" + "-" * 25)

def display_on_sensehat(matrix):
    """Display the matrix on the Sense HAT LED matrix."""
    # Create a list of RGB colors for the Sense HAT (8x8 LED matrix)
    pixels = []

    for row in matrix:
        for val in row:
            color = COLOR_MAP.get(val, (255, 255, 255))  # Default to white for unknown values
            # Each tile in the 4x4 grid is represented as a 2x2 block of LEDs
            pixels.extend([color, color])

    # Repeat each row twice to create the 2x2 blocks
    sense_pixels = []
    for i in range(0, len(pixels), 8):
        sense_pixels.extend(pixels[i:i + 8])
        sense_pixels.extend(pixels[i:i + 8])

    # Set the pixels on the Sense HAT
    sense.set_pixels(sense_pixels)

def can_merge_or_move(matrix):
    """Check if any moves are possible (merging or sliding)."""
    # Check for empty spaces
    for row in matrix:
        if 0 in row:
            return True

    # Check for possible merges (adjacent equal numbers)
    for r in range(ROWS):
        for c in range(COLS):
            if c + 1 < COLS and matrix[r][c] == matrix[r][c + 1]:
                return True  # Horizontal merge possible
            if r + 1 < ROWS and matrix[r][c] == matrix[r + 1][c]:
                return True  # Vertical merge possible

    return False  # No moves available


def move_left(matrix):
    """Move all tiles to the left and merge if possible."""
    moved = False
    for row in matrix:
        # Slide non-zero tiles to the left
        new_row = [val for val in row if val != 0]
        for i in range(len(new_row) - 1):
            if new_row[i] == new_row[i + 1]:  # Merge tiles
                new_row[i] *= 2
                new_row[i + 1] = 0
                moved = True
        # Remove zeros again after merging
        new_row = [val for val in new_row if val != 0]
        # Add zeros to the end to maintain row length
        new_row += [0] * (COLS - len(new_row))
        # Check if the row has changed
        if row != new_row:
            moved = True
        row[:] = new_row  # Update the original row
    return moved


def move_right(matrix):
    """Move all tiles to the right and merge if possible."""
    for row in matrix:
        row.reverse()  # Reverse the row
    moved = move_left(matrix)  # Move left on the reversed row
    for row in matrix:
        row.reverse()  # Reverse the row back
    return moved


def move_up(matrix):
    """Move all tiles up and merge if possible."""
    matrix[:] = list(map(list, zip(*matrix)))  # Transpose the matrix
    moved = move_left(matrix)  # Move left on the transposed matrix
    matrix[:] = list(map(list, zip(*matrix)))  # Transpose the matrix back
    return moved


def move_down(matrix):
    """Move all tiles down and merge if possible."""
    matrix[:] = list(map(list, zip(*matrix)))  # Transpose the matrix
    moved = move_right(matrix)  # Move right on the transposed matrix
    matrix[:] = list(map(list, zip(*matrix)))  # Transpose the matrix back
    return moved


def handle_input(matrix,temp,order):
    """Prompt the user for input and handle the move."""
    move_made = False
    command2 = ""
    while not move_made:
        ##command = input("Enter move (up, down, left, right, quit): ").strip().lower()
        command = order
        if (command == "thumbs_up" or command2 == "thumbs_up"):
            move_made = move_up(matrix)
        elif (command == "PeaceSign" or command2 == "PeaceSign"):
            move_made = move_down(matrix)
        elif (command == "Open" or command2 == "Open"):
            move_made = move_left(matrix)
        elif (command == "Close" or command2 == "Close"):
            move_made = move_right(matrix)
        
        if not move_made:
            print(command, "is a invalid move. Try a different direction.")
            tmp, order1 = get_input(temp)
            command2 = order1
            
    return move_made
  
def check_winning_condition(matrix):
    """Check if the player has reached the winning tile."""
    for row in matrix:
        if 512 in row:
            return True
    return False
    
def get_input(temp):
    print("getting")
    order = call.output(temp)
    temp = order
    print(order)
    return temp,order
    
def main():
    """Main game loop."""
    matrix = initialize_game()
    temp = ""
    has_won = False
    One_more = True
    while True:
        print_matrix(matrix)
        display_on_sensehat(matrix)
        
        
        if  (not has_won) and (check_winning_condition(matrix)):
            sense.show_message("Congratulations! You've reached the 2048 tile!", text_colour=(255, 255, 255))
            sense.show_message("Continue?Again?", text_colour=(255, 255, 255))
            temp, order = get_input(temp)
            if order == "Open":
                has_won = True
                sense.show_message("To be Continue", text_colour=(255, 255, 255))
                continue
            elif order == "PeaceSign":
                sense.show_message("Restarting", text_colour=(255, 255, 255))
                return True
            else:
                return False

        if (not can_merge_or_move(matrix)) or (not One_more) :
            sense.show_message("Game Over!", text_colour=(255, 255, 255))
            sense.show_message("Again?", text_colour=(255, 255, 255))
            temp, order = get_input(temp)
            
            if order == "PeaceSign":
                has_won = True
                sense.show_message("Restarting", text_colour=(255, 255, 255))
                return True
            else:
                sense.show_message("Thanks for playing?", text_colour=(255, 255, 255))
                return False
                
        temp, order = get_input(temp)
        handle_input(matrix,temp,order)
        One_more = add_new_tile(matrix)
        One_more = add_new_tile(matrix)



if __name__ == "__main__":
    sense = SenseHat()
    restart = True
    #sense.show_message("Welcome to the 2048 tile!!", text_colour=(255, 255, 255))
    while(restart == True):
        restart = main()
    sense.show_message("Thanks for playing?", text_colour=(255, 255, 255))
