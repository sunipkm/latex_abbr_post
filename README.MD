# Create clickable abbreviations after the fact.

1. Update your `main.tex` with the appropriate imports and newcommands.
2. Change the `abbr_template.tex` file to create a template with adequate `\section` formatting.
3. Create a copy of `abbr_template.tex` and call it `abbr.tex`.
4. Update `process.py` with the list of `.tex` files you want to process.
5. Run `process.py` to generate the new `.tex` files, a new `abbr.tex` and back up the old source `.tex` to `_old.tex`.
6. Generate the LaTeX document. Find `ReplaceMe` in the document: this is where the first occurance of the abbreviation is, and remove the definition of your abbreviation from there.
7. Go into the `abbr.tex` file and update the abbreviation definitions.
8. Recompile the PDF.