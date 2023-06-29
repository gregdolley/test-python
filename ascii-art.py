#---------------------------------------------------------------------------------------------
# File: ascii-art.py
# Author: Greg Dolley
# Date: 6/28/2023
#
# This Python script can take any color image, no matter how big or complex, and redraw a
# very realistic version of it using only ASCII art. Not only can it do this with just
# ASCII art, but it can do it while being constrained to only using 11 basic ASCII 
# characters.
#
# TODO: this code is messy and I think it can be refactored into much neater and simpler code.
# Also, remove this file from the test-python project and put it in its own project.
#---------------------------------------------------------------------------------------------
from math import ceil

from PIL import Image, ImageDraw, ImageFont

ASCII_CHARS = ["@", "#", "$", "%", "?", "*", "+", ";", ":", ",", "."]

def main():
    try:
        image, new_image_width = get_user_config()
        image = resize(image, int(new_image_width, base=10) if new_image_width.isnumeric() else image.width)

        greyscale_image = image.convert("L") # convert image to greyscale
        ascii_str = pixels_to_ascii_chars(greyscale_image)
        img_width = greyscale_image.width
        ascii_img=""

        # split the string based on width  of the image
        for i in range(0, len(ascii_str), img_width):
            ascii_img += ascii_str[i:i+img_width] + "\n"

        # save the string to a file to check for accuracy
        with open("ascii_image.txt", "w") as f: f.write(ascii_img)

        # convert the text file to an image as if it were a screenshot
        textfile_to_image("ascii_image.txt").save("ascii_image.png")
    except:
        pass


def get_user_config():
    path = input("Enter the path to the image file: ")
    
    try:
        image = Image.open(path)
    except:
        print("Unable to open that image file. Please check your path and try again.")
        raise

    new_image_width = input("Resize input image to the following width (leave blank to skip): ")
    return image, new_image_width


def pixels_to_ascii_chars(image):
    pixels = image.getdata()
    ascii_str = ""

    for pixel in pixels:
        ascii_str += ASCII_CHARS[pixel//25]
    return ascii_str


def resize(image, new_width):
    if new_width == image.width: return image
    
    new_height = new_width * image.height / image.width
    return image.resize((new_width.__round__(), new_height.__round__()))


def textfile_to_image(textfile_path):
    # remove any trailing white spaces from each line
    with open(textfile_path) as f:
        lines = tuple(line.rstrip() for line in f.readlines())

    font_filename = "c:/windows/fonts/consola.ttf"

    try:
        font = ImageFont.truetype(font_filename, size=12)
    except IOError:
        print(f'Could not load font "{font_filename}".')
        raise

    # find tallest line out of the entire set; that height will be used 
    # on _all_ the lines that are rendered to the image file
    tallest_line = max(lines, key=lambda line: font.getbbox(line)[3])
    max_line_height = font.getbbox(tallest_line)[3]+font.getmetrics()[1]
    image_height = int(ceil(max_line_height * len(lines)))

    # similar to above, find the line that will require the most number
    # of horizontsl pixels
    widest_line = max(lines, key=lambda s: font.getbbox(s)[2])
    max_line_width = font.getbbox(widest_line)[2]
    image_width = int(ceil(max_line_width))

    # create image and drawing objects (default background color of 
    # image is specified by the "color" parameter)
    image = Image.new("L", (image_width, image_height), color=255) # "L" for 8-bit greyscale palette
    draw = ImageDraw.Draw(image)
    draw.fontmode = "1" # turns off anti-aliasing on TT fonts

    # draw each line of text onto image
    horizontal_position = 0
    for i, line in enumerate(lines):
        vertical_position = int(round(i * max_line_height))
        draw.text((horizontal_position, vertical_position), line, fill=0, font=font)

    return image


if __name__ == '__main__':
    main()
