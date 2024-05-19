from PIL import Image

def crop_image(image_path, start_coord, end_coord, output_path):
    img = Image.open(image_path)
    cropped_image = img.crop((start_coord[0], start_coord[1], end_coord[0], end_coord[1]))
    cropped_image.save(output_path)
    print(f"Image cropped and saved to {output_path}")

image_path = "1.1 MHz.png"
start_coord = (44, 35) # Top left
end_coord = (107, 49)  # Bottom right
output_path = "cropped_1.1_MHz.png"

crop_image(image_path, start_coord, end_coord, output_path)
