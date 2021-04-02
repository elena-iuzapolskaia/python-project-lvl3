start:
	poetry run page-loader --output /home/ubuntu/dev/ https://www.sheldonbrown.com/web_sample1.html

test:
	poetry run pytest -vv

test-coverage:
	poetry run coverage run -m pytest -vv
	poetry run coverage xml

install:
	poetry install

update:
	pip3 uninstall hexlet-code
	poetry build
	pip3 install --user dist/*.whl

build:
	poetry build

package-install:
	pip3 install --user dist/*.whl

package-uninstall:
	pip3 uninstall hexlet-code

lint:
	poetry run flake8 page_loader

