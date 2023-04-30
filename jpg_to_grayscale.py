"""This program converts a rgb.jpg file into a grayscale.jpg file"""

from PIL import Image
import numpy as np

# Load a jpg image and show it with Pillow

image = Image.open('group_of_animals.jpg')
im = np.array(Image.open('group_of_animals.jpg'))

print("line 11:  image bands  ", image.getbands())
width, height = image.size
print(f"Line 13:   {width}    {height}")
print("Line 14:    array shape =  ", im.ndim)
print(im)

new_image = np.dot(im[..., :3], [0.299, 0.587, 0.114])
print("Line 18: new_image array shape =  ", new_image.ndim)
print(new_image)
# convert numpy array to image and display image
image = Image.fromarray(new_image)
image = image.convert("L")
image.save("animals_grayscale.jpg")
image.show()
