#!/usr/bin/env python3
#
# Copyright (c) 2019-2022 Christian Hauris Sorensen
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# Descriptions of packing Python:
# - https://the-hitchhikers-guide-to-packaging.readthedocs.io/en/latest/creation.html
# - https://python-markdown.github.io/extensions/api/
# - https://docs.python.org/3/distutils/sourcedist.html
#
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
#from transform import ProduceMarkdown
#import ProduceMarkdown
from datetime import datetime
import os
import sys
# ----------------------------------
# Setup up the Markdown extension
# ----------------------------------
def makeExtension(*args, **kwargs):
  #print(**kwargs)
  return TableTagExtension(**kwargs)

# Can be called from the console_scripts as defined in setup.py.
def version():
  return 'tagtomarkdown v.0.4.0, 2019-04-11'

class TableTagExtension(Extension):

  config = {}

  def __init__(self, **kwargs):
    #print(kwargs)
    #self.config = {
    #  'dummy' : ['Defaultdummy', 'Just to show the usage of a parameter']
    #}
    super(TableTagExtension, self).__init__(**kwargs)
    #super(TableTagExtension, args*, **kwargs)

  def extendMarkdown(self, md, md_globals):
    #md.register(TagConverter(md), 'tagtomarkdown', 175)
    md.registerExtension(self)
    md.preprocessors.add('tagtomarkdown', TagConverter(md), '_begin')

# -------------------------------
# Business logic from here
# -------------------------------

# ---------------------------------------------------------
class TagConverter(Preprocessor):

  def __init__(self, substitutions):
    super().__init__()
    self.substitutions = substitutions

  def run(self, lines):
    documentElement = DocumentElement()
    documentElement.handleLines(lines, self.intPutConsole, self.intPutConsole)
    #documentElement.substituteSymbols(self.intPutConsole, self.intPutConsole)
    simpleConversions = SimpleConversions()
    simpleConversions.transform(documentElement, self.intPutConsole, self.intPutConsole)
    tableConversion = TableConversion()
    tableConversion.produceSymbolicNumbers(documentElement, self.intPutConsole, self.intPutConsole)
    orderedListConversion = OrderedListConversion()
    orderedListConversion.produceSymbolicNumbers(documentElement, self.intPutConsole, self.intPutConsole)
    documentElement.substituteSymbols(self.intPutConsole, self.intPutConsole)
    tableConversion.convertTable(documentElement, self.intPutConsole, self.intPutConsole)
    orderedListConversion.convertOrderedList(documentElement, self.intPutConsole, self.intPutConsole)
    #simpleConversions = SimpleConversions()
    #simpleConversions.transform(documentElement, self.intPutConsole, self.intPutConsole)
    #documentElement.writeOutputFile(fileOutName, self.intPutConsole, self.intPutConsole)
    return documentElement.getLines() 

  # Original tester method run:
  def runProofOfConcept(self, lines):
    outLines = []
    for line in lines:
      #print('Input line: %s' % line)
      if line.startswith(">br "):
        outLines.append("<p>%s</p>"% line[4:])
      else:
        outLines.append(line)
    return outLines

  # Internal helpers:
  # Internal console writer. Can be overwritten by GUI driver.
  def intPutConsole(self, text):
    print(text)

  def getTime(self):
    now = datetime.now()
    #toDay = now.strftime('%Y%m%d')
    return now.isoformat(' ')[0:19]

