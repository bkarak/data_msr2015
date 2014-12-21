pdf:
	pdflatex msr.tex
	bibtex msr
	pdflatex msr.tex
	pdflatex msr.tex

clean:
	-rm -f *.aux
	-rm -f *.bbl *.ent *.blg *.log *.out *.dvi *~ *.spl
	-rm -f msr.pdf

