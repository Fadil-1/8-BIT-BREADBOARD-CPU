from PIL import Image
import numpy as np
import os

def image_to_hex_encoded(image_path):
    # Loads the image and converts it to grayscale
    img = Image.open(image_path).convert('L')
    
    # Converts image to numpy array
    img_array = np.array(img)
    
    # Normalizes the image to 8 shades of gray
    img_normalized = (img_array // 32) * 32
    
    # Converts to binary with a threshold
    threshold = 85
    img_binary = np.where(img_array > threshold, 0xF, 0x0)
    
    # Encodes grayscale and binary images to hex format
    hex_array_gray, hex_array_binary = [], []
    
    for y in range(img.height):
        for x in range(0, img.width, 2):
            # Processes two pixels at a time for grayscale
            if x + 1 < img.width:  # Check for image width being odd
                left_pixel_gray = img_normalized[y, x] // 32
                right_pixel_gray = img_normalized[y, x + 1] // 32
                hex_array_gray.append(f"0x{left_pixel_gray << 4 | right_pixel_gray:02x}")
            
            # Processes two pixels at a time for binary
            if x + 1 < img.width:  # Checks for image width being odd
                left_pixel_binary = img_binary[y, x]
                right_pixel_binary = img_binary[y, x + 1]
                hex_array_binary.append(f"0x{left_pixel_binary << 4 | right_pixel_binary:02x}")

    # Saves arrays to text files
    with open(f'{os.path.splitext(image_path)[0]}_grayscale_hex.txt', 'w') as f:
        f.write('{')
        f.write(','.join(hex_array_gray))
        f.write('}')

    with open(f'{os.path.splitext(image_path)[0]}_binary_hex.txt', 'w') as f:
        f.write('{')
        f.write(','.join(hex_array_binary))
        f.write('}')

    print("Hex arrays saved successfully.")
    Image.fromarray(img_array).save(f'{os.path.splitext(image_path)[0]}_binary_hex.png')

image_path = "cropped_images/cropped_17.2_KHz.png"  
image_to_hex_encoded(image_path)
