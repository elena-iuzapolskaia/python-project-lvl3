import argparse
from pathlib import Path
import requests
import re


def parse_cli_args():
    ''' parse arguments from cli

    '''
    parser = argparse.ArgumentParser(description='Download page')
    parser.add_argument('-O', '--output', help='set output path')
    parser.add_argument('link')
    args = parser.parse_args()

    if not args.output:
        args.output = ''
    return (args.link, Path.cwd() / Path(args.output))


def make_filename(link):

    slashes_pos = link.find('//')
    no_scheme_link = link[slashes_pos + 2:]

    filename = re.sub('[^0-9a-zA-Z]', '-', no_scheme_link)

    return f'{filename}.html'


def make_filepath(filepath):

    full_path = filepath.absolute()
    return full_path.as_posix()


def download(link, folder_path):

    filename = Path(make_filename(link))
    page = requests.get(link)
    filepath = folder_path / filename
    with open(filepath, 'w') as f:
        f.write(page.text)
        return make_filepath(filepath)


def main():

    link, file_path = parse_cli_args()
    print(download(link, file_path))


if __name__ == '__init__':
    main()
