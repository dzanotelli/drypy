# Semplifing the pip/wheel package building ...
#
# PROJECT_NAME must have underscore in the place of spaces
PROJECT_NAME="Python_Dryrun"

.PHONY: echo_msg build clean create_pkg

rebuild: echo_msg clean build

echo_msg:
	@echo "=== " $(PROJECT_NAME) " ==="
	@echo "Building the pip/wheel package ..."
	@echo ""

build:
	python setup.py bdist_wheel

clean:
	-rm -rf build
	-rm -rf $(PROJECT_NAME).egg-info
	-rm -rf dist
