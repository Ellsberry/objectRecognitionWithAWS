"""This program converts a rgb.jpg file into a grayscale.jpg file"""

from PIL import Image
import numpy as np

# Load a jpg image and show it with Pillow

message = True
while message:
    color = input("input the RGB color you want.  Input r for red, g for green, or b for blue")
    if color == 'r' or color == 'g' or color == 'b':
        message = False

image = Image.open('group_of_animals.jpg')
im = np.array(Image.open('group_of_animals.jpg'))

print("line 11:  image bands  ", image.getbands())
width, height = image.size
print(f"Line 13:   width =  {width}    height = {height}")
print("Line 14:    array shape =  ", im.ndim)
# print(im)

if color == "r":
    R = 1
    G = 0
    B = 0

if color == "g":
    R = 0
    G = 1
    B = 0

if color == "b":
    R = 0
    G = 0
    B = 1

for row in range(height):
    for column in range(width):
        im[row, column, 0] *= R
        im[row, column, 1] *= G
        im[row, column, 2] *= B

# convert numpy array to image and display image
image = Image.fromarray(im)
# image = image.convert("L")
image.save("animals_one_color.jpg")
image.show()
print(im)