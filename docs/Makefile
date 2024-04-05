# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = source
BUILDDIR      = build

PYTHON        = python
PREPROCESSOR  = source/preproc.py
# Preprocessor call options
STDOPT        =
FILEOPT       =
PRODOPT       =
PRODDIR       =
VOCABOPT      =

# Web publishing options
PUBHOST       = faam-webserver
PUBDIR        = /var/www/html/additional/sphinx/data/main


# Create arg strings from preproccessor options;
#	STDOPT: version number of standard
# 	FILEOPT: product/definition file to produce documentation for
# 	PRODOPT: version number of product
#	PRODDIR: path to product files (if not local)
# 	VOCABOPT: type of vocabulary to include in documentation
STDVER = $(addprefix --standard=,$(word 1,$(STDOPT)))
FILENAME = $(addprefix --file=,$(word 1,$(FILEOPT)))
PRODVER = $(addprefix --product=,$(word 1,$(PRODOPT)))
PRODPATH = $(addprefix --product_path=,$(word 1,$(PRODDIR)))
VOCAB = $(addprefix --vocab=,$(word 1,$(VOCABOPT)))
# $(info $$(STDVER) is $(STDVER))
# $(info $$(FILENAME) is $(FILENAME))
# $(info $$(PRODVER) is $(PRODVER))
# $(info $$(PRODPATH) is $(PRODPATH))
# $(info $$(VOCAB) is $(VOCAB))


# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	@echo "\n"
	@$(PYTHON) "$(PREPROCESSOR)" --help

.PHONY: help Makefile

# Create html and copy to webserver
publish:
	make html
	ssh $(PUBHOST) mkdir -p $(PUBDIR)
	rsync -a  _build/html/ $(PUBHOST):$(PUBDIR)

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(PYTHON) "$(PREPROCESSOR)" $(FILENAME) $(STDVER) $(PRODVER) $(PRODDIR) $(VOCAB)
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)