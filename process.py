# %% Imports
import os
import re
import sys
from typing import List
# %%
def load_file(filename: str):
    with open(filename, "r") as f:
        return f.read()
    
def parse_tokens(text: str):
    textftr = text.replace("\r", " ").replace("\n", " ") # replace newlines with spaces
    words = re.findall(r"[ \(][A-Z][A-Z]+", textftr) # find all caps words after a space or (
    words = list(map(lambda x: x[1:], words)) # remove the space
    words = list(set(words)) # remove duplicate
    words.sort() # sort
    return words

def replace_tokens(text: str, tokens: List[str]):
    for token in tokens:
        words = re.findall(r"\(" + token + r"[a-z]*" + r"\)", text) # find all occurences of the original token
        if len(words) == 0:
            print(f"Warning: original {token} not found")
            continue
        for word in words:
            text = text.replace(word, f'\\aclink{{{token}}}')
        words = re.findall(r"([^\w\s\{]? )(" + token + r")", text) # find all occurences of the token
        if len(words) == 0:
            continue
        for thing in words:
            to_replace = token
            replacement = f'\\aclink{{{token}}}'
            if len(thing) > 0:
                to_replace = ''
                for th in thing[:-1]:
                    to_replace += th
                replacement = to_replace + replacement
                to_replace += token
            text = text.replace(to_replace, replacement)
    return text

def store_file(filename: str, text: str):
    with open(filename, "w") as f:
        f.write(text)

def store_abbrs(tokens: List[str], filename: str):
    if not os.path.isfile(filename):
        raise FileNotFoundError
    if '_template.tex' not in filename:
        raise ValueError("Abbreviations file must be a .tex file and end with _template.tex")
    text = load_file(filename) # load the template
    outname = filename.replace('_template.tex', '.tex')
    first_letter = '0'
    tokens = list(set(tokens))
    tokens.sort()
    for token in tokens:
        if token[0] != first_letter:
            first_letter = token[0]
            text += f'\n\\subsection*{{{first_letter}}}'
        text += f'\n\\acrotarget{{{token}}}{{{"ReplaceMe"}}}\\\\'
    store_file(outname, text)

def process_file(filename: str, dryrun: bool = True)->List[str]:
    """Process a file and get tokens

    Args:
        filename (str): Name of file

    Returns:
        List[str]: List of tokens
    """
    if not os.path.isfile(filename):
        raise FileNotFoundError
    if '.tex' not in filename:
        raise ValueError("File must be a .tex file")
    text = load_file(filename)
    tokens = parse_tokens(text)
    text = replace_tokens(text, tokens)
    outname = filename
    if dryrun:
        outname = filename.replace('.tex', '_out.tex')
    else:
        os.rename(filename, filename.replace('.tex', '_old.tex'))
    store_file(outname, text)
    return tokens

def restore_file(filename: str, from_dryrun: bool = True)->str:
    """Restore a file from process_file.

    Args:
        filename (str): File name.
        from_dryrun (bool, optional): Whether to restore from a dry run. Defaults to True.

    Returns:
        str: File name of the source file
    """
    if '.tex' not in filename:
        raise ValueError("File must be a .tex file")
    if from_dryrun:
        outname = filename.replace('.tex', '_out.tex')
    else:
        outname = filename.replace('.tex', '_old.tex')
    if not os.path.isfile(outname):
        raise FileNotFoundError
    os.rename(outname, filename)
    return outname

# %% Process the file
dryrun = False
input_files = ['textsrc.tex'] # list of files to process
tokens = [] # list of tokens
for file in input_files:
    itokens = process_file(file, dryrun=dryrun)
    tokens += itokens
store_abbrs(tokens, 'abbr_template.tex')

# %% Restore files
for file in input_files: restore_file(file, from_dryrun=dryrun)

# %%
