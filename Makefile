.PHONY: install
install:
	pip install -U pip setuptools
	pip install -e .
	pip install -r tests/requirements.txt

.PHONY: isort
isort:
	isort -rc -w 120 pytest_toolbox
	isort -rc -w 120 tests

.PHONY: lint
lint:
	flake8 pytest_toolbox/ tests/
	pytest pytest_toolbox -p no:sugar -q --cache-clear
	coverage run setup.py check -rms

.PHONY: test
test:
	py.test --cov=pytest_toolbox

.PHONY: testcov
testcov:
	py.test --cov=pytest_toolbox && (echo "building coverage html"; coverage combine; coverage html)
