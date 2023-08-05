This directory contains some files to run as a test of the tagtomarkdown installation.
It also serves as a demonstration of a set-up for the extension being used as a
Python-Markdown extension as well as a MkDocs extension.

The doc directory and the directories beneath it is a standard MkDocs set-up. The
Markdown file(s) should be placed in the doc/docs directory and the mkdocs program
is putting its HTML output in the doc/site directory.

For the test and demo, one Markdown file has been made: doc/docs/Page1.md.

For running under Python-Markdown, run the produceHtml.py script:

    python3 produceHtml.py

in the directory sample. It should produce a Page1.html file in the directory
sample. It doesn't look so well because of the lack of css files.

For running under MkDocs go down into the doc directory and issue the command:

    mkdocs build

This reads the md files in the doc/docs directory and converts them into HTML files
in the doc/site directory where MkDocs will place a few more files. Because you are
using the *tagtomarkdown* extension, such md files can contain the tags, supported
by this tool, e.g. the table ones: `>row` and `>cell`. 
