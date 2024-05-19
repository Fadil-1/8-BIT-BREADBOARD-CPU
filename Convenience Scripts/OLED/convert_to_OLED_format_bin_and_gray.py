from PIL import Image, ImageFilter
import numpy as np
import os

def image_to_64x128_encoded(image_path):
    img = Image.open(image_path).convert('L')
    img_resized = img.resize((128, 64), Image.ANTIALIAS)
    # With and without filtering
    img = img_resized.filter(ImageFilter.GaussianBlur(radius=1))

    img_array = np.array(img_resized)
    # Converts to 8 shades of gray (3 bits per pixel)
    img_normalized = (img_array // 32) * 32  # Scales pixel values to 0-7 range

    threshold = 85
    img_binary = np.where(img_array > threshold, 0xF, 0x0)

    hex_array_gray, hex_array_binary = [], []

    for y in range(64):
        for x in range(0, 128, 2):
            # Processes two pixels at a time for grayscale
            left_pixel_gray = img_normalized[y, x] // 32
            right_pixel_gray = img_normalized[y, x + 1] // 32
            hex_array_gray.append(f"0x{left_pixel_gray << 4 | right_pixel_gray:02x}")

            # Processes two pixels at a time for binary
            left_pixel_binary = img_binary[y, x]
            right_pixel_binary = img_binary[y, x + 1]
            hex_array_binary.append(f"0x{left_pixel_binary << 4 | right_pixel_binary:02x}")

    def save_arrays_and_splits(array, name):
        # Saves whole image and 8 splits of the image for use on the Arduino Nano.
        os.mkdir(f'./{name}_image')
        with open(f'./{name}_image/{name}_full_array.txt', 'w') as file:
            file.write(','.join(array))

        # Note: The splitting in 8 is just for testing purposes on the Arduino nano, which does not 
        # have enough dynamic memory to hold the full image byte array. 
        split_length = len(array) // 8
        for i in range(8):
            split_array = array[i*split_length:(i+1)*split_length]
            with open(f'./{name}_image/{name}_split_{i+1}.txt', 'w') as file:
                file.write(','.join(split_array))

    save_arrays_and_splits(hex_array_gray, 'grayscale')
    save_arrays_and_splits(hex_array_binary, 'binary')

    # Saves grayscale and binary images
    Image.fromarray(img_normalized).save(r'./grayscale_image/grayscale_image.png')
    Image.fromarray((img_binary * 255).astype(np.uint8)).convert('L').save(r'./binary_image/binary_image.png')

#os.mkdir('binary_image')
#os.mkdir('grayscale_image')

image_path = "./text_to_images/17.2 KHz.png"
image_to_64x128_encoded(image_path)
