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
STDVER        =
STDFILE       =
PRODVER       =
PRODDIR       =


# Web publishing options
PUBHOST       = faam-webserver
PUBDIR        = /var/www/html/additional/sphinx/spif


# Create arg strings from preproccessor options;
#	STDVER: version number of standard
# 	STDFILE: One or more product/definition file/s, comma-delineated.
#      First file is assumed to be minimal example file with mandatory only vocab
# 	PRODOPT: version number of product
#	PRODDIR: path to product files (if not local)
comma = ,
empty =
space = $(empty) $(empty)

STD = $(addprefix --standard=,$(word 1,$(STDVER)))
# Convert comma-delineated list to whitespace-delineated
FILELIST = $(addprefix --file$(space),$(word 1,$(STDFILE)))
FILENAME = $(subst $(comma),$(space),$(FILELIST))
PRODUCT = $(addprefix --product=,$(word 1,$(PRODVER)))
PRODPATH = $(addprefix --product_path=,$(word 1,$(PRODDIR)))

# $(info $$(FILELIST) is $(FILELIST))
# $(info $$(FILENAME) is $(FILENAME))
# $(info $$(STD) is $(STD))
# $(info $$(PRODUCT) is $(PRODUCT))
# $(info $$(PRODPATH) is $(PRODPATH))


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
	rsync -a  build/html/ $(PUBHOST):$(PUBDIR)

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(PYTHON) "$(PREPROCESSOR)" $(FILENAME) $(STD) $(PRODUCT) $(PRODPATH)
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
