# makefile for theia

# remove compiled modules
clean-pyc:
	find . -name "*.pyc" -exec rm --force {} +


# remove compiled documentation
clean-doc:

# tests

test-optics:
	python tests/test_optics.py

test-rendering:
	python tests/test_rendering.py

test-tree:
	python tests/test_tree.py

test-simulation:
	python tests/test_simulation.py
