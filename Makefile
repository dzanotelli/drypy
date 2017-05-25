# Semplifing the pip/wheel package building ...
#
# PROJECT_NAME must have underscore in the place of spaces
PROJECT_NAME=drypy

.PHONY: msg_src msg_whl src whl clean

msg_whl:
	@echo "=== " $(PROJECT_NAME) " ==="
	@echo "Building the binary wheel package ..."
	@echo ""

msg_src:
	@echo "=== " $(PROJECT_NAME) " ==="
	@echo "Building the source tarball package ..."
	@echo ""

src: msg_src
	python setup.py sdist

whl: msg_whl
	python setup.py bdist_wheel

clean:
	-rm -rf build
	-rm -rf $(PROJECT_NAME).egg-info
	-rm -rf dist
