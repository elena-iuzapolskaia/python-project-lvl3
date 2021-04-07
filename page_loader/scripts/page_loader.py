from .name_creator import make_name, make_filename, make_img_name
import argparse
from pathlib import Path
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
import requests


def parse_cli_args():
    parser = argparse.ArgumentParser(description='Download page')
    parser.add_argument('-O', '--output', help='set output path')
    parser.add_argument('link')
    args = parser.parse_args()

    if not args.output:
        args.output = ''
    return (args.link, Path.cwd() / Path(args.output))


def make_filepath_str(filepath):
    ''' convert pathlib.Path to string'''

    full_path = filepath.absolute()
    return full_path.as_posix()


def get_all_images(filepath, img_folder, link):
    ''' download all images from saved page'''

    with open(filepath) as f:
        page = f.read()
    soup = bs(page, 'lxml')

    for img in soup.find_all('img'):
        img_url = img.get('src')
        if not img_url or 'http' in img_url:
            continue
        img_url = urljoin(link, img_url)
        img_response = requests.get(img_url)
        img_name = make_img_name(img_url)
        img_path = img_folder / img_name
        with open(img_path, "wb") as img_file:
            img_file.write(img_response.content)
        img['src'] = f'{img_folder.stem}/{img_name}'

    with open(filepath, 'w') as f:
        f.write(soup.prettify(formatter="html5"))


def download(link, folder_path):
    ''' download page and page's content'''
    foldername = f'{make_name(link)}_files'
    print(foldername)
    filename = Path(make_filename(link))
    file_path = folder_path / filename
    imgs_path = folder_path / foldername
    if not imgs_path.is_dir():
        imgs_path.mkdir()

    page = requests.get(link)
    with open(file_path, 'w') as f:
        f.write(page.text)

    get_all_images(file_path, imgs_path, link)

    return make_filepath_str(file_path)


def main():
    link, file_path = parse_cli_args()
    print(download(link, file_path))


if __name__ == '__init__':
    main()
