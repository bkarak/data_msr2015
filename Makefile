camera-ready:
	pdflatex msr2015-camera-ready.tex

pdf:
	pdflatex msr.tex
	bibtex msr
	pdflatex msr.tex
	pdflatex msr.tex

clean:
	-rm -f *.aux
	-rm -f *.bbl *.ent *.blg *.log *.out *.dvi *~ *.spl
	-rm -f msr.pdf
	-rm -f msr2015-camera-ready.pdf

