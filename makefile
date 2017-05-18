# makefile for theia

# remove compiled modules
clean-pyc:
	find . -name "*.pyc" -exec rm --force {} +


# remove compiled documentation
clean-doc:
	find doc/ -name "*.vrb" -exec rm --force {} +
	find doc/ -name "*.toc" -exec rm --force {} +
	find doc/ -name "*.synctex.gz" -exec rm --force {} +
	find doc/ -name "*.snm" -exec rm --force {} +
	find doc/ -name "*.out" -exec rm --force {} +
	find doc/ -name "*.nav" -exec rm --force {} +
	find doc/ -name "*.log" -exec rm --force {} +
	find doc/ -name "*.aux" -exec rm --force {} +

# remove compiled tutos
clean-tutos:
	find tutos/ -name "*.opt" -exec rm --force {} +
	find tutos/ -name "*.opt.ps" -exec rm --force {} +

# remove build data
clean-build:
	rm -rf build
	rm -rf dist
	rm -rf theia.egg-info

# clean all
clean-all: clean-pyc clean-doc clean-tutos

# tests
test-optics:
	@python tests/test_optics.py

test-rendering:
	@python tests/test_rendering.py

test-tree:
	@python tests/test_tree.py

test-running:
	@cd tests ; python test_simulation.py

#build theia
go:
	@python setup.py install --user
