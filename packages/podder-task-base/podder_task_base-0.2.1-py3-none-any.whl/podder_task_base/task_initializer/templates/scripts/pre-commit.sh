#!/usr/bin/env bash

echo 'executing formatters ...'
autopep8 --in-place --recursive --aggressive .
yapf --in-place --recursive .
autoflake --in-place --remove-unused-variables --remove-all-unused-imports --recursive .
isort --recursive .

echo 'executing linters ...'
flake8 --ignore=E501,F811 .

echo 'executing unit tests ...'
python3 -m pytest