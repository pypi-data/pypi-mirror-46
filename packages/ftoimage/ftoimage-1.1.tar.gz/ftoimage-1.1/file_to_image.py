from image_convertion.to_image import convert_from_path, text_image
import glob
from resume_text.resume2text import get_raw


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