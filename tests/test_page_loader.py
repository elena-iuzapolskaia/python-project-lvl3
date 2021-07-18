import filecmp
import tempfile
import requests_mock

from pathlib import Path, PosixPath
from page_loader.scripts.page_loader import download


def test_page_downloader():
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
    testfile_path = Path.cwd() / 'tests' / 'fixtures' / 'test_page_content' / 'ru-hexlet-io-courses.html'
    testdir_path = Path.cwd() / 'tests' / 'fixtures' / 'test_page_content' / 'ru-hexlet-io-courses_files'
    # common_files = ['www-test1-com-bathing-suit.webp']

    with requests_mock.Mocker() as m:
        m.get(page_link, text=page)
        m.get(link_link, content=link)
        m.get(img_link, content=img)
        m.get(script_link, content=script)
        with tempfile.TemporaryDirectory() as tmpdir:

            downloaded_path = PosixPath(download(page_link, tmpdir))
            assert filecmp.cmp(testfile_path, downloaded_path, shallow=False)
            dc = filecmp.dircmp(testdir_path,
                                downloaded_path.parent / 'ru-hexlet-io-courses_files')
            assert len(dc.left_only + dc.right_only) == 0


def test_page_2_downloader():
    page_link = 'https://site.com/blog/about'
    link_link = '/blog/about/assets/styles.css'
    img_link = '/photos/me.jpg'
    script_link = 'https://site.com/assets/scripts.js'

    with open('tests/fixtures/test_page_2_content/site-com-blog-about_files/site-com-blog-about.html', 'r') as f:
        page = f.read()
    with open('tests/fixtures/test_page_2_content/site-com-blog-about_files/site-com-blog-about-assets-styles.css', 'rb') as f:
        link = f.read()
    with open('tests/fixtures/test_page_2_content/site-com-blog-about_files/site-com-photos-me.jpg', 'rb') as f:
        img = f.read()
    with open('tests/fixtures/test_page_2_content/site-com-blog-about_files/site-com-assets-scripts.js', 'rb') as f:
        script = f.read()
    testfile_path = Path.cwd() / 'tests' / 'fixtures' / 'test_page_2_content' / 'site-com-blog-about.html'
    testdir_path = Path.cwd() / 'tests' / 'fixtures' / 'test_page_2_content' / 'site-com-blog-about_files'

    with requests_mock.Mocker() as m:
        m.get(page_link, text=page)
        m.get(link_link, content=link)
        m.get(img_link, content=img)
        m.get(script_link, content=script)
        download(page_link, '/Users/Elena/dev/examples')
        with tempfile.TemporaryDirectory() as tmpdir:

            downloaded_path = PosixPath(download(page_link, tmpdir))
            assert filecmp.cmp(testfile_path, downloaded_path, shallow=False)
            dc = filecmp.dircmp(testdir_path,
                                downloaded_path.parent / 'site-com-blog-about_files')
            assert len(dc.left_only + dc.right_only) == 0

