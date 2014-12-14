# Makefile for LaTeX

TEXFILE	= songbook.tex

all: $(TEXFILE)
	pdflatex -synctex=1 $(TEXFILE)

#make bibtex for this target
bibtex: $(TEXFILE)
	pdflatex $(TEXFILE)
	bibtex $(TEXFILE:.tex=.aux)
	pdflatex $(TEXFILE)
	pdflatex -synctex=1 $(TEXFILE)

clean:
	@rm -f \
	$(TEXFILE:.tex=.aux) \
	$(TEXFILE:.tex=.bbl) \
	$(TEXFILE:.tex=.blg) \
	$(TEXFILE:.tex=.log) \
	$(TEXFILE:.tex=.out) \
	$(TEXFILE:.tex=.toc) \
	$(TEXFILE:.tex=.synctex.gz) \
	$(TEXFILE:.tex=.pdf)

default: all
	pdflatex -synctex=1 $(TEXFILE)


