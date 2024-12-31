.PHONY: install
install:
	pip uninstall -y todo --break-system-packages
	pip install -e . --break-system-packages
