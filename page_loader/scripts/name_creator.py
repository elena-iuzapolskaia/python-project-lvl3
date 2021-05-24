import re


def convert_to_str(link):
    """Change link to string without scheme and special symbols."""
    slashes_pos = link.find('//')
    no_scheme_link = link[slashes_pos + 2:]

    return re.sub('[^0-9a-zA-Z]', '-', no_scheme_link)


def make_filename(link):
    return '{0}.html'.format(convert_to_str(link))


def make_img_name(img_url):

    slash_pos = img_url.rfind('/')
    img_name = img_url[slash_pos + 1:]
    dot_pos = img_name.rfind('.')
    extention = '.png'
    if dot_pos == -1:
        dot_pos = len(img_name)
    else:
        extention = img_name[dot_pos:]
    full_name = convert_to_str(img_url[:slash_pos + dot_pos + 1])
    return '{0}{1}'.format(full_name, extention)
