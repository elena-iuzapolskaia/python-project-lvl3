import re


def make_name(link):
    ''' change link to string without scheme and special symbols'''
    slashes_pos = link.find('//')
    no_scheme_link = link[slashes_pos + 2:]

    name = re.sub('[^0-9a-zA-Z]', '-', no_scheme_link)
    return name


def make_filename(link):

    filename = make_name(link)
    return f'{filename}.html'


def make_img_name(img_url):

    slash_pos = img_url.rfind('/')
    img_name = img_url[slash_pos + 1:]
    dot_pos = img_name.rfind('.')
    extention = '.png'
    if dot_pos != -1:
        extention = img_name[dot_pos:]
    else:
        dot_pos = len(img_name)
    full_name = make_name(img_url[:slash_pos + dot_pos + 1])
    return f'{full_name}{extention}'