# ---------------------------------------------------------
# DocumentElement class
#
# These special tags are known:
#
# >set symbol word [word] ...
#   Defines a one-line symbol with value word [word] ...
# >setblock symbol and >/setblock
#   defines the line(s) between the two tags as the value of symbol.
#   The lines can contain > tags
# >sub symbol
#   The value of symbol should be substituted here.
# >ignore and >/ignore
#   Sections of text within these tags are not written to output.
#   >ignore tags can be nested
# ># [text]
#   Comment line
#
class DocumentElement:
  # Remember the constructor (def __init__(self)) if you change those:
  outstandingSubstitutions = True
  substitutions = {}
  elements = []
  inDirName = ''
  fileName = ''
  parentDocumentElement = None
  globalSymbols=False

  # Constructor:
  def __init__(self, globalSymbols=False):
    self.outstandingSubstitutions = True
    self.substitutions = {}
    self.elements = []
    self.inDirName = ''
    self.parentDocumentElement = None
    self.globalSymbols = globalSymbols

  # Handle the file, given as a list of text lines, and store its data, ignoring
  # '>ignore' blocks and '>#' lines.
  # Convert '>set' lines an '>setblock' blocks into elements in 'substitutions'
  # instead of storing them as lines.
  def handleLines(self, lines, consPrint, statusPrint):
    ignoreMode = False
    setBlockMode = False
    multiLineSymbolValue = []
    multiLineSymbolName = ''

    for lFull in lines:
      line = self.stripNewLine(lFull)
      #consPrint('line: %s' % line)
      words = line.split()
      if ignoreMode:
        if line.startswith('>/ignore'):
          ignoreMode = False
        continue
      if setBlockMode:
        #print('setblockMode True...')
        if line.startswith('>/setblock'):
          self.storeSubstitutionValue(multiLineSymbolName, multiLineSymbolValue)
          multiLineSymbolValue = []
          multiLineSymbolName = ''
          setBlockMode = False
        else:
          multiLineSymbolValue.append(line)
      elif line.startswith('>set '):
        lineRemainder = ""
        for i in range(2, len(words)):
          if i > 2:
            lineRemainder += ' '
          lineRemainder += words[i]
        self.storeSubstitutionValue(words[1], lineRemainder)
      elif line.startswith('>setblock'):
        #print('>setblock not supported yet')
        multiLineSymbolName = words[1]
        #print('>setblock, multiLineSymbolName set to: ' + multiLineSymbolName)
        setBlockMode = True
      elif line.startswith('>#'):
        pass
      elif line.startswith('>ignore'):
        ignoreMode = True
      else:
        #consPrint('line to append: %s' % line)
        self.elements.append(line)
    #consPrint(' readFile finished')
    return

  # Substitute symbolic variables, where possible.
  def substituteSymbols(self, consPrint, statusPrint):
    self.outstandingSubstitutions = False    ;# Assume OK
    i = 0
    while i < len(self.elements):
      line = self.elements[i]
      if isinstance(line, str):
        words = line.split()
        if line.startswith('>sub'):
          substitutionString = self.lookupSymbol(words[1])
          if len(substitutionString) < 1:
            consPrint('Symbol %s not defined' % words[1])
            self.outstandingSubstitutions = True
          else:
            if isinstance(substitutionString, str):
              if len(words) > 2:
                self.elements[i] = substitutionString + words[2]
              else:
                #print('- line: %s replaced by: %s' % (self.elements[i], substitutionString))
                self.elements[i] = substitutionString
            else:
              del self.elements[i]
              for l in substitutionString:
                self.elements.insert(i, l)
                i += 1
      elif isinstance(line, DocumentElement):
        #print('DocumentElement child begin:')
        line.substituteSymbols(consPrint, statusPrint)
        #print('DocumentElement child end.')
        if line.outstandingSubstitutions == True:
          self.outstandingSubstitutions = True
      else:
        consPrint('DocumentElement element of unknown type: %s.' % type(line).__name__)
      i += 1
 
  # Return the lines that have been read and transformed
  def getLines(self):
    return self.elements

  # Produce timestamp in ISO format, down to seconds 
  def getTime(self):
    now = datetime.now()
    return now.isoformat(' ')[0:19]

  # Helper: Look up symbol in 'substitutions' in this instance and in parent
  # instances, if not found here. If not found at all, return ''.
  def lookupSymbol(self, symbol):
    #result = self.substitutions[symbol]
    result = self.substitutions.get(symbol, '')
    if len(result) > 0:
      return result
    pDE = self.parentDocumentElement
    if isinstance(pDE, DocumentElement):
      result = pDE.lookupSymbol(symbol)
      if len(result) > 0:
        return result
      else:
        return ''
    else:
      return ''

  # Helper: Strip newline char off right end of string, if present
  # Probably not necessary in the Markdown version, since the lines are stored
  # in a list of strings
  def stripNewLine(self, line):
    if len(line) > 0:
      if "\n" == line[-1]:
        #return line[0:len(line)-1]
        return line[0:-1]
    return line

  # Helper: Store symbolic name and value.
  def storeSubstitutionValue(self, symbolName, symbolValue):
    if self.globalSymbols:
      parent = self
      while parent != None:
        parentPrevious = parent 
        parent = parent.parentDocumentElement
        parentPrevious.substitutions[symbolName] = symbolValue
    else:
      self.substitutions[symbolName] = symbolValue

  # Helper: Print stored elements, for trace during development
  def printElements(self, recurseDepth):
    print('printElements() starting, %d elements, recurse depth: %d...' % (len(self.elements), recurseDepth))
    for line in self.elements:
      if isinstance(line, str):
        print('Str: %s' % line)
      elif isinstance(line, DocumentElement):
        print('DocumentElement child begin:')
        #if recurseDepth > 2:
        #  sys.exit('Recurse depth!')          ;# For development time, to be deleted later
        line.printElements(recurseDepth + 1)
        print('DocumentElement child end.')
      else:
        print('DocumentElement element of unknown type: %s.' % type(line).__name__)
    print('printElements: substitutions:')
    for key in self.substitutions.keys():
      print('Key %s: %s' % (key, self.substitutions.get(key)))

  # For development/test
  def writeElements(self, f, elements, consPrint, statusPrint):
    for line in elements:
      if isinstance(line, str):
        f.write('%s\n' % line)
      elif isinstance(line, DocumentElement):
        line.writeElements(f, line.elements, consPrint, statusPrint)
      else:
        consPrint('DocumentElement element of unknown type: %s.' % type(line).__name__)

