# makefile for theia

#variables
EPYOPTS = --name=theia -u http://93.71.63.5:56000 --graph=all --inheritance=listed \
		-v
PDFLATEXCMD = pdflatex -interaction=nonstopmode

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
	find doc/ -name "*.dvi" -exec rm --force {} +
	find doc/ -name "*.idx" -exec rm --force {} +
	find doc/ -name "*.ilg" -exec rm --force {} +
	find doc/ -name "*.ps" -exec rm --force {} +

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

#compile pdf (do it twice for all the refs to fall into place)
compile-pdf:
	-cd doc/src ; $(PDFLATEXCMD) primer.tex
	-cd doc/src ; $(PDFLATEXCMD) userguide.tex
	-cd doc/src ; $(PDFLATEXCMD) quickref.tex
	-cd doc/src ; $(PDFLATEXCMD) api.tex
	-cd doc/src ; $(PDFLATEXCMD) primer.tex
	-cd doc/src ; $(PDFLATEXCMD) userguide.tex
	-cd doc/src ; $(PDFLATEXCMD) quickref.tex
	-cd doc/src ; $(PDFLATEXCMD) api.tex


copy-pdf: clean-doc
	mv doc/src/primer.pdf doc/primer.pdf
	mv doc/src/quickref.pdf doc/quickref.pdf
	mv doc/src/api.pdf doc/apiguide.pdf
	mv doc/src/userguide.pdf doc/userguide.pdf

#generate html and pdf from epydoc
epydoc-pdf:
	epydoc --pdf $(EPYOPTS) -o doc/src theia

epydoc-html:
	epydoc --html $(EPYOPTS) -o doc/html theia

#build theia
build-theia:
	@python setup.py install --user

#build documentation
build-doc: compile-pdf compile-pdf compile-pdf copy-pdf
	
#install all
install: build-theia build-doc clean-pyc clean-build

#uninstall
clear:
	rm -rf ~/.local/lib/python2.7/site-packages/theia*
	rm -rf ~/.local/bin/theia
