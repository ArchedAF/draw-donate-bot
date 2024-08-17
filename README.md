# draw-donate-bot
no injection/executor auto draw bot for draw &amp; donate roblox. (Uses your mouse)

# Automated Image Processing and Color Picking

```markdown
# Automated Image Processing and Color Picking

This project automates the process of identifying and resizing specific areas within a screenshot (white and red areas), and then uses these dimensions to configure and automate color picking and image drawing on a canvas.

## Installation

To get started, you'll need to install the following Python libraries:

```bash
pip install pillow
pip install pyautogui
pip install autoit
pip install keyboard
```

These libraries are required for image processing, screen capturing, automating mouse and keyboard actions, and handling collections.

## Usage

### Step 1: Capturing and Resizing the Canvas

1. **Take a Screenshot** of your canvas and save it as `screenshot.png`.
2. **Run `resize.py`** to find and crop the white and red areas from the screenshot.

```python
if __name__ == "__main__":
    input_image_path = "screenshot.png"
    white_output_path = "white_cropped.png"
    red_output_path = "red_cropped.png"
    find_and_save_area(input_image_path, white_output_path, red_output_path)
```

This script will output the cropped areas and their dimensions:

```bash
White area cropped and saved as white_cropped.png. Dimensions: (764, 765)
Red area cropped and saved as red_cropped.png. Dimensions: (4, 4)
```

### Step 2: Configuring `main.py`

Once you have the dimensions from `resize.py`, configure the following variables in `main.py`:

```python
# Configuration variables
SQUARE_SIZE = 764  # YOUR SQUARE SIZE
GRID_SIZE = 3  # YOUR FOUND GRID SIZE
COLOR_SIMILARITY_THRESHOLD = 10  # Higher = less detailed but faster
```

Adjust the `COLOR_SIMILARITY_THRESHOLD` according to the level of detail you desire. A higher value will result in less detail but faster processing.

### Step 3: Setting Color Picker Locations

In `main.py`, set the coordinates for the color picker locations:

```python
COLOR_PICKER_POSITION = (640, 855)
COLOR_CHANGE_TAB = (1100, 705)
FINALIZE_COLOR_CHANGE = (877, 703)
```

These coordinates correspond to the positions on your screen where the color picker actions need to occur. You can adjust these based on your specific setup.

### Step 4: Adding Images to the Color Picker

To automate adding images to the color picker, include them in the directory where `main.py` is located, and modify the script to reference these images as needed during the color change process.

### Running the Script

With everything configured, you can now run `main.py` to automate the color picking and drawing process on your canvas:

```bash
python main.py
```

## Contributing

If you'd like to contribute to this project, please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License.
```

### Summary:
- **Installation**: The README guides users through the installation of necessary Python libraries.
- **Usage**: Instructions are provided for capturing a screenshot, resizing it, configuring the script, setting color picker locations, and running the automation.
- **Customization**: Users are informed on how to adjust the configuration variables and set up the color picker to work with their specific setup.
- **Contributing and License**: Encourages contributions and specifies the project's license.

This `README.md` should be comprehensive and provide all the necessary information for users to install, configure, and run your project.
