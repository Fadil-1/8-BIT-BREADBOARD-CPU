import numpy as np
from PIL import Image

def image_to_64x128_grayscale_bytes(image_path):
    # Loads and converts the image
    img = Image.open(image_path)
    img_gray = img.convert('L')  # Converts to grayscale
    img_gray = img_gray.resize((128, 64), Image.ANTIALIAS)  # Resizes to 128x64
    
    # Converts to 8 shades of gray (3 bits per pixel)
    img_8_shades = np.array(img_gray) // 32  # Scales pixel values to 0-7 range
    bytes_array = []
    
    # Processes the image by rows to fit the display format
    for y in range(64):
        for x in range(0, 128, 2):  # Each byte represents 2 pixels
            left_pixel = img_8_shades[y, x] << 4  # High nibble
            right_pixel = img_8_shades[y, x + 1]  # Low nibble
            byte = left_pixel | right_pixel
            bytes_array.append(byte)
    
    return bytes_array, img_gray, img_8_shades

def save_data_and_image(bytes_array, img_gray, img_8_shades, filename_prefix):
    # Converts byte array to hex string and save
    hex_str_array = ["0x{:02x}".format(byte) for byte in bytes_array]
    full_hex_str = ", ".join(hex_str_array)
    with open(f"{filename_prefix}_full.txt", "w") as file:
        file.write(full_hex_str)
    
    # Saves grayscale image for reference
    img_gray.save(f"{filename_prefix}_grayscale.jpg")
    
    # Saves whole image and 8 splits of the image for use on the Arduino Nano.
    portion_len = len(bytes_array) // 8
    for i in range(8):
        start = i * portion_len
        end = start + portion_len
        portion = hex_str_array[start:end]
        portion_str = ", ".join(portion)
        with open(f"{filename_prefix}_portion_{i+1}.txt", "w") as file:
            file.write(portion_str)
    
    # Saves the 8-shade grayscale image
    img_8_shades_img = Image.fromarray(img_8_shades * 32)  # Scale back to 0-255 range for saving
    img_8_shades_img = img_8_shades_img.convert("L")  # Ensure it's in L mode
    img_8_shades_img.save(f"{filename_prefix}_8_shades.jpg")

# Example
#image_path = "79.PNG"
image_path = r"0.PNG"
filename_prefix = "output_image"  # Base name for output files
bytes_array, img_gray, img_8_shades = image_to_64x128_grayscale_bytes(image_path)
save_data_and_image(bytes_array, img_gray, img_8_shades, filename_prefix)
