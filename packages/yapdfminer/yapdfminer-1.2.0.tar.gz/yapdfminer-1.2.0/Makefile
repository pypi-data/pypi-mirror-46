all: help

help:
	@echo "version      - Display the current version from setup.py."
	@echo "test         - Run nose and sample tests."
	@echo "tag          - git tag and push. Supply the tag in an env var, like TAG=1.2.3."
	@echo "clean        - Remove build artifacts."
	@echo "build        - Generate the distribution packages."
	@echo "publish      - Publish to PyPI."

version:
	python3 setup.py --version

test: test-nose test-samples

test-nose::
	@[ -d tmp ] || mkdir tmp
	nosetests

test-samples:
	cd samples && make test

tag:
	git tag $(TAG)
	git push --tags

clean: clean-pyc clean-build
	-cd tools && make clean

clean-pyc:
	-find . -type f -a \( -name "*.pyc" -o -name "*$$py.class" \) | xargs rm
	-find . -type d -name "__pycache__" | xargs rm -r

clean-build:
	rm -rf build/ dist/ .eggs/ *.egg-info/

build:
	python3 setup.py sdist bdist_wheel

publish:
	python3 -m twine upload dist/*
