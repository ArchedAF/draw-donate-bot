from PIL import ImageGrab, Image
import time
import autoit
import keyboard
from collections import defaultdict

# Configuration variables
SQUARE_SIZE = 764  # YOUR SQUARE SIZE
GRID_SIZE = 3  # YOUR FOUND GRID SIZE
COLOR_SIMILARITY_THRESHOLD = 10  # Higher = less detailed but faster

COLOR_PICKER_POSITION = (640, 855)
COLOR_CHANGE_TAB = (1100, 705)
FINALIZE_COLOR_CHANGE = (877, 703)

INPUT_IMAGE_PATH = 'art.png'
OUTPUT_IMAGE_PATH = 'prepared_image.png'

# Don't configure
CLICK_DELAY = 0.5
DELETE_DELAY = 2
IMAGE_RESIZE_METHOD = Image.BOX
SCREENSHOT_INTERVAL = 1

# Pause/continue toggle
paused = False

def is_white_pixel(r, g, b, threshold=200):
    return r > threshold and g > threshold and b > threshold

def color_similarity(c1, c2, threshold=COLOR_SIMILARITY_THRESHOLD):
    """Compares two RGB colors and returns True if they are within the specified similarity threshold."""
    r1, g1, b1 = c1
    r2, g2, b2 = c2
    return abs(r1 - r2) < threshold and abs(g1 - g2) < threshold and abs(b1 - b2) < threshold

def find_closest_color(existing_colors, color, threshold=COLOR_SIMILARITY_THRESHOLD):
    """Find the closest color in the existing colors, or return the original color if none are close enough."""
    for existing_color in existing_colors:
        if color_similarity(existing_color, color, threshold):
            return existing_color
    return color

def find_white_square(square_size=SQUARE_SIZE):
    # Take a screenshot of the screen
    screen = ImageGrab.grab()
    screen_width, screen_height = screen.size
    pixels = screen.load()

    # Loop through the pixels to find the white square
    for y in range(screen_height - square_size + 1):
        for x in range(screen_width - square_size + 1):
            # Check the top-left corner for white
            if is_white_pixel(*pixels[x, y]):
                # Check if the bottom-right corner is white and if it forms a square of the correct size
                if (is_white_pixel(*pixels[x + square_size - 1, y]) and
                    is_white_pixel(*pixels[x, y + square_size - 1]) and
                    is_white_pixel(*pixels[x + square_size - 1, y + square_size - 1])):
                    
                    # Check the borders of the square to ensure all are white
                    all_white = True
                    for i in range(square_size):
                        if not (is_white_pixel(*pixels[x + i, y]) and
                                is_white_pixel(*pixels[x + i, y + square_size - 1]) and
                                is_white_pixel(*pixels[x, y + i]) and
                                is_white_pixel(*pixels[x + square_size - 1, y + i])):
                            all_white = False
                            break
                    
                    if all_white:
                        return (x, y, x + square_size - 1, y + square_size - 1)
    
    return None

def prepare_image_for_drawing(input_image_path=INPUT_IMAGE_PATH, square_size=SQUARE_SIZE):
    # Open the input image
    input_image = Image.open(input_image_path)

    # Directly resize the image to square_size x square_size pixels
    resized_image = input_image.resize((square_size, square_size), IMAGE_RESIZE_METHOD)

    # Convert to RGB mode to ensure correct pixel format
    resized_image = resized_image.convert('RGB')

    # Save the prepared image
    resized_image.save(OUTPUT_IMAGE_PATH)
    print(f"Prepared image saved as '{OUTPUT_IMAGE_PATH}'")
    return resized_image

def change_color(color_code, color_picker_position=COLOR_PICKER_POSITION, 
                 color_change_tab=COLOR_CHANGE_TAB, 
                 finalize_color_change=FINALIZE_COLOR_CHANGE):
    # Click the color picker position
    autoit.mouse_click("left", color_picker_position[0], color_picker_position[1])
    time.sleep(CLICK_DELAY)

    # Double click the color change tab
    autoit.mouse_click("left", color_change_tab[0], color_change_tab[1], clicks=2)
    time.sleep(CLICK_DELAY)

    # Select all existing content and delete it
    autoit.send("^a")  # Ctrl + A to select all
    time.sleep(0.5)
    autoit.send("{DEL}")
    time.sleep(DELETE_DELAY)

    # Use AutoIt to send the color code with `#`
    autoit.clip_put(f"#{color_code}")  # Copy color code to clipboard
    
    # Paste the color code
    autoit.send("^v")  # Ctrl+V to paste from clipboard
    time.sleep(DELETE_DELAY)

    # Click to finalize the color change
    autoit.mouse_click("left", finalize_color_change[0], finalize_color_change[1])
    time.sleep(CLICK_DELAY)

def draw_image_on_canvas(borders, prepared_image, grid_size=GRID_SIZE):
    x1, y1, _, _ = borders
    pixels = prepared_image.load()

    color_positions = defaultdict(list)
    existing_colors = []

    # Group similar colors
    for y in range(0, prepared_image.height, grid_size):
        for x in range(0, prepared_image.width, grid_size):
            r, g, b = pixels[x, y]
            if is_white_pixel(r, g, b):  # Skip white pixels
                continue

            # Find the closest existing color or use the original color
            closest_color = find_closest_color(existing_colors, (r, g, b))
            if closest_color not in existing_colors:
                existing_colors.append(closest_color)

            color_code = f'{closest_color[0]:02X}{closest_color[1]:02X}{closest_color[2]:02X}'
            color_positions[color_code].append((x1 + x + grid_size // 2, y1 + y + grid_size // 2))

    # Draw the grouped colors
    for color_code, positions in color_positions.items():
        change_color(color_code)
        for pos in positions:
            global paused
            while paused:  # Wait if paused
                if keyboard.is_pressed('p'):
                    paused = False
                    print("Resuming process...")
                    time.sleep(0.5)
            if keyboard.is_pressed('p'):
                paused = True
                print("Pausing process...")
                time.sleep(0.5)
            if keyboard.is_pressed('q'):  # Stop if 'Q' is pressed
                print("Process stopped by user.")
                return
            autoit.mouse_move(pos[0], pos[1])
            autoit.mouse_click("left")
            time.sleep(0.01)  # Small delay between clicks for speed

# Main process to find the white square, prepare the image, and draw it
while True:
    borders = find_white_square()
    if borders:
        print(f"White square found with borders: {borders}")
        break
    else:
        print(f"No {SQUARE_SIZE}x{SQUARE_SIZE} white square found. Retrying...")
    time.sleep(SCREENSHOT_INTERVAL)

# After finding the white square, prepare the image for drawing
prepared_image = prepare_image_for_drawing()

# Draw the prepared image on the canvas
draw_image_on_canvas(borders, prepared_image)
