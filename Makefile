start:
	poetry run page-loader --output /home/ubuntu/dev/examples/page_loader http://www.dolekemp96.org/main.htm

start_mac:
	poetry run page-loader --output /Users/Elena/dev/examples/ http://www.dolekemp96.org/main.htm

test:
	poetry run pytest -vv

test-coverage:
	poetry run coverage run -m pytest -vv
	poetry run coverage xml --omit */.venv/*

test-coverage-actions:
	poetry run coverage run -m pytest -vv
	poetry run coverage xml --omit */virtualenvs/*

install:
	poetry install

update:
	pip3 uninstall hexlet-code
	poetry build
	pip3 install --user dist/*.whl

update-mac:
	pip3 uninstall hexlet-code
	poetry build
	pip3 install dist/*.whl

build:
	poetry build

package-install:
	pip3 install --user dist/*.whl

package-uninstall:
	pip3 uninstall hexlet-code

lint:
	poetry run flake8 page_loader

