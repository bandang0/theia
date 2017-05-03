# makefile for theia

# remove compiled modules
clean-pyc:
	find . -name "*.pyc" -exec rm --force {} +


# remove compiled documentation
clean-doc:

# tests

test-optics:
	python theia/tests/test_optics.py

test-rendering:
	python theia/tests/test_rendering.py

test-tree:
	python theia/tests/test_tree.py

test-simulation:
	python theia/tests/test_simulation.py
