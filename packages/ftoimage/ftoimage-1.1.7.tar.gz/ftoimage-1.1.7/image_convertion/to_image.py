from pdf2image import convert_from_path
import glob
import PIL
import PIL.Image
import PIL.ImageFont
import PIL.ImageOps
from resume_text.resume2text import get_raw
import PIL.ImageDraw

PIXEL_ON = 0  # PIL color to use for "on"
PIXEL_OFF = 255  # PIL color to use for "off"

def get_image_from_pdf(pdf_path):
    """
    Fcuntion that takes pdf path and returns the first page of the pdf
    :param pdf_path: PDF path
    :return: First page
    """
    to_save_path = pdf_path.replace('.pdf', '.jpg')
    glob_path = glob.glob(to_save_path)
    if not glob_path:
        pages = convert_from_path(pdf_path, 500)
        return pages[0]


def convert_to_image(path):
    """
    Function takes pdf and converts it to jpg and saves it
    :param pdf_path: PDF PATH
    :param jpg_path: JPG PATH. OPTIONAL
    :return: None
    """
    extension = path.split('.')[-1]
    if extension == 'pdf':
        to_save_path = path.replace('.pdf', '.jpg')
        # to_save_name = os.path.abspath(to_save_path)
        glob_path = glob.glob(to_save_path)
        if not glob_path:
            pages = convert_from_path(path, 500)
            pages[0].save(to_save_path)
            print('Created image')
    else:
        to_save_path = path.replace('.' + extension, '.jpg')
        text = get_raw(path)
        lines = text.splitlines()
        img = text_image(lines)
        img.save(to_save_path)

    return to_save_path


def text_image(lines, font_path=None):
    """Convert text file to a grayscale image with black characters on a white background.

    arguments:
    text_path - the content of this file will be converted to an image
    font_path - path to a font file (for example impact.ttf)
    """
    grayscale = 'L'
    # parse the file into lines

    # choose a font (you can see more detail in my library on github)
    large_font = 20  # get better resolution with larger size
    font_path = font_path or 'cour.ttf'  # Courier New. works in windows. linux may need more explicit path
    try:
        font = PIL.ImageFont.truetype(font_path, size=large_font)
    except IOError:
        font = PIL.ImageFont.load_default()
        print('Could not use chosen font. Using default.')

    # make the background image based on the combination of font and lines
    pt2px = lambda pt: int(round(pt * 96.0 / 72))  # convert points to pixels
    max_width_line = max(lines, key=lambda s: font.getsize(s)[0])
    # max height is adjusted down because it's too large visually for spacing
    test_string = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    max_height = pt2px(font.getsize(test_string)[1])
    max_width = pt2px(font.getsize(max_width_line)[0])
    height = max_height * len(lines)  # perfect or a little oversized
    width = int(round(max_width + 40))  # a little oversized
    image = PIL.Image.new(grayscale, (width, height), color=PIXEL_OFF)
    draw = PIL.ImageDraw.Draw(image)

    # draw each line of text
    vertical_position = 5
    horizontal_position = 5
    line_spacing = int(round(max_height * 0.8))  # reduced spacing seems better
    for line in lines:
        draw.text((horizontal_position, vertical_position),
                  line, fill=PIXEL_ON, font=font)
        vertical_position += line_spacing
    # crop the text
    c_box = PIL.ImageOps.invert(image).getbbox()
    image = image.crop(c_box)
    return image




def create_images_from_paths(training_paths, test_paths):
    training_images, test_images = [], []
    for training_path in training_paths:
        train_img = get_image_from_pdf(training_path)
        training_images.append(train_img)
    for test_path in test_paths:
        test_img = get_image_from_pdf(test_path)
        test_images.append(test_img)

    return training_images, test_images


def save_images_within_paths(training_paths, test_paths):
    for training_path in training_paths:
        convert_to_image(training_path)
    for test_path in test_paths:
        convert_to_image(test_path)
