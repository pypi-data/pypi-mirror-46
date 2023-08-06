
**New in 1.4.2:** Improved epub support.

**New in 1.4.0:** Support for references in bracketed spans.

[more...](#whats-new)


pandoc-tablenos 1.4.2
=====================

*pandoc-tablenos* is a [pandoc] filter for numbering tables and table references when converting markdown documents to other formats.

Demonstration: Processing [demo3.md] with `pandoc --filter pandoc-tablenos` gives numbered tables and references in [pdf][pdf3], [tex][tex3], [html][html3], [epub][epub3], [docx][docx3] and other formats (including beamer slideshows).

This version of pandoc-tablenos was tested using pandoc 1.15.2 - 2.7.2<sup>[1](#footnote1)</sup>.  It works under linux, Mac OS X and Windows.  I am pleased to receive bug reports and feature requests on the project's [Issues tracker].  If you find pandoc-tablenos useful, then please kindly give it a star [on GitHub].

See also: [pandoc-fignos], [pandoc-eqnos]

[pandoc]: http://pandoc.org/
[Issues tracker]: https://github.com/tomduck/pandoc-tablenos/issues
[on GitHub]: https://github.com/tomduck/pandoc-tablenos
[pandoc-fignos]: https://github.com/tomduck/pandoc-fignos
[pandoc-eqnos]: https://github.com/tomduck/pandoc-eqnos


Contents
--------

 1. [Usage](#usage)
 2. [Markdown Syntax](#markdown-syntax)
 3. [Customization](#customization)
 4. [Details](#details)
 5. [Installation](#installation)
 6. [Getting Help](#getting-help)
 7. [What's New](#whats-new)


Usage
-----

Use the following option with pandoc:

    --filter pandoc-tablenos

Note that any use of `--filter pandoc-citeproc` or `--bibliography=FILE` should come *after* the pandoc-tablenos filter call.


Markdown Syntax
---------------

The markdown syntax extension used by pandoc-tablenos was worked out in [pandoc Issue #813] -- see [this post] by [@scaramouche1].

To mark a table for numbering, add an id to its attributes:

    A B
    - -
    0 1

    Table: Caption. {#tbl:id}

The prefix `#tbl:` is required. `id` should be replaced with a unique identifier composed of letters, numbers, dashes and underscores.  If `id` is omitted then the figure will be numbered but unreferenceable.

To reference the table, use

    @tbl:id

or

    {@tbl:id}

Curly braces around a reference are stripped from the output.

Demonstration: Processing [demo.md] with `pandoc --filter pandoc-tablenos` gives numbered tables and references in [pdf], [tex], [html], [epub], [docx] and other formats.

[pandoc Issue #813]: https://github.com/jgm/pandoc/issues/813
[this post]: https://github.com/jgm/pandoc/issues/813#issuecomment-70423503
[@scaramouche1]: https://github.com/scaramouche1
[demo.md]: https://raw.githubusercontent.com/tomduck/pandoc-tablenos/master/demos/demo.md
[pdf]: https://raw.githack.com/tomduck/pandoc-tablenos/master/demos/out/demo.pdf
[tex]: https://raw.githack.com/tomduck/pandoc-tablenos/master/demos/out/demo.tex
[html]: https://raw.githack.com/tomduck/pandoc-tablenos/master/demos/out/demo.html
[epub]: https://raw.githack.com/tomduck/pandoc-tablenos/master/demos/out/demo.epub
[docx]: https://raw.githack.com/tomduck/pandoc-tablenos/master/demos/out/demo.docx

#### Clever References ####

Writing markdown like

    See table @tbl:id.

seems a bit redundant.  Pandoc-tablenos supports "clever referencing" via single-character modifiers in front of a reference.  You can write

     See +@tbl:id.

to have the reference name (i.e., "table") automatically generated.  The above form is used mid-sentence.  At the beginning of a sentence, use

     *@tbl:id

instead.  If clever referencing is enabled by default (see [Customization](#customization), below), then you can disable it for a given reference using<sup>[2](#footnote2)</sup>

    !@tbl:id

Demonstration: Processing [demo2.md] with `pandoc --filter pandoc-tablenos` gives numbered tables and references in [pdf][pdf2], [tex][tex2], [html][html2], [epub][epub2], [docx][docx2] and other formats.

Note: If you use `*tbl:id` and emphasis (e.g., `*italics*`) in the same sentence, then you must backslash escape the `*` in the clever reference; e.g., `\*tbl:id`.

[demo2.md]: https://raw.githubusercontent.com/tomduck/pandoc-tablenos/master/demos/demo2.md
[pdf2]: https://raw.githack.com/tomduck/pandoc-tablenos/master/demos/out/demo2.pdf
[tex2]: https://raw.githack.com/tomduck/pandoc-tablenos/master/demos/out/demo2.tex
[html2]: https://raw.githack.com/tomduck/pandoc-tablenos/master/demos/out/demo2.html
[epub2]: https://raw.githack.com/tomduck/pandoc-tablenos/master/demos/out/demo2.epub
[docx2]: https://github.com/tomduck/pandoc-tablenos/blob/master/demos/out/demo2.docx


#### Tagged Tables ####

You may optionally override the table number by placing a tag in a table's attributes block as follows:

    A B
    - -
    0 1

    Table: Caption. {#tbl:id tag="B.1"}

The tag may be arbitrary text, or an inline equation such as `$\text{B.1}'$`.  Mixtures of the two are not currently supported.


Customization
-------------

Pandoc-tablenos may be customized by setting variables in the [metadata block] or on the command line (using `-M KEY=VAL`).  The following variables are supported:

  * `tablenos-capitalise` or `xnos-capitalise` - Capitalizes the
    names of "+" references (e.g., change from "table" to "Table");

  * `tablenos-caption-name` - Sets the name at the beginning of a
    caption (e.g., change it from "Table to "Tab.");

  * `tablenos-cleveref` or just `cleveref` - Set to `True` to assume
    "+" clever references by default;

  * `tablenos-plus-name` - Sets the name of a "+" reference 
    (e.g., change it from "table" to "tab."); and

  * `tablenos-star-name` - Sets the name of a "*" reference 
    (e.g., change it from "Table" to "Tab.").

  * `xnos-number-sections` - Set to `True` so that tables are
    numbered per section (i.e. Table 1.1, 1.2, etc in Section 1, and
    Table 2.1, 2.2, etc in Section 2).  For html and LaTeX/pdf this
    feature works in conjunction with pandoc's `--section-numbers`
    command-line flag.  See
    [Table Numbering by Section](#table-numbering-by-section),
    below.

    This feature is only presently enabled for html, LaTeX/pdf, and
    docx.

[metadata block]: http://pandoc.org/README.html#extension-yaml_metadata_block

Demonstration: Processing [demo3.md] with `pandoc --filter pandoc-tablenos` gives numbered tables and references in [pdf][pdf3], [tex][tex3], [html][html3], [epub][epub3], [docx][docx3] and other formats.

[demo3.md]: https://raw.githubusercontent.com/tomduck/pandoc-tablenos/master/demos/demo3.md
[pdf3]: https://raw.githack.com/tomduck/pandoc-tablenos/master/demos/out/demo3.pdf
[tex3]: https://raw.githack.com/tomduck/pandoc-tablenos/master/demos/out/demo3.tex
[html3]: https://raw.githack.com/tomduck/pandoc-tablenos/master/demos/out/demo3.html
[epub3]: https://raw.githack.com/tomduck/pandoc-tablenos/master/demos/out/demo3.epub
[docx3]: https://raw.githack.com/tomduck/pandoc-tablenos/master/demos/out/demo3.docx


#### Table Numbering by Section ####

Pandoc's `--number-sections` option enables section numbering for LaTeX/pdf and html output.  For docx, use [custom styles](https://pandoc.org/MANUAL.html#custom-styles) instead.  Table numbering by section (e.g., "Table 2.1") can then be obtained as follows:

 1) **html and docx:** Add `xnos-number-sections: True` to your YAML
    metadata or use the `-M xnos-number-sections=True` option with
    pandoc.  This variable is ignored for other output formats.

 2) **LaTeX/pdf:** Add 
    `header-includes: \numberwithin{table}{section}` to your YAML
    metadata.  If you need multiple header includes, then add
    something like this:

    ~~~
    header-includes:
      - \numberwithin{figure}{section}
      - \numberwithin{equation}{section}
      - \numberwithin{table}{section}
    ~~~

    Alternatively, write your header includes into FILE,
    and use the `--include-in-header=FILE` option with pandoc.

    If you set either `--top-level-division=part` or
    `--top-level-division=chapter` then these header includes can be
    dropped.

    LaTeX header-includes are ignored for html output.


#### Latex/PDF Specializations ####

To make the table caption label bold, add `\usepackage[labelfont=bf]{caption}` to the `header-includes` field of your document's YAML metadata.  See the [LaTeX caption package] documentation for additional features.

[LaTeX caption package]: https://www.ctan.org/pkg/caption


Details
-------

TeX/pdf:

  * The `\label` and `\ref` macros are used for table labels and
    references;
  * `\figurename` is set for the caption name;
  * Tags are supported by temporarily redefining `\thetable` around 
    a table; and
  * The clever referencing macros `\cref` and `\Cref` are used
    if they are available (i.e. included in your LaTeX template via
    `\usepackage{cleveref}`), otherwise they are faked.  Set the 
    meta variable `xnos-cleveref-fake` to `False` to disable cleveref
    faking.
  * The clever reference names are set using `\crefformat` and
    `\Crefformat`.  For this reason the cleveref package's
    `capitalise` parameter has no effect.  Use the
    `fignos-capitalise` meta variable instead.

Other formats:

  * Links to figures use html's and docx's native capabilities; and

  * The numbers, caption name, and (clever) references are hard-coded
    into the output.


Installation
------------

Pandoc-tablenos requires [python], a programming language that comes pre-installed on linux and Mac OS X, and which is easily installed on Windows.  Either python 2.7 or 3.x will do.

[python]: https://www.python.org/


#### Standard installation ####

Install pandoc-tablenos as root using the shell command

    pip install pandoc-tablenos 

To upgrade to the most recent release, use

    pip install --upgrade pandoc-tablenos 

Pip is a program that downloads and installs modules from the Python Package Index, [PyPI].  It should come installed with your python distribution.

Note that on some systems for `python3` you may need to use `pip3` instead.

[PyPI]: https://pypi.python.org/pypi


#### Troubleshooting ####

If you are prompted to upgrade `pip`, then do so.  Installation errors may occur with older versions.   The command you need to execute (as root) is

    python -m pip install --upgrade pip

One user reported that they had to manually upgrade the `six` and `setuptools` modules:

    pip install --upgrade six
    pip install pandoc-tablenos

This should not normally be necessary.

You may test the installation as a regular user using the shell command

    which pandoc-tablenos

This will tell you where pandoc-tablenos is installed.  If it is not found, then please submit a report to our [Issues tracker].

To determine which version of pandoc-tablenos you have installed, use

    pip show pandoc-tablenos

As of pandoc-tablenos 1.4.1 you can also use

    pandoc-tablenos --version

Please be sure you have the latest version installed before reporting a bug on our [Issues tracker].


#### Installing on linux ####

If you are running linux, then pip may be packaged separately from python.  On Debian-based systems (including Ubuntu), you can install pip as root using

    apt-get update
    apt-get install python-pip

During the install you may be asked to run

    easy_install -U setuptools

owing to the ancient version of setuptools that Debian provides.  The command should be executed as root.  You may now follow the [standard installation] procedure given above.

[standard installation]: #standard-installation


#### Installing on Mac OS X ####

To install as root on Mac OS X, you will need to use the `sudo` command.  For example:

    sudo pip install pandoc-tablenos

Troubleshooting should be done as a regular user (i.e., without using `sudo`).


#### Installing on Windows ####

It is easy to install python on Windows.  First, [download] the latest release.  Run the installer and complete the following steps:

 1. Install Python pane: Check "Add Python 3.5 to path" then
    click "Customize installation".

 2. Optional Features pane: Click "Next".

 3. Advanced Options pane: Optionally check "Install for all
    users" and customize the install location, then click "Install".

Once python is installed, start the "Command Prompt" program.  Depending on where you installed python, you may need elevate your privileges by right-clicking the "Command Prompt" program and selecting "Run as administrator".  You may now follow the [standard installation] procedure given above.  Be sure to close the Command Prompt program when you have finished.

[download]: https://www.python.org/downloads/windows/


Getting Help
------------

If you have any difficulties with pandoc-tablenos, or would like to see a new feature, then please submit a report to our [Issues tracker].


What's New
----------

**New in 1.4.2:** Improved epub support.

**New in 1.4.1:** Working links in epub output.

**New in 1.4.0:** Support for references in bracketed spans.

**New in 1.3.2:** Support for docx table numbering by section.

**New in 1.3.0:** Boolean metadata values must now be one of `true`, `True` `TRUE`, `false`, `False`, or `FALSE`.  This is following a [change of behaviour](https://pandoc.org/releases.html#pandoc-2.2.2-16-july-2018) with pandoc 2.2.2.

**New in 1.2.0:** Added `fignos-capitalise` meta variable to capitalise clever references (e.g., change "fig." to "Fig.").


----

**Footnotes**

<a name="footnote1">1</a>: Pandoc 2.4 [broke](https://github.com/jgm/pandoc/issues/5099) how references are parsed, and so is not supported.

<a name="footnote2">2</a>: The disabling modifier "!" is used instead of "-" because [pandoc unnecessarily drops minus signs] in front of references.

[pandoc unnecessarily drops minus signs]: https://github.com/jgm/pandoc/issues/2901
