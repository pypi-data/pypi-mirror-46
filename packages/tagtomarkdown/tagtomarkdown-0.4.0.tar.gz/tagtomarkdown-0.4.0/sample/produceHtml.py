#!/usr/bin/env python
#
import markdown
import codecs
from markdown.extensions.tables import TableExtension 
from markdown.extensions.toc import TocExtension
#from tagtomarkdown import TableTagExtension
from ../tagtomarkdown import TableTagExtension
import sys
import os
#
def produceHtml(inFileName, outFileName):
  #print('produceHtml, inFileName: %s' % inFileName)
  #print('produceHtml, outFileName: %s' % outFileName)
  input_file = codecs.open(inFileName, mode="r", encoding="utf-8")
  text = input_file.read()
  #html = markdown.markdown(text, extensions=[TableExtension(), TocExtension(), TableTagExtension()], output_format="html5")
  html = markdown.markdown(text, extensions=['tables', 'toc', 'tagtomarkdown'], output_format="html5")
  output_file = codecs.open(outFileName, mode="w", encoding="utf-8")
  output_file.write('<html xmlns="http://www.w3.org/1999/xhtml">\n')
  output_file.write("<head>\n")
  output_file.write('  <meta content="text/html; charset=utf-8" http-equiv="content-type" />\n')
  output_file.write("  <title>Test the Python-Markdown extension tagtomarkdown</title>\n")
  output_file.write("</head>\n")
  output_file.write("<style> td, th {border: 1px solid black; padding:5px;}")
  output_file.write(" table {border-collapse: collapse;}</style>\n")

  output_file.write(html)
  output_file.close()

if __name__ == '__main__':
  cwd = os.getcwd()
  IN_FILE = '%s/doc/docs/Page1.md' % cwd
  OUT_FILE = '%s/Page1.html' % cwd
  print("produceHtml started input file: %s..." % IN_FILE)
  produceHtml(IN_FILE, OUT_FILE)
  print("produceHtml stops,  output file: %s." % OUT_FILE)
