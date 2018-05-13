#!/usr/bin/env python
import sys
import os
import errno
import re
import shlex
import subprocess

#
# Tag defs
#
beginLatexTag = "BeginLatex"
endLatexTag = "EndLatex"

beginCodeBlockTag = "BeginCodeSnippet"
endCodeBlockTag = "EndCodeSnippet"

validCodeBlockTypes = ['Latex', 'CodeSnippet']

## This class is initialized with a the starting line of
## the command processing, and the block of text for
## this command invocation


class OneDocBlock():
    def __init__(self, sourceFile, id, codeblock):
        self.sourceFile = sourceFile
        self.id = id
        self.codeblock = codeblock
        self.blockType = 'Unknown'  # Something other than items in validCodeBlockTypes

    def Print(self):
        blockline = self.id
        print("=" * 80)
        print("{0} : {1}".format(self.blockType, self.sourceFile))
        for blocktext in self.codeblock:
            blockline += 1
            print("{0}  : {1}".format(blockline, blocktext))
        print("^" * 80)

    def GetCodeBlockString(self):
        blockstring = ""
        if self.blockType == 'Latex':
            for blocktext in self.codeblock:
                blockstring += "{0}\n".format(blocktext)
            pass
        elif self.blockType == 'CodeSnippet':
            # blockstring += "\\small\n"
            # blockstring += "\\begin{verbatim}\n"
            # blockstring += "\\begin{itklisting}[language=C++]\n"
            blockstring += "\\begin{minted}[baselinestretch=1,fontsize=\\footnotesize,linenos=false,bgcolor=ltgray]{c++}\n"
#blockstring += "\\begin{minted}[baselinestretch=1,fontsize=\small,linenos=false,bgcolor=ltgray]{c++}\n"
            for blocktext in self.codeblock:
                blockstring += "{0}".format(blocktext)
            blockstring += "\\end{minted}\n"
            # blockstring += "\\end{itklisting}\n"
            # blockstring += "\\end{verbatim}\n";
            # blockstring += "\\normalsize\n";
            pass
        return blockstring


def ParseOneFile(sourceFile):
    # Some embedded formatting from latex is pushing lines over the limit.
    # Create a pattern that removes most latex formatting before testing line length
    latexPattern = re.compile("\\[a-z]+")
    # Comment line begin regular expression
    commentPattern = re.compile("^ *//")
    #
    # Read each line and Parse the input file
    #
    # Get the command line args from the source file
    sf = open(sourceFile, 'r')
    INFILE = sf.readlines()
    sf.close()
    parseLine = 0
    starttagline = 0
    checkForBlankLine = False
    thisFileCommandBlocks = []
    isLatexBlock = True
    for thisline in INFILE:
        parseLine += 1

        # If the "BeginCommandLineArgs" tag is found, set the "starttagline" var and
        # initialize a few variables and arrays.
        if thisline.count(beginLatexTag) == 1:  # start of LatexCodeBlock
            isLatexBlock = True
            starttagline = parseLine
            codeBlock = []
            checkForBlankLine = True
        elif thisline.count(endLatexTag) == 1:  # end of LatexCodeBlock
            ocb = OneDocBlock(sourceFile, starttagline, codeBlock)
            ocb.blockType = 'Latex'
            thisFileCommandBlocks.append(ocb)
            starttagline = 0
        elif thisline.count(beginCodeBlockTag) == 1:  # start of CodeSnippet
            isLatexBlock = False
            starttagline = parseLine
            codeBlock = []
        elif thisline.count(endCodeBlockTag) == 1:  # end of CodeSnippet
            ocb = OneDocBlock(sourceFile, starttagline, codeBlock)
            ocb.blockType = 'CodeSnippet'
            thisFileCommandBlocks.append(ocb)
            starttagline = 0
        elif starttagline > 0:  # Inside a codeBlock
            if isLatexBlock == True:
                thisline = commentPattern.sub("",thisline)
                thisline = thisline.lstrip().rstrip()
                if checkForBlankLine:
                  if thisline != "":
                    print("{filename}:{line}: warning: Line after start of LaTeX block should be a newline -- instead got {value}".format(
                           filename=sourceFile,
                           line=parseLine,
                           value=thisline
                           )
                    )
                  checkForBlankLine = False

            if not isLatexBlock and ( len(thisline) > 80 ):
                print("{filename}:{line}:80: warning: Line length too long for LaTeX printing".format(
                       filename=sourceFile,
                       line=parseLine
                     )
                )
            codeBlock.append(thisline)
        else:  # non-codeBlock line
            pass
    return thisFileCommandBlocks


def GetPreambleString(examplefilename):
    # The following message is a warning writen on the generated .tex
    # files for preventing them from being manualy edited.
    preamble = """
% Please do NOT edit this file.
% It has been automatically generated
% by a perl script from the original cxx sources
% in the Insight/Examples directory

% Any changes should be made in the file
% {0}

The source code for this section can be found in the file\\\\
\\texttt{2}{1}{3}.
""".format(examplefilename, os.path.basename(examplefilename), '{', '}')
    return preamble

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: {0} <input file> <output file>".format(argv[0]))
        sys.exit(-1)

    inputfilename = sys.argv[1]
    outputfilename = sys.argv[2]
    print("Processing {0} into {1}  ... \n".format(inputfilename, outputfilename))

    thisCodeBlocks = ParseOneFile(inputfilename)

    try:
        path = os.path.dirname(outputfilename)
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

    outPtr = open(outputfilename, 'w')
    outPtr.write(GetPreambleString(inputfilename))
    for cb in thisCodeBlocks:
        outPtr.write(cb.GetCodeBlockString())
    outPtr.close()
