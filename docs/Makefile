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
PRODOPT       =
VOCABOPT      =

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	@echo "\n"
	@$(PYTHON) "$(PREPROCESSOR)" --help

.PHONY: help Makefile


# Create arg strings from preproccessor options;
#	1) version number of standard
# 	2) version number of product
# 	3) type of vocabulary to include in documentation
STDVER = $(addprefix --standard=,$(word 1,$(STDOPT)))
PRODVER = $(addprefix --product=,$(word 1,$(PRODOPT)))
VOCAB = $(addprefix --vocab=,$(word 1,$(VOCABOPT)))

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	#$(info $$(STDVER) is $(STDVER))
	#$(info $$(PRODVER) is $(PRODVER))
	#$(info $$(VOCAB) is $(VOCAB))
	@$(PYTHON) "$(PREPROCESSOR)" "$(STDVER)" "$(PRODVER)" "$(VOCAB)"
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)