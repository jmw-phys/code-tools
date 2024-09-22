#!/usr/local/bin/python3

from PIL import Image
import glob

image_files = sorted(glob.glob('./*.png'))

images = [Image.open(img) for img in image_files]

#images[0].save('animation.gif', save_all=True, append_images=images[1:], duration=500, loop=0)

images[0].save(
    'animation.gif',
    save_all=True,
    append_images=images[1:],
    duration=500,
    loop=0,
    optimize=False,
    quality=95
)


print("GIF Done")

