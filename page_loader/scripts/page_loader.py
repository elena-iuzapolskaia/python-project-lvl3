import argparse

import requests
from page_loader.scripts.name_creator import convert_to_str, make_filename, make_img_name
from pathlib import Path
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin, urlparse


def parse_cli_args():
    parser = argparse.ArgumentParser(description='Download page')
    parser.add_argument('-O', '--output', help='set output path')
    parser.add_argument('link')
    args = parser.parse_args()

    if not args.output:
        args.output = ''
    return (args.link, Path.cwd() / Path(args.output))


def save_all_content(filepath, img_folder, link):

    with open(filepath) as fl:
        page = fl.read()
    soup = bs(page, 'lxml')
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
            img_response = requests.get(img_url)
            img_name = make_img_name(img_url)
            img_path = img_folder / img_name
            with open(img_path, 'wb') as img_file:
                img_file.write(img_response.content)
            img[attr_type] = '{0}/{1}'.format(img_folder.stem, img_name)

    with open(filepath, 'w') as fs:
        fs.write(soup.prettify(formatter='html5'))


def download(link, folder_path):
    """Download page and page's content."""
    foldername = Path('{0}_files'.format(convert_to_str(link)))
    filename = Path(make_filename(link))
    file_path = folder_path / filename
    imgs_path = folder_path / foldername
    if not imgs_path.is_dir():
        imgs_path.mkdir()

    page = requests.get(link)
    with open(file_path, 'w') as f:
        f.write(page.text)

    save_all_content(file_path, imgs_path, link)

    return file_path.absolute().as_posix()


def main():
    link, file_path = parse_cli_args()
    print(download(link, file_path))


if __name__ == '__init__':
    main()
