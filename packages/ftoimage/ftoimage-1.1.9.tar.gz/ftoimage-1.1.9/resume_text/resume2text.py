# from pdf2text import pdftotext
from resume_text.PDFtoText import convertPDFToText
import os
from resume_text.docx2text import docx2text


# Program must be modified if a user opens this with Linux

# get raw text of given 
def get_raw(resume_path):
    '''
    Function takes file path as input and returns 
    text content of file
    '''
    extension = resume_path.split('.')[-1]

    if extension == 'pdf':
        converted_text = convertPDFToText(resume_path)  ## use pdftotext library

    elif extension == 'docx':
        converted_text = docx2text(resume_path)  ## use docx library

    elif extension == 'txt':
        with open(resume_path, 'r', encoding='utf-8-sig') as textfile:
            converted_text = textfile.read()
    else:
        converted_text = None
    return converted_text

    # elif extension == 'doc':
    #     return textract.process(resume_path).decode('utf-8-sig')
    # return fulltext.get(resume_path)  ## use doc library


def get_all_texts(paths):
    """
    This will take paths as input which will have files in them and return the texts as a list with using get_raw function
    :param paths: Paths to files
    :param setting: File extension, can be extracted, to make it ready for APIs, I do it this way.
    :return: Text list
    """
    result = []
    if paths:
        for path in paths:
            extension = '.' + path.split('.')[-1]
            text_path = path.replace(extension, '.txt')
            path_check = os.path.exists(text_path)
            extension_check = extension != '.txt'
            if not path_check:
                cv_text = get_raw(path)
                with open(text_path, 'w', encoding='utf-8-sig') as file:
                    file.write(cv_text)
            elif path_check and extension_check:
                continue
            else:
                with open(text_path, 'r', encoding='utf-8-sig') as file:
                    cv_text = file.read()
            result.append(cv_text)

            print('Finished: ', path)
    return result
