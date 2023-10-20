#!/bin/bash
rm -vf *.toc *.aux *.lo* *.blg *.bbl *.fls *.dvi *.fdb* *.dvi *.pdf *.out *.synctex*

mv textsrc_old.tex textsrc.tex
cp abbr_template.tex abbr.tex