# ---------------------------------------------------------
# SimpleConversion class
# 
# Handle some simple tags
#
# 2018-08-14 CHS: Add tags >br, >br1 and >br2.
#
# These special tags are known:
#
# >datetime [word]
#   Insert a date-time stamp in the shape: YYYY-MM-DD HH:MM:SS.
#   If a second word is given (period, e.g.), it is inserted right after the date-time stamp (no space).
#
# >date [word]
#   Insert a date stamp in the shape: YYYY-MM-DD.
#   If a second word is given (period, e.g.), it is inserted right after the date stamp (no space).
#
# >time [word]
#   Insert a time stamp in the shape: HH:MM:SS.
#   If a second word is given (period, e.g.), it is inserted right after the time stamp (no space).
#
# >br  Insert a line break
# >brn n must be an integer: Insert n line breaks
#
class SimpleConversions:

  def transform(self, documentElement, consPrint, statusPrint):
    i = 0
    while i < len(documentElement.elements):
      line = documentElement.elements[i]
      #print('line: %s' % line)
      if isinstance(line, str):
        replacementString = ''
        if line.startswith('>datetime'):
          replacementString = datetime.now().isoformat(' ')[0:19]
        elif line.startswith('>date'):
          replacementString = datetime.now().isoformat(' ')[0:10]
        elif line.startswith('>time'):
          replacementString = datetime.now().isoformat(' ')[11:19]
        #elif line.startswith('>br1'):
        #  replacementString = '<br />'
        #elif line.startswith('>br2'):
        #  replacementString = '<br /><br />'
        #elif line.startswith('>br'):
        #  replacementString = '<br />'
        elif line.startswith('>br'):
          words = line.split()   ;# V.0.4.0 addition:
          l = words[0]           ;# Support for any number of line breaks, i.e. '>brn', n being any inteeger
          if len(l) == 3:
            replacementString = '<br />'
          else:
            repetitionNoString = l[3:]
            if repetitionNoString.isnumeric():
              repetitionNo = int(repetitionNoString)
              while repetitionNo > 0:
                replacementString += '<br />'
                repetitionNo -= 1
        if len(replacementString) > 0:
          words = line.split()
          #print('- words: %s' % words)
          #if len(words) > 1:
          #  replacementString += words[1]
          wordCount = 0
          for word in words:
            if wordCount == 1:
              replacementString += word
            if wordCount > 1:
              replacementString += ' ' + word
            wordCount += 1
          #del documentElement.elements[i]
          #documentElement.elements.insert(i, replacementString)
          documentElement.elements[i] = replacementString
      elif isinstance(line, DocumentElement):
        simpleConversions = SimpleConversions()
        simpleConversions.transform(line, consPrint, statusPrint)
      else:
        consPrint('DocumentElement element of unknown type: %s.' % type(line).__name__)
      i += 1

