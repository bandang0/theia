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
	find tutos/ -name "*.out" -exec rm --force {} +


# clean tests results
clean-tests:
	find tests/ -name "*.opt" -exec rm --force {} +
	find tests/ -name "*.opt.ps" -exec rm --force {} +
	find tests/ -name "*.out" -exec rm --force {} +

# clean all
clean-all: clean-pyc clean-doc clean-tutos clean-tests

# remove build data
clean-build:
	rm -rf build
	rm -rf dist
	rm -rf theia.egg-info

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

#compile pdf
go-pdf:
	cd doc/ ; pdflatex -interaction=nonstopmode primer.tex
	cd doc/ ; pdflatex -interaction=nonstopmode userguide.tex
	cd doc/ ; pdflatex -interaction=nonstopmode apiguide.tex
	cd doc/ ; pdflatex -interaction=nonstopmode quickref.tex

#build documentation
go-doc:	go-pdf clean-doc

#install all
install: go go-doc clean-pyc clean-build

#uninstall
clear:
	rm -rf ~/.local/lib/python2.7/site-packages/theia*
	rm -rf ~/.local/bin/theia
