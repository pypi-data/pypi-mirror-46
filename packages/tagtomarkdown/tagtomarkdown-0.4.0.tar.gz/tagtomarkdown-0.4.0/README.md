## tagtomarkdown

A [Python3 Markdown](https://github.com/Python-Markdown/markdown) preprocessor
to transform a home made tag language for defining tables into the *Markdown*
table format.

The preprocessor can be used as an extension to
[Python Markdown](https://python-markdown.github.io/) like this:

    from tagtomarkdown import TableTagExtension
     ...
    ext_tables = TableTagExtension()
    html = markdown.markdown('Line 1\n>br text\nLine 3 and last', extensions=[ext_tables], output_format='html5')

or:

    from tagtomarkdown import TableTagExtension
     ...
    html = md.convert('Line 1\n>br text\nLine 3 and last', extensions=[TableTagExtension()], output_format='html5')

or:

    html = md.convert('Line 1\n>br text\nLine 3 and last', extensions=['tables', 'tagtomarkdown'], output_format='html5')

It can also be used as an [MkDocs](https://www.mkdocs.org/) extension by referring
it in a document's *mkdocs.yml* file like this:

    markdown_extensions:
      - tagtomarkdown
      - tables
        ...

Your *MkDocs* instance must be installed under Python version 3, or you will
get something like "tagtomarkdown not found".

### Tags supported by the preprocessor

Please note that the source distribution contains a directory, `sample`,
showing test and example use of the tool. There is a `README.txt` file there
explaining the files. It might be quicker to get the idea by looking at the example
than by reading the below, you might consider the below as a reference manual.

The syntax of the tags supported is: Tags are identified by a `>` character, followed
by a name. The `>` character must be at the beginning of a new line.

The supported tags are:

#### Tables

Tables are started the usual *Markdown* way, i.e. like this:

```
|:-:|---|
|No.|Subject|
```

The rows following the header row are then defined using the language, defined below.
A table is ended by either a blank line or by the ```&gt;/row``` tag.

**&gt;row**
:   Produces a new table row

**&gt;row noOfColumns**
:   Produces a new table row and saves the number of columns. This number is being
    used later when a new row is defined by another >row statement. The table
    logic will then fill in possible missing cells to finish the previous row. 
    This parameter must be given only in the first >row statement in a given table.

**&gt;cell [optional cell text in same line]**
:   Produces a table cell. Contents can be of more lines.

**&gt;cell &ast;start [symbol]**
:   Sets a counter to the value 1 and inserts the 1 in a new cell,
    *symbol* is stored as a substitutable symbol of name symbol and the value 1

**&gt;cell &ast;incr [symbol]**
:   Increments the counter and writes its value in a new cell.
    *symbol* is stored as a substitutable symbol of name symbol and the value of
    the number substituting *incr.

**&gt;/row [&ast;tableno] [optional table caption text in same line]**
:   End a table definition. If the table definitions ends with a blank line,
    this tag is not necessary.
    *tableno indicates that the caption should be preceded by the text "Table n: "
    optional table caption: If given, a line with its text is written beneath the table. 

#### Ordered lists

**&gt;li &ast;start [symbol]**
:   Sets a counter to the value 1 and inserts the 1 in a new line.
   symbol is stored as a substitutable symbol of name symbol and the value 1

**&gt;li &ast;incr [symbol]**
:   Initiates a new List Item with a number.
    symbol is stored as a substitutable symbol of name symbol and the value of
    the number substituting *incr.

**&gt;li [optional item text in same line]**
:   Initiates a new List Item with a number.
    The item text is written to the same output line.

**&gt;/li**
:   Stops an Ordered List. Normally unnecessary.

#### Substitutions

**&gt;set symbol word [word] ...**
:   Defines a one-line symbol with value word [word] ...

**&gt;setblock symbol** and **&gt;/setblock**
:  Defines the line(s) between the two tags as the value of symbol.
   The lines can contain &gt; tags

**&gt;sub symbol**
:   The value of symbol should be substituted here.

**&gt;ignore** and **&gt;/ignore**
:   Sections of text within these tags are not written to output.
    &gt;ignore tags can be nested

**&gt;# [text]**
:   Comment line

#### Simple functions

**&gt;date [word]**
:   Insert a date stamp in the shape: YYYY-MM-DD.
    If a second word is given (period, e.g.), it is inserted right after the date stamp (no space).

**&gt;time [word]**
:   Insert a time stamp in the shape: HH:MM:SS.
    If a second word is given (period, e.g.), it is inserted right after the time stamp (no space).

**&gt;br**
:   Insert a line break

**&gt;brn**, n being an integer
:  Insert n line breaks

### Installation

The extension was made using Python v.3. As far as `mkdocs` goes, it has been
tested with v.1.0.4. It has been test installed and tested un Linux Mint 19
and Windows 10.

You are supposed to install *Python-Markdown* and, maybe, *MkDocs* yourself
independently of this product, which is defined as being dependent on *Markdown*,
i.e. *Python-Markdown*. 

You can install the *Markdown* extension by issuing this command in a console:

    pip3 install tagtomarkdown

You can also download the `tar.gz` file and issue this command in the directory where
the setup.py file is located:

    python3 setup.py install

The extension is going to write possible error messages on the console from where
it was started.

If you are using the tags for defining table cells, you should of course make the
document's *mkdocs.yml* file refer the `tables` extension too, like shown in the
figure above.

If you are in doubt which version is installed on your machine, you can issue
these commands in a console:

    1 python3
    2 >>> import tagtomarkdown
    3 >>> print(tagtomarkdown.version())
    4 tagtomarkdown v.0.4.0, 2019-04-11
    5 >>>

Line 4 is the product's indication of its version. You can update the product
by adding the `--update` flag to the `pip3 install ...` command.
