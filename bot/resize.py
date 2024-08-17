from PIL import Image

def find_and_save_area(image_path, white_output_path, red_output_path):
    img = Image.open(image_path).convert("RGB")
    white_threshold = (250, 250, 250)
    red_threshold = (150, 80, 80)
    width, height = img.size

    white_left, white_top, white_right, white_bottom = width, height, 0, 0
    red_left, red_top, red_right, red_bottom = width, height, 0, 0

    for y in range(height):
        for x in range(width):
            pixel = img.getpixel((x, y))
            if all(channel >= white_threshold[i] for i, channel in enumerate(pixel)):
                white_left = min(white_left, x)
                white_top = min(white_top, y)
                white_right = max(white_right, x)
                white_bottom = max(white_bottom, y)
            if pixel[0] >= red_threshold[0] and pixel[1] <= red_threshold[1] and pixel[2] <= red_threshold[2]:
                red_left = min(red_left, x)
                red_top = min(red_top, y)
                red_right = max(red_right, x)
                red_bottom = max(red_bottom, y)

    if white_right > white_left and white_bottom > white_top:
        white_bbox = (white_left, white_top, white_right + 1, white_bottom + 1)
        white_cropped_img = img.crop(white_bbox)
        white_cropped_img.save(white_output_path)
        print(f"White area cropped and saved as {white_output_path}. Dimensions: {white_cropped_img.size}")
    else:
        print("No white area found.")

    if red_right > red_left and red_bottom > red_top:
        red_bbox = (red_left, red_top, red_right + 1, red_bottom + 1)
        red_cropped_img = img.crop(red_bbox)
        red_cropped_img.save(red_output_path)
        print(f"Red area cropped and saved as {red_output_path}. Dimensions: {red_cropped_img.size}")
    else:
        print("No red area found.")

if __name__ == "__main__":
    input_image_path = "ss.png"
    white_output_path = "white_cropped.png"
    red_output_path = "red_cropped.png"
    find_and_save_area(input_image_path, white_output_path, red_output_path)
