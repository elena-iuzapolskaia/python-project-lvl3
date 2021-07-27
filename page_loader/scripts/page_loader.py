import argparse
import logging
import requests
import sys

import page_loader.scripts.exceptions as exceptions
from page_loader.scripts.name_creator import convert_to_str, make_filename, make_content_name
from pathlib import Path
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin, urlparse
from progress.spinner import PixelSpinner
from logging import config


LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'formatter': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
    },
    'handlers': {
        's_handler': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'formatter'
        },
        'f_handler': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'formatter': 'formatter',
            'filename': 'debug.log',
            'mode': 'a',
        },
    },
    'loggers': {
        'root': {
            'handlers': ['f_handler'],
            'level': 'INFO',
        },
        'name_creator': {
            'handlers': ['s_handler'],
            'level': 'INFO',
            'propagate': False,
        }
    }
}

config.dictConfig(LOGGING)
logger = logging.getLogger()


def parse_cli_args():
    parser = argparse.ArgumentParser(description='Download page')
    parser.add_argument('-O', '-o', '--output', help='set output path')
    parser.add_argument('link')
    try:
        args = parser.parse_args()
    except SystemExit:
        sys.exit(0)

    if not args.output:
        args.output = ''
    return (args.link, Path.cwd() / Path(args.output))


def download_content(response, attr_value):
    content = b''
    spinner = PixelSpinner(f'Loading {attr_value} ')
    for data in response.iter_content(chunk_size=10):
        spinner.next()
        content += data
    print()
    return content


def get_attr_with_value(tag):
    if tag.get('href'):
        attr_value = tag.get('href')
        attr = 'href'
    else:
        attr_value = tag.get('src')
        attr = 'src'
    if attr_value:
        return attr, attr_value
    return None


def save_all_content(filepath, content_folder, link):

    try:
        with open(filepath) as fl:
            page = fl.read()
    except OSError as e:
        raise exceptions.BadInputError("Can't open downloaded page") from e

    soup = bs(page, 'html.parser')
    content = soup.find_all(['img', 'script', 'link'])
    for tag in content:
        tag_content = get_attr_with_value(tag)
        if not tag_content:
            continue
        attr, attr_value = tag_content

        if urlparse(attr_value).hostname:
            if urlparse(link).hostname != urlparse(attr_value).hostname:
                continue
        attr_value = urljoin(link, attr_value)

        try:
            response = requests.get(attr_value, stream=True)
        except requests.exceptions.RequestException as e:
            raise exceptions.LinkError('Problems with link or connection') from e

        content = download_content(response, attr_value)

        content_name = make_content_name(attr_value)
        content_path = content_folder / content_name
        with open(content_path, 'wb') as content_file:
            try:
                content_file.write(content)
            except OSError as e:
                raise exceptions.BadInputError("Can't download content to file") from e

        tag[attr] = '{0}/{1}'.format(content_folder.stem, content_name)

    with open(filepath, 'w') as fs:
        try:
            fs.write(soup.prettify(formatter='html5'))
        except OSError as e:
            raise exceptions.BadInputError("Can't save page to file") from e


def download(link, folder_path):
    """Download page and page's content."""
    page_folder = Path('{0}_files'.format(convert_to_str(link)))
    page_name = Path(make_filename(link))
    page_path = folder_path / page_name
    content_folder = folder_path / page_folder

    try:
        page = requests.get(link)
        page.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise exceptions.LinkError('Problems with link or connection') from e

    if not content_folder.is_dir():
        try:
            content_folder.mkdir()
        except OSError as e:
            raise exceptions.BadInputError("Can't download to this directory") from e

    with open(page_path, 'w') as f:
        try:
            f.write(page.text)
        except OSError as e:
            raise exceptions.BadInputError("Can't save page to file") from e

    save_all_content(page_path, content_folder, link)

    return page_path.absolute().as_posix()


def main():
    link, file_path = parse_cli_args()
    try:
        print(download(link, file_path))
    except exceptions.AppInternalError as e:
        logger.exception(e)
        print(e.args[0])
        sys.exit(1)


if __name__ == '__init__':
    main()
