.DEFAULT_GOAL := all
isort = isort -rc pytest_toolbox tests

.PHONY: install
install:
	pip install -U pip setuptools
	pip install -r tests/requirements.txt
	pip install -e .

.PHONY: isort
isort:
	$(isort)

.PHONY: lint
lint:
	flake8 pytest_toolbox/ tests/
	$(isort) --check-only
	coverage run setup.py check -rms

.PHONY: test
test:
	py.test --cov=pytest_toolbox

.PHONY: testcov
testcov:
	py.test --cov=pytest_toolbox && (echo "building coverage html"; coverage combine; coverage html)

.PHONY: all
all: testcov lint
