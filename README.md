# Page loader
[![Actions Status](https://github.com/alena-yudzina/python-project-lvl3/workflows/hexlet-check/badge.svg)](https://github.com/alena-yudzina/python-project-lvl3/actions) [![lint_flake8](https://github.com/alena-yudzina/python-project-lvl3/actions/workflows/flake8.yml/badge.svg)](https://github.com/alena-yudzina/python-project-lvl3/actions/workflows/flake8.yml) [![Maintainability](https://api.codeclimate.com/v1/badges/9942eff314e6dabc2504/maintainability)](https://codeclimate.com/github/alena-yudzina/python-project-lvl3/maintainability) [![Test Coverage](https://api.codeclimate.com/v1/badges/9942eff314e6dabc2504/test_coverage)](https://codeclimate.com/github/alena-yudzina/python-project-lvl3/test_coverage)

This is a CLI utility for downloading the specified webpage from the Internets.

## Installation

``` bash
make install
make build
make package-install
```

## Usage

``` bash
usage: page-loader [-h] [-o OUTPUT] [-l {INFO,DEBUG}] url

Page loader

positional arguments:
  url

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        set output directory
```

## Downloading simple webpage

``` bash
page-loader --output . http://example.com
```

## Downloading webpage with local resources

``` bash
page-loader -o /tmp/ https://ru.hexlet.io/courses
```
