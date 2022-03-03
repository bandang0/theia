# makefile for theia

#variables
EPYOPTS = --name=theia -u http://theia.hopto.org --graph=all \
 		--inheritance=listed -v
PDFLATEXCMD = pdflatex -interaction=nonstopmode

# remove compiled modules
clean-pyc:
	find . -name "*.pyc" -exec rm -r {} +

# remove compiled documentation
clean-doc:
	find doc/ -name "*.vrb" -exec rm -r {} +
	find doc/ -name "*.toc" -exec rm -r {} +
	find doc/ -name "*.synctex.gz" -exec rm -r {} +
	find doc/ -name "*.snm" -exec rm -r {} +
	find doc/ -name "*.out" -exec rm -r {} +
	find doc/ -name "*.nav" -exec rm -r {} +
	find doc/ -name "*.log" -exec rm -r {} +
	find doc/ -name "*.aux" -exec rm -r {} +
	find doc/ -name "*.dvi" -exec rm -r {} +
	find doc/ -name "*.idx" -exec rm -r {} +
	find doc/ -name "*.ilg" -exec rm -r {} +
	find doc/ -name "*.ps" -exec rm -r {} +

# remove compiled tutos
clean-tutos:
	find tutos/ -name "*.opt" -exec rm -r {} +
	find tutos/ -name "*.opt.ps" -exec rm -r {} +
	find tutos/ -name "*.out" -exec rm -r {} +
	find tutos/ -name "*.fcstd" -exec rm -r {} +
	find tutos/ -name "*.fcstd1" -exec rm -r {} +

# clean tests results
clean-tests:
	find tests/ -name "*.opt" -exec rm -r {} +
	find tests/ -name "*.opt.ps" -exec rm -r {} +
	find tests/ -name "*.out" -exec rm -r {} +
	find tests/ -name "*.fcstd" -exec rm -r {} +
	find tests/ -name "*.fcstd1" -exec rm -r {} +

# clean all
clean-all: clean-pyc clean-doc clean-tutos clean-tests

# remove build data
clean-build:
	rm -rf build
	rm -rf dist
	rm -rf theia.egg-info

# tests
test-optics:
	@cd tests ; python test_optics.py

test-rendering:
	@cd tests ; python test_rendering.py

test-tree:
	@cd tests ; pythontest_tree.py

test-simulation:
	@cd tests ; python test_simulation.py

test-syntax:
	@cd tests ; python test_syntax.py

test-geo:
	@cd tests ; python test_geometry.py

test-plain:
	@cd tests ; python test_plain.py

test-regex:
	@cd tests ; python test_regex.py

#compile pdf (do it twice for all the refs to fall into place)
compile-pdf:
	-cd doc/src ; $(PDFLATEXCMD) primer.tex
	-cd doc/src ; $(PDFLATEXCMD) userguide.tex
	-cd doc/src ; $(PDFLATEXCMD) quickref.tex
	-cd doc/src ; $(PDFLATEXCMD) api.tex
	-cd doc/src ; $(PDFLATEXCMD) statusupdate.tex
	-cd doc/src ; $(PDFLATEXCMD) primer.tex
	-cd doc/src ; $(PDFLATEXCMD) userguide.tex
	-cd doc/src ; $(PDFLATEXCMD) quickref.tex
	-cd doc/src ; $(PDFLATEXCMD) api.tex
	-cd doc/src ; $(PDFLATEXCMD) statusupdate.tex

copy-pdf: clean-doc
	mv doc/src/primer.pdf doc/primer.pdf
	mv doc/src/quickref.pdf doc/quickref.pdf
	mv doc/src/api.pdf doc/apiguide.pdf
	mv doc/src/userguide.pdf doc/userguide.pdf
	mv doc/src/statusupdate.pdf doc/statusupdate.pdf

#generate html and pdf from epydoc
epydoc-pdf:
	epydoc --pdf $(EPYOPTS) -o doc/src theia

epydoc-html:
	epydoc --html $(EPYOPTS) -o doc/html theia

#build theia
build-theia:
	@python setup.py install --user

#build documentation
build-doc: compile-pdf copy-pdf

#install all
install: build-theia build-doc clean-pyc clean-build

#uninstall
clear:
	rm -rf ~/.local/lib/python2.7/site-packages/theia*
	rm -rf ~/.local/bin/theia
