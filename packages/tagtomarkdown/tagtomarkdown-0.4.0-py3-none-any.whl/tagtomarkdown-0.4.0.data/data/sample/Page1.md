## Test tagtomarkdown tags in markdown file

Just some text, until further.
>br and a home made line break
and more text.
>br6 Try out v.0.4 addition:
Break a given number of lines.

### Try tables

|No|Text|Remarks|
|:-:|---|---|
>row 3
>cell *start
>cell Here is the first row. You can write as many
lines here as you want.
>row
>cell *incr rowNoReference
>cell And the second
>cell And a bit of a comment here.
>row
>cell *incr
>cell and that's it.
>/row *tableno Some caption text for the table

### Try ordered lists

>li *start
Number one and with quite some text, so that we can show
that there can be more input lines here. But note that when there is a
keyword after the >li, there should be no more text in that line
>li *incr itemNoReference
Next item.
>li
Note no keyword (*incr) here.

># And that's it for the ordered list. This line is a comment and will not appear in the Markdown text.

## Test references to table row numbers and ordered list numbers

Here, we can refer symbolically row
>sub rowNoReference
in the table above and the ordered list item
>sub itemNoReference .

## A few other services

Last update:
>datetime .

>ignore
This paragraph should be ignored
and therefore not appear in the resulting HTML.
>/ignore
