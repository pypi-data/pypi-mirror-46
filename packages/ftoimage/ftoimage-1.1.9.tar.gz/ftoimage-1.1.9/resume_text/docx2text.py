import docx2txt


# import glob

def docx2text(path):
    content = docx2txt.process(path)

    return content

#
# paths = glob.glob(
#     '../data/20 Job Ad/*docx')  # This program does not work with multiple ones. You gotta do it one by one
#   # put this in a loop and iterate, create pandas df and put everything there
# path = paths[0]
# print(docx2text(path))
