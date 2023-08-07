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
# IMPORTANT UPDATE (8/6/2023): this file has been moved to the ascii_art_generator project and
# is no longer maintained under this test-python project. The code in this source file started
# as an experiment and consisted of just a couple dozen lines of code. The experiment worked
# so well that I kept on building on top of it and adding new features. This code is no longer
# an experiment and requires its own project/repo.
#---------------------------------------------------------------------------------------------
import argparse
import os
import platform
import sys
import traceback
from math import ceil

from PIL import Image, ImageDraw, ImageFont

ASCII_CHARS = ["@", "#", "$", "%", "?", "*", "+", ";", ":", ",", "."]
DEFAULT_OUTPUT_FILENAME = "ascii_image"

user_font_file = ""

def main():
    image, new_image_width, output_filename = get_user_config()
    image = resize(image, new_image_width)
    print("Generating ASCII art text string...")
    ascii_img_text = generate_ascii_art(image)

    output_text_filename, output_image_filename = get_output_filenames_with_ext(output_filename)
    print("Writing text string to file: {0}".format(output_text_filename))
    with open(output_text_filename, "w") as f: f.write(ascii_img_text) # save the string to a file to check for accuracy        
    print("Done.");
    
    print("Creating image version of ASCII text file...")
    textfile_to_image(output_text_filename).save(output_image_filename) # convert the text file to an image as if it were a screenshot
    print("Done.")

    print(f"ASCII art text file generated: {output_text_filename}")
    print(f"Image version of the same file: {output_image_filename}")

    return 0


def file_exists(filename): return (os.path.isfile(filename) == True)
def convert_image_to_grayscale(image): return image.convert("L")
def disable_antialiasing(renderer): renderer.fontmode = "1" # turns off anti-aliasing on TT fonts (renderer = ImageDraw object)


def generate_ascii_art(input_image):
    greyscale_image = convert_image_to_grayscale(input_image)
    ascii_str = pixels_to_ascii_chars(greyscale_image)
    img_width = greyscale_image.width
    ascii_img_text = ""

    # add line breaks
    for i in range(0, len(ascii_str), img_width):
        ascii_img_text += ascii_str[i:i+img_width] + "\n"
    
    return ascii_img_text


def get_output_filenames_with_ext(output_filename):
    fname_data = dict(filename=output_filename, txt_ext="txt", img_ext="png");
    output_text_filename = "{filename}.{txt_ext}".format(**fname_data)
    output_image_filename = "{filename}.{img_ext}".format(**fname_data)
    return output_text_filename, output_image_filename

    
def draw_text_strings_as_graphical_lines(lines, renderer, line_height, font):
    # draw each line of text onto image
    for i, line in enumerate(lines):
        renderer.text((0, int(round(i * line_height))), line, fill=0, font=font)


def prompt_for_image_file():
    path = ""

    while(len(path) == 0):
        path = input("Enter the path to the image file: ").strip()
        if(len(path) == 0): print("Received blank input.")

    return path


def get_user_config():
    parser = argparse.ArgumentParser(description='Command-line example.')
    parser.add_argument('-o', action='store', dest='output',
                        metavar='FILE',
                        help='Use FILE as output file name (without extension) instead of default (ascii_image.txt/.png)')
    parser.add_argument('-f', action='store', dest='font_file',
                        metavar='FONT_FILE_PATH',
                        help='Use font file FONT_FILE_PATH for ASCII art font instead of default')
    parser.add_argument('-w', action='store', dest='resize_image_width',
                        metavar='RESIZE_IMAGE_PIXEL_WIDTH',
                        help='Resize the input image width to RESIZE_IMAGE_PIXEL_WIDTH pixels before converting to ASCII art (allows you to shrink/grow the input image if it is too big/small)')

    args = parser.parse_args()
    path = prompt_for_image_file()
    image = Image.open(path)
    new_image_width = int(args.resize_image_width, base=10) if "resize_image_width" in args and args.resize_image_width != None else image.width
    output_filename = args.output if "output" in args and args.output != None else DEFAULT_OUTPUT_FILENAME

    return image, new_image_width, output_filename


