import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

# Loads an image(Selects top left and bottom right of a rectangular area)
image_path = "output_text_image.png"
img = Image.open(image_path)
fig, ax = plt.subplots()
ax.imshow(img)

points = []

def onclick(event):
    if len(points) < 2:
        ix, iy = event.xdata, event.ydata
        print(f'Point selected: ({ix}, {iy})')

        points.append((int(ix), int(iy)))
        
        if len(points) == 2:
            rect = plt.Rectangle(points[0], np.abs(points[1][0]-points[0][0]), np.abs(points[1][1]-points[0][1]), fill=False, edgecolor='red', linewidth=2)
            ax.add_patch(rect)
            plt.draw()
            
            # Displays rectangle details
            print(f"Rectangle Coordinates: {points[0]} to {points[1]}")

            print(f"OLED Display Coordinates:")
            print(f"Start Row: {points[0][1]}, End Row: {points[1][1]}")
            print(f"Start Column: {points[0][0]}, End Column: {points[1][0]}")


            crop_img = img.crop((points[0][0], points[0][1], points[1][0], points[1][1]))
            crop_img.show()

fig.canvas.mpl_connect('button_press_event', onclick)
plt.show()
