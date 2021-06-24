import filecmp
import tempfile
import requests_mock
import requests

from pathlib import Path, PosixPath
from page_loader.scripts.page_loader import download

link = 'http://www.test1.com'
img_link = 'http://www.test1.com/bathing-suit.webp'
with open('/Users/Elena/dev/test_page/index.html', 'r') as f:
    page = f.read()
with open('/Users/Elena/dev/test_page/bathing-suit.webp', 'rb') as f:
    img = f.read()


def test_page_downloader():
    testfile_path = Path.cwd() / 'tests' / 'fixtures' / 'test_page1' / 'www-test1-com.html'
    testdir_path = Path.cwd() / 'tests' / 'fixtures' / 'test_page1'
    common_files = ['www-test1-com-bathing-suit.webp']
    link = 'http://www.test1.com'

    with requests_mock.Mocker() as m:
        m.get(link, text=page)
        m.get(img_link, content=img)
        with tempfile.TemporaryDirectory() as tmpdir:

            downloaded_path = PosixPath(download(link, tmpdir))
            assert filecmp.cmp(testfile_path, downloaded_path)
            # assert filecmp.cmpfiles(testdir_path/'www-test1-com_files',
            #                         downloaded_path.parent/'www-test1-com_files', common_files)

