brain-games:
	poetry run brain-games

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

