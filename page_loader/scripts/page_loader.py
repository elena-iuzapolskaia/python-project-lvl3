import argparse
import logging
import requests
import sys

import page_loader.scripts.exceptions as exceptions
from page_loader.scripts.name_creator import convert_to_str, make_filename, make_img_name
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
    parser.add_argument('-O', '--output', help='set output path')
    parser.add_argument('link')
    try:
        args = parser.parse_args()
    except SystemExit:
        sys.exit(0)

    if not args.output:
        args.output = ''
    return (args.link, Path.cwd() / Path(args.output))


def save_all_content(filepath, img_folder, link):

    with open(filepath) as fl:
        page = fl.read()
    soup = bs(page, 'html.parser')
    content = soup.find_all(['img', 'script', 'link'])
    for img in content:
        if img.get('href'):
            img_url = img.get('href')
            attr_type = 'href'
        else:
            img_url = img.get('src')
            attr_type = 'src'
        if img_url and (not urlparse(img_url).hostname or urlparse(link).hostname == urlparse(img_url).hostname):
            img_url = urljoin(link, img_url)

            try:
                response = requests.get(img_url, stream=True)
            except requests.exceptions.RequestException as e:
                raise exceptions.LinkError('Problems with link or connection') from e

            img_response = b''
            spinner = PixelSpinner(f'Loading {img_url} ')
            for data in response.iter_content(chunk_size=10):
                spinner.next()
                img_response += data
            print()

            img_name = make_img_name(img_url)
            img_path = img_folder / img_name
            with open(img_path, 'wb') as img_file:
                try:
                    img_file.write(img_response)
                except OSError as e:
                    raise exceptions.BadInputError("Can't download content to file") from e

            img[attr_type] = '{0}/{1}'.format(img_folder.stem, img_name)

    with open(filepath, 'w') as fs:
        try:
            fs.write(soup.prettify(formatter='html5'))
        except OSError as e:
            raise exceptions.BadInputError("Can't save page to file") from e


def download(link, folder_path):
    """Download page and page's content."""
    foldername = Path('{0}_files'.format(convert_to_str(link)))
    filename = Path(make_filename(link))
    file_path = folder_path / filename
    imgs_path = folder_path / foldername

    try:
        page = requests.get(link)
        page.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise exceptions.LinkError('Problems with link or connection') from e

    if not imgs_path.is_dir():
        try:
            imgs_path.mkdir()
        except OSError as e:
            raise exceptions.BadInputError("Can't download to this directory") from e

    with open(file_path, 'w') as f:
        try:
            f.write(page.text)
        except OSError as e:
            raise exceptions.BadInputError("Can't save page to file") from e

    save_all_content(file_path, imgs_path, link)

    return file_path.absolute().as_posix()


def main():
    link, file_path = parse_cli_args()
    try:
        print(download(link, file_path))
    except exceptions.AppInternalError as e:
        logger.exception(e)
        print(e.args[0])
        sys.exit(1)
    finally:
        sys.exit(0)


if __name__ == '__init__':
    main()
