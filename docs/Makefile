# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
BUILDDIR      = ../sphinx-doc
PDFBUILDDIR   = /tmp
PDF           = ../manual.pdf
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = source

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

#latexpdf:
#    @$(SPHINXBUILD) -b latex $(ALLSPHINXOPTS) "$(PDFBUILDDIR)/latex"
#	@echo "Running LaTeX files through pdflatex..."
#    make -C $(PDFBUILDDIR)/latex all-pdf
#    cp $(PDFBUILDDIR)/latex/*.pdf $(PDF)
#    @echo "pdflatex finished; see $(PDF)"

.PHONY: help Makefile latexpdf

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
