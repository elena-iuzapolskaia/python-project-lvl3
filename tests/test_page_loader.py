import filecmp
import tempfile
import requests_mock

from pathlib import Path, PosixPath
from page_loader.scripts.page_loader import download


page_link = 'https://ru.hexlet.io/courses'
link_link = 'https://ru.hexlet.io/assets/application.css'
img_link = 'https://ru.hexlet.io/assets/professions/nodejs.png'
script_link = 'https://ru.hexlet.io/packs/js/runtime.js'

with open('tests/fixtures/test_page/courses.html', 'r') as f:
    page = f.read()
with open('tests/fixtures/test_page/assets/application.css', 'rb') as f:
    link = f.read()
with open('tests/fixtures/test_page/assets/professions/nodejs.png', 'rb') as f:
    img = f.read()
with open('tests/fixtures/test_page/packs/js/runtime.js', 'rb') as f:
    script = f.read()


def test_page_downloader():
    testfile_path = Path.cwd() / 'tests' / 'fixtures' / 'test_page_content' / 'ru-hexlet-io-courses.html'
    # testdir_path = Path.cwd() / 'tests' / 'fixtures' / 'test_page1'
    # common_files = ['www-test1-com-bathing-suit.webp']

    with requests_mock.Mocker() as m:
        m.get(page_link, text=page)
        m.get(link_link, content=link)
        m.get(img_link, content=img)
        m.get(script_link, content=script)
        with tempfile.TemporaryDirectory() as tmpdir:

            downloaded_path = PosixPath(download(page_link, tmpdir))
            assert filecmp.cmp(testfile_path, downloaded_path)
            # assert filecmp.cmpfiles(testdir_path/'www-test1-com_files',
            #                         downloaded_path.parent/'www-test1-com_files', common_files)
