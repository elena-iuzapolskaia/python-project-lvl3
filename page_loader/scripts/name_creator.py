import re
from urllib.parse import urlparse
import os


def convert_to_str(link):
    """Change link to string without scheme and special symbols."""
    slashes_pos = link.find('//')
    no_scheme_link = link[slashes_pos + 2:]

    return re.sub('[^0-9a-zA-Z]', '-', no_scheme_link)


def make_filename(link):
    return '{0}.html'.format(convert_to_str(link))


def make_img_name(img_url):
    path = urlparse(img_url).path
    extention = os.path.splitext(path)[1]
    dot_pos = img_url.rfind('.')
    
    full_name = convert_to_str(img_url[:dot_pos])
    return '{0}{1}'.format(full_name, extention)