# ---------------------------------------------------------
# TableConversion class
#
# Handle table tags and convert them into Markup table definitions. 
#
# These special tags are known:
#
# >row
#   Produces a new table row
# >row noOfColumns
#   Produces a new table row and saves the number of columns. This number is being
#   used later when a new row is defined by another >row statement. The table
#   logic will then fill in possible missing cells to finish the previous row. 
#   This parameter must be given only in the first >row statement in a given table.
# >cell [optional cell text in same line]
#   Produces a table cell. Contents can be of more lines.
# >cell *start [symbol]
#   Sets a counter to the value 1 and inserts the 1 in a new cell
#   symbol is stored as a substitutable symbol of name symbol and the value 1
# >cell *incr [symbol]
#   Increments the counter and writes its value in a new cell.
#   symbol is stored as a substitutable symbol of name symbol and the value of
#   the number substituting *incr.
# >/row [*tableno] [optional table caption text in same line]
#   End a table definition. If the table definitions ends with a blank line,
#   this tag is not necessary.
#   *tableno indicates that the caption should be preceded by the text "Table n: "
#   optional table caption: If given, a line with its text is written beneath the table. 
#
# 2018-10-17 CHS: Start making the Table Caption feature.
# 2018-05-16 CHS: Started under Eclipse/PyDev as a copy from the PyCharm version.
#                 At the same time, start implementing row-/col-span in HRML tables.
#
class TableConversion:

  # Constructor:
  def __init__(self):
    #self.memberVariable = None
    pass

  # >cell statements with the '*start' or '*incr' keyword can have a second parameter:
  # A symbolic name that should be defined with the value of the number generated by
  # the '*start' or '*incr'. Find such >cell statements, replace the keywords with
  # the proper numbers and store symbolic values.
  def produceSymbolicNumbers(self, documentElement, consPrint, statusPrint):
    tableRowCounter = 0
    i = 0
    while i < len(documentElement.elements):
      line = documentElement.elements[i]
      if isinstance(line, str):
        words = line.split()
        if line.startswith('>cell'):
          if len(words) > 1:
            command = words[1]
            if command.startswith('*'):
              if command == '*start':
                tableRowCounter = 1
                documentElement.elements[i] = '>cell %s' % tableRowCounter
              elif command == '*incr':
                tableRowCounter += 1
                documentElement.elements[i] = '>cell %s' % tableRowCounter
              if len(words) > 2:
                symbol = words[2]
                documentElement.substitutions[symbol] = '%d' % tableRowCounter
      elif isinstance(line, DocumentElement):
        #print('DocumentElement child begin:')
        self.produceSymbolicNumbers(line, consPrint, statusPrint)
        #print('DocumentElement child end.')
      else:
        consPrint('DocumentElement element of unknown type: %s.' % type(line).__name__)
      i += 1

  # Convert table related statements into Markdown statements.
  def convertTable(self, documentElement, consPrint, statusPrint):
    currColNo = 0
    noOfCols = 0
    cellContents = ''
    rowContents = ''
    caption = ''
    tableNo = 0;
    tableMode = False
    linesIn = []
    i = 0
    while i < len(documentElement.elements):
      line = documentElement.elements[i]
      #print('-line read: %s' % line)
      if isinstance(line, str):
        words = line.split()
        if tableMode:
          #print('- tableMode; deleting element: %s' % documentElement.elements[i])
          del documentElement.elements[i]
          i -= 1
          #print('tableMode: line, length: %s, %d' % (line, line.__len__()))
          if len(line.strip()) < 1 or line.startswith('>/row'):
            #print('tableMode, len(line) == 0...')
            #statusPrint('End of table...')
            savedContents = self.closeCell(cellContents)
            cellContents = ''
            if len(savedContents) > 0:
              #linesIn.append(savedContents)
              rowContents += savedContents
            if noOfCols > 0:
              #print ('noOfRows: %d...' % (noOfRows))
              while currColNo < noOfCols:
                #print ('currColNo, noOfCols: %d, %d...' % (currColNo, noOfCols))
                #linesIn.append('&nbsp;|')
                rowContents += '&nbsp;|'
                currColNo += 1
            if len(rowContents) > 0:
              linesIn.append(rowContents)
              linesIn.append('')
              rowContents = ''
            # if added 01-10-17 by CHS: Make support for a table caption
            if line.startswith('>/row'):
              caption = ''
              if len(words) > 1:
                for j in range(1, len(words)):
                  if j == 1:
                    if words[j].strip() == '*tableno':
                      tableNo += 1
                    else:
                      caption += words[j].strip()
                  else:
                    caption += ' '
                    caption += words[j].strip()
                #linesIn.append(' ')
                if tableNo > 0:
                  linesIn.append('**Table %d: %s**' % (tableNo, caption))
                else:
                  linesIn.append('**%s**' % caption)
            for line in linesIn:
              #print('- line in linesIn: %s' % line)
              i += 1
              documentElement.elements.insert(i, line)
            currColNo = 0
            tableMode = False
            #noOfCols = 0
            linesIn = []
          elif line.startswith('>row'):
            savedContents = self.closeCell(cellContents)
            cellContents = ''
            if len(savedContents) > 0:
              #linesIn.append(savedContents)
              rowContents += savedContents
            if noOfCols > 0:
              while currColNo < noOfCols:
                #linesIn.append('&nbsp;|')
                rowContents += '&nbsp;|'
                currColNo += 1
            linesIn.append(rowContents)
            #noOfCols = 0
            #linesIn.append('')
            rowContents = '|'
            currColNo = 0
            #linesIn.append('\n|')
          elif line.startswith('>cell'):
            savedContents = self.closeCell(cellContents)
            cellContents = ''
            if len(savedContents) > 0:
              #linesIn.append(savedContents)
              rowContents += savedContents

            # Attempt to implement row-/col-span, BEGIN:
            # Not finished, no support for spans in MarkDown.
            #words = line.split()
            #command = words[1]
            #if command.startswith('*'):
            #  if command == '*rowspan':
            #    if len(words) > 2:
            #      spanNo = words[2]
            #  elif command == '*colspan':
            #    if len(words) > 2:
            #      spanNo = words[2]
            # Attempt to implement row-/col-span, END.

            lineRemainder = ''
            if len(words) > 1:
              for j in range(1, len(words)):
                if j > 1:
                  lineRemainder += ' '
                lineRemainder += words[j].strip()
              cellContents = lineRemainder
            else:
              cellContents = '&nbsp;'
            currColNo += 1
          else:
            if len(cellContents) > 0:
              if cellContents == '&nbsp;':
                cellContents = ''
              else:
                cellContents += ' '
            cellContents += line.strip()
            #print('inside >cell, cellContents: %s' % cellContents)

        # Not tableMode:
        else:
          if line.startswith('>row'):
            #print('- Not tableMode; deleting element: %s' % documentElement.elements[i])
            del documentElement.elements[i]
            i -= 1
            cellContents = ''
            tableMode = True
            if len(words) > 1:
              noOfCols = int(words[1])
            else:
              noOfCols = 0
            currColNo = 0
            #linesIn.append('|')
            rowContents = '|'
          #else:
          #  #print('Plain line: %s' % line)
          #  linesIn.append(line)

      elif isinstance(line, DocumentElement):
        #print('DocumentElement child begin:')
        tableConversion = TableConversion()
        tableConversion.convertTable(line, consPrint, statusPrint)
        #print('DocumentElement child end.')
      else:
        consPrint('TableConversion: DocumentElement element of unknown type: %s.' % type(line).__name__)
      i += 1

  # -------------------------
  # Internal helpers:
  # -------------------------
  def closeCell(self, cellContents):
    #print('closeCell, cellContents: %s' % cellContents)
    if len(cellContents) == 0:
      return ''
    return cellContents + '|'
