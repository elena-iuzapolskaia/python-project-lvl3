import argparse
import os


def parse_cli_args():
    ''' parse arguments from cli

    '''
    parser = argparse.ArgumentParser(description='Download page')
    parser.add_argument('-O', '--output', help='set output path')
    parser.add_argument('link')
    args = parser.parse_args()
    if not args.output:
        args.output = os.getcwd()
    return (args.link, args.output)


def download(link, file_path):
    print(link)
    print(file_path)


def main():
    link, file_path = parse_cli_args()
    download(link, file_path)


if __name__ == '__init__':
    main()