def pixels_to_ascii_chars(image):
    pixels = image.getdata()
    ascii_str = ""

    for pixel in pixels:
        # TODO: it would be better if this was a non-linear scale based on the grayscale histogram of the image
        ascii_str += ASCII_CHARS[pixel//25]
    return ascii_str


def resize(image, new_width):
    if new_width == None: return image
    if new_width <= 0: return image
    if new_width == image.width: return image # no resize needed
    
    new_height = new_width * image.height / image.width
    return image.resize((new_width.__round__(), new_height.__round__()))


def get_monospace_font_filename():
    operating_system = platform.system()

    if operating_system == "Windows":
        possible_fonts = ["c:/windows/fonts/consola.ttf"]
    elif operating_system == "Linux":
        possible_fonts = ["/usr/share/fonts/truetype/freefont/FreeMono.ttf",
                          "/usr/share/fonts/truetype/ubuntu/UbuntuMono-R.ttf"]
    elif operating_system == "Darwin": # MacOS
        possible_fonts = ["/System/Library/Fonts/Monaco.ttf"]

    for font_file in possible_fonts:
        if file_exists(font_file) == True:
            return font_file

    raise FileNotFoundError("Can't find a suitable font file for your operating system.")


def create_grayscale_image_with_renderer(image_width, image_height):
    # Remember that grayscale images don't have RGB pixel values - they have
    # a single color channel going from 0 (black) to 255 (white) and all shades
    # of gray in between (from darkest gray of 1 to lightest gray of 254).
    # In Image.new() below, "L" is for a 256-color grayscale palette and 
    # "color=255" specifies the default background color should be white.
    image = Image.new("L", (image_width, image_height), color=255)
    return image, ImageDraw.Draw(image)


def read_all_lines_rstrip(textfile_path):
    with open(textfile_path) as f:
        lines = tuple(line.rstrip() for line in f.readlines())
    return lines


def textfile_to_image(textfile_path):
    lines = read_all_lines_rstrip(textfile_path) # read all text lines and put into "lines" array (also rstrip any trailing whitespaces)
    font_filename = get_monospace_font_filename()

    try:
        font = ImageFont.truetype(font_filename, size=12)
    except IOError:
        print(f'Could not load font "{font_filename}".')
        raise

    image_height, max_line_height = sum_pixel_height_for_all_lines(lines, font)
    image_width = calc_widest_line_in_pixels(lines, font)
    new_image, renderer = create_grayscale_image_with_renderer(image_width, image_height)
    disable_antialiasing(renderer)
    draw_text_strings_as_graphical_lines(lines, renderer, max_line_height, font)

    return new_image


def calc_widest_line_in_pixels(lines, font):
    widest_line = max(lines, key=lambda s: font.getbbox(s)[2])
    max_line_width = font.getbbox(widest_line)[2]
    return int(ceil(max_line_width))


def calc_tallest_line_in_pixels(lines, font):
    tallest_line = max(lines, key=lambda line: font.getbbox(line)[3])
    return font.getbbox(tallest_line)[3]+font.getmetrics()[1]


def sum_pixel_height_for_all_lines(lines, font):
    max_line_height = calc_tallest_line_in_pixels(lines, font)
    return int(ceil(max_line_height * len(lines))), max_line_height


def callstack_prompt(from_traceback):
    while True:
        resp = input("Show callstack? (y/n) ").strip()
        if(len(resp) == 0 or resp == "n"): break
        elif(resp == "y"): 
            traceback.print_tb(from_traceback) 
            break
        
        print("Invalid input. Please try again (note: response is case-sensitive).")


if __name__ == '__main__':
    try:
        status = main()

        print("Done.")
        print(f"Exit status code:  {status}")
        
        sys.exit(status)
    except Exception as e:
        print(sys.exc_info()[1])
        callstack_prompt(sys.exc_info()[2])
        sys.exit(-1)