# ---------------------------------------------------------
# OrderedListConversion class
#
# Handle Ordered List tags and convert them into Markup Ordered list definitions.
# A symbolic name can be assigned to a list entry and then the list item number
# can be referred to symbolically from other places in the text. 
#
# These special tags are known:
#
# >li *start [symbol]
#   Sets a counter to the value 1 and inserts the 1 in a new line.
#   symbol is stored as a substitutable symbol of name symbol and the value 1
# >li *incr [symbol]
#   Initiates a new List Item with a number.
#   symbol is stored as a substitutable symbol of name symbol and the value of
#   the number substituting *incr.
# >li [optional item text in same line]
#   Initiates a new List Item with a number
#   The item text is written to the same output line.
# >/li
#   Stops an Ordered List. Normally unnecessary.
#
class OrderedListConversion:

  # Constructor:
  def __init__(self):
    #self.memberVariable = None
    pass

  # >li statements with the '*start' or '*incr' keyword can have a second parameter:
  # A symbolic name that should be defined with the value of the number generated by
  # the '*start' or '*incr'. Find such >li statements, replace the keywords with
  # the proper numbers and store symbolic values.
  def produceSymbolicNumbers(self, documentElement: DocumentElement, consPrint, statusPrint):
    listItemCounter = 0
    i = 0
    insideListItem = False
    while i < len(documentElement.elements):
      line = documentElement.elements[i]
      if isinstance(line, str):
        words = line.split()
        if line.startswith('>li'):
          insideListItem = True
          if len(words) > 1:
            command = words[1]
            if command.startswith('*'):
              if command == '*start':
                listItemCounter = 1
                documentElement.elements[i] = '%s. ' % listItemCounter
              elif command == '*incr':
                listItemCounter += 1
                documentElement.elements[i] = '%s. ' % listItemCounter
              if len(words) > 2:
                symbol = words[2]
                documentElement.substitutions[symbol] = '%d' % listItemCounter
            else:
              listItemCounter += 1    ;# In-line text on the >li line:
              documentElement.elements[i] = '%s. %s' % (listItemCounter, self.fetchRemainder(words))
          else:
            listItemCounter += 1
            documentElement.elements[i] = '%s. ' % listItemCounter
            #lineRemainder = ''
            #if len(words) > 1:
            #  documentElement.elements[i] += '%s' % self.fetchRemainder(words)
        elif line.startswith('>/li'):
          insideListItem = False
          del(documentElement.elements[i])
          i -= 1
        else:
          if insideListItem:
            documentElement.elements[i - 1] += line
            del(documentElement.elements[i])
            i -= 1
            insideListItem = False
      elif isinstance(line, DocumentElement):
        #print('DocumentElement child begin:')
        self.produceSymbolicNumbers(line, consPrint, statusPrint)
        #print('DocumentElement child end.')
      else:
        consPrint('OrderedListConverision: DocumentElement element of unknown type: %s.' % type(line).__name__)
      i += 1

  # Convert Ordered List related statements into Markdown statements.
  def convertOrderedList(self, documentElement: DocumentElement, consPrint, statusPrint):
    #currColNo = 0
    #noOfCols = 0
    #itemContents = ''
    #rowContents = ''
    orderedListMode = False
    linesIn = []
    i = 0
    while i < len(documentElement.elements):
      line = documentElement.elements[i]
      #print('-line read: %s' % line)
      if isinstance(line, str):
        words = line.split()
        if line.startswith('>li'):
          linesIn.append(self.fetchRemainder(words))
        elif line.startswith('>/li'):
          pass
        else:
          linesIn.append(line)
      elif isinstance(line, DocumentElement):
        #print('DocumentElement child begin:')
        orderedListConversion = OrderedListConversion()
        orderedListConversion.convertOrderedList(line, consPrint, statusPrint)
        #print('DocumentElement child end.')
      else:
        consPrint('OrderedListConversion: DocumentElement element of unknown type: %s.' % type(line).__name__)
      i += 1

  # Meant to pick words from a line except the first ('>li') part
  # The line is given inthe shape of a list with its words in it, so we skip the first word.
  def fetchRemainder(self, words):
    lineRemainder = ''
    if len(words) > 1:
      for j in range(1, len(words)):
        if j > 1:
          lineRemainder += ' '
        lineRemainder += words[j].strip()
    return lineRemainder
# ---------------------------------------------------------
