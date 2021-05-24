import filecmp
import tempfile

from pathlib import Path, PosixPath
from page_loader.scripts.page_loader import download


def test_page_downloader():
    testfile_path = Path.cwd() / 'tests' / 'fixtures' / 'www-dolekemp96-org-main-htm.html'

    test_link = 'http://www.dolekemp96.org/main.htm'
    with tempfile.TemporaryDirectory() as tmpdir:

        downloaded_path = PosixPath(download(test_link, tmpdir))
        assert filecmp.cmp(testfile_path, downloaded_path)
