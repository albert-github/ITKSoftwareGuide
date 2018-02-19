ITK Software Guide
==================

[![Build Status](https://circleci.com/gh/InsightSoftwareConsortium/ITKSoftwareGuide.svg?style=shield)](https://circleci.com/gh/InsightSoftwareConsortium/ITKSoftwareGuide)

This [ITK Software Guide] is the handbook for developing software with ITK.

It is divided into two companion books.

The [first book] covers
building and installation, general architecture and design, as well as the
process of contributing in the ITK community.

The [second book] covers
detailed design and functionality for reading and writing images, filtering,
registration, segmentation, and performing statistical analysis.

This repository contains the source code for the Software Guide.

How to Contribute to the ITK Software Guide
===========================================

Contributions are welcome and appreciated!

Contribution Process Overview
-----------------------------

The following commands illustrate patch submission to [GitHub]:

```sh
   $ git clone https://github.com/InsightSoftwareConsortium/ITKSoftwareGuide.git
   $ cd ITKSoftwareGuide
   $ ./Utilities/SetupForDevelopment.sh
   $ git checkout -b my-topic
   # make changes to local file(s)
   $ git add -- changedFileName
   $ git commit
   $ git review-push
```

Contribution Details
--------------------

For more detailed instructions, see the [CONTRIBUTING.md](CONTRIBUTING.md) file.

Building with Docker
--------------------

All the dependencies described belowe are available pre-installed in a [Docker]
image. This is the easiest way to build and contribute to The Software
Guide.

  1. Download and [install Docker](http://docs.docker.com/installation/).
  2. From a shell, run
```sh
docker run --name software-guide -p 8888:8888 insighttoolkit/itksoftwareguide-edit:latest
```
  3. Open a Console.
  4. To setup the repository for develop and build the project, run:
```sh
ssh-keygen
cat ~/.ssh/id_rsa.pub
# Paste this value into https://github.com/settings/keys cd /ITKSoftwareGuide ./Utilities/SetupForDevelopment.sh
cd /ITKSoftwareGuide-build/ITKSoftwareGuide-build
ninja
```
  6. To view the built PDF's, navigate to `bin/ITKSoftwareGuide/SoftwareGuide/Latex/`,
     click on the PDF, then the *download* button.
  7. Contribute as described in [CONTRIBUTING.md](CONTRIBUTING.md).
  8. To restart the container, run `docker start software-guide`.

Build Overview
--------------

A combination of [CMake]
`Superbuild` infrastructure, [Python] extraction scripts, and [LaTeX]
formatting are required to render the entire ITK Software Guide.

`CMakeLists.txt` files are placed in the directories
involved on the build process. As any other CMake-managed process, the results
of the build process are put in a binary tree corresponding to the source tree.

The following dependencies are required to build ITK Software Guide on Linux or
Windows platforms:

  * [Git]
  * [Python]
  * [ImageMagick]: Windows installer can be found
    [here](https://www.imagemagick.org/script/download.php#windows).
  * [LaTeX] and [BibTeX]. See the preamble of the
    [`./SoftwareGuide/Latex/00-Preamble-Common.tex`] file for the full list of
    required LaTeX packages. Among these packages, the [Minted] package for
    syntax highlighting in its turn depends on a Python package [Pygments].
    Instructions for installing [Minted] and [Pygments] packages on Windows are
    available [here](https://minted.googlecode.com/files/minted.pdf).
  * [dvips], [ps2pdf]. While on Linux platforms these tools are usually
    included with most distributions, on Windows platforms they are usually
    included in [MikTex] Latex distribution.

ITK Software Guide is generated with Latex by using input from a variety of
source code files and images:

  1. LaTeX files found in [`./SoftwareGuide/Latex`].
  2. JPEG, PNG and EPS files in [`./SoftwareGuide/Art`].
  3. PNG files generated as the result of compiling and running the examples
     included in the ITK source code.
  3. ITK examples source code `.cxx` files where the comments delimited with
     `BeginLaTeX`, `EndLaTeX` and `BeginCodeSnippet`, `EndCodeSnippet` have
     been written specifically to be included in the ITK Software Guide; the
     regular LaTeX files in [`./SoftwareGuide/Latex`] include the LaTeX files
     generated from the ITK examples source code.

Following is a brief description of the build process:

  1. The source code of `ITK` is downloaded and built (including ITK
     examples) in the binary output directory.
  2. JPEG and PNG files in the [`./SoftwareGuide/Art`] directory are converted
     to EPS using [ImageMagick] tools; the resulting EPS files are saved in the
     `Art` directory in the binary output directory.
  3. PNG files are generated by running ITK examples and converted to EPS using
     [ImageMagick]; the resulting EPS files are saved in `Art/Generated`
     directory of the binary output directory.
  4. A Python script
     [`./SoftwareGuide/Examples/ParseCxxExamples.py`](https://github.com/InsightSoftwareConsortium/ITKSoftwareGuide/blob/master/SoftwareGuide/Examples/ParseCxxExamples.py)
     is invoked to extract the comments in the ITK examples source file
     delimited with `BeginLaTeX`, `EndLaTeX` and `BeginCodeSnippet`,
     `EndCodeSnippet` and generate LaTeX files which are copied into the
     `Examples` subdirectory of the binary output directory.
  5. The top-level LaTeX file
     [`./SoftwareGuide/LaTeX/ITKSoftwareGuide-Book1.tex`](https://github.com/InsightSoftwareConsortium/ITKSoftwareGuide/blob/master/SoftwareGuide/Latex/ITKSoftwareGuide-Book1.tex)
     is compiled with a series of calls to `latex`, `bibtex`, `latex`,
     `makeindex`,`dvips`, and `ps2pdf` to generate the PDF file.

Configuring and Building with CMake
-----------------------------------

Following is the description how to configure and build ITK Software Guide using
[CMake]:

  1. Run cmake-gui and specify input and binary output directories.
     Alternatively, create the binary output directory and run
```sh
   $ ccmake source_dir
```
where source_dir is the full path of the `ITKSoftwareGuide` directory.
  2. Configure and generate the project for the target platform.
  3. Build `SuperBuild\_ITKSoftwareGuide` project as appropriate for the target
     platform.

Troubleshooting
---------------

  1. Build process will fail if [CMake] is unable to locate any of the
     dependencies. In this case a close examination of the error messages might
     provide a clue as to which dependency is failing.

  2. Frustrated by the build taking a long time to complete
     ... no solution here :blush:.




[`./SoftwareGuide/Art`]: https://github.com/InsightSoftwareConsortium/ITKSoftwareGuide/tree/master/SoftwareGuide/Art
[`./SoftwareGuide/Latex`]: https://github.com/InsightSoftwareConsortium/ITKSoftwareGuide/tree/master/SoftwareGuide/Latex
[`./SoftwareGuide/Latex/00-Preamble-Common.tex`]: https://github.com/InsightSoftwareConsortium/ITKSoftwareGuide/blob/master/SoftwareGuide/Latex/00-Preamble-Common.tex

[ITK Software Guide]: https://itk.org/ITKSoftwareGuide/html/
[first book]: https://itk.org/ITKSoftwareGuide/html/Book1/ITKSoftwareGuide-Book1.html
[second book]: https://itk.org/ITKSoftwareGuide/html/Book2/ITKSoftwareGuide-Book2.html
[CMake]: https://cmake.org/
[GitHub]: https://github.com/

[BibTeX]: http://www.bibtex.org/
[Docker]: https://www.docker.com/
[dvips]: http://tug.org/texinfohtml/dvips.html
[Git]: https://git-scm.com/
[ImageMagick]: https://www.imagemagick.org
[LaTeX]: https://www.latex-project.org//
[Minted]: https://ctan.org/pkg/minted?lang=en
[MikTex]: https://miktex.org/
[ps2pdf]: https://www.ps2pdf.com/
[Pygments]: http://pygments.org/
[Python]: https://www.python.org/
