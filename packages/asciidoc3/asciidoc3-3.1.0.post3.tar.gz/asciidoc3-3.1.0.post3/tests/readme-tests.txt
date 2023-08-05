= AsciiDoc3 Tests README

To test the features of AsciiDoc3, please use the information given in the 'userguide',
the 'quickstart', and the files in directory ../doc of the distribution.


[NOTE]
You may safely remove directory 'tests' (and subfolders - if any -) and the entire data
they contain. This will *not* have any effect on the execution of AsciiDoc3! 

Most users are happy to see AsciiDoc3 work in the expected way, and so it does! If you like 
to see even more examples of the power of AsciiDoc3, try this:

-------------------
cd ~/asciidoc3/tests

python3 testasciidoc3.py --force update
-------------------

You'll see something like this on stdout:

-------------------
WRITING: data/testcases-html4.html
WRITING: data/testcases-xhtml11.html
WRITING: data/testcases-docbook.xml
WRITING: data/testcases-html5.html
WRITING: data/filters-test-html4.html
 ...
WRITING: data/rcs-id-marker-test-docbook.xml
WRITING: data/rcs-id-marker-test-html5.html
WRITING: data/deprecated-quotes-html4.html
WRITING: data/deprecated-quotes-xhtml11.html
WRITING: data/deprecated-quotes-docbook.xml
WRITING: data/deprecated-quotes-html5.html
-------------------

Change to ./data and check out the multi-faceted 170 files computed by AsciiDoc3.
They underline the capabilities of the program. 

Beside the new files in ./data there are a few generated md5/png in ../images.


== Usage

If you like to develop and test your own asciidoc3.py (or the conf-files, respectively), you can test the output
with the help of 'testasciidoc3.py', too: 

--------------
python3 testasciidoc3.py
--------------

gives you the 'usage'

----------------
Usage: testasciidoc3.py [OPTIONS] COMMAND
Run AsciiDoc3 conformance tests specified in configuration FILE.

Commands:
  list                          List tests
  run [NUMBER] [BACKEND]        Execute tests
  update [NUMBER] [BACKEND]     Regenerate and update test data

Options:
  -f, --conf-file=CONF_FILE
        Use configuration file CONF_FILE (default configuration file is
        testasciidoc3.conf in testasciidoc3.py directory)
  --force
        Update all test data overwriting existing data
----------------

== List

So we have:

----------------
python3 testasciidoc3.py list

1: Test cases
2: Filters
3: Tables
4: Source highlighter
5: Example article
6: Example article with embedded images (data URIs)
7: Example article with included docinfo file.
8: Example book
9: Example multi-part book
10: Man page
11: Example slideshow
12: ASCIIMathML
13: LaTeXMathML
14: LaTeX Math
15: LaTeX Filter
16: UTF-8 Examples
17: Additional Open Block and Paragraph styles
18: English language file (article)
19: English language file (book)
20: English language file (manpage)
21: Russian language file (article)
22: Russian language file (book)
23: Russian language file (manpage)
24: French language file (article)
25: French language file (book)
26: French language file (manpage)
27: German language file (article)
28: German language file (book)
29: German language file (manpage)
30: Hungarian language file (article)
31: Hungarian language file (book)
32: Hungarian language file (manpage)
33: Spanish language file (article)
34: Spanish language file (book)
35: Spanish language file (manpage)
36: Brazilian Portuguese language file (article)
37: Brazilian Portuguese language file (book)
38: Brazilian Portuguese language file (manpage)
39: Ukrainian language file (article)
40: Ukrainian language file (book)
41: Ukrainian language file (manpage)
42: Dutch language file (article)
43: Dutch language file (book)
44: Dutch language file (manpage)
45: Italian language file (article)
46: Italian language file (book)
47: Italian language file (manpage)
48: Czech language file (article)
49: Czech language file (book)
50: Czech language file (manpage)
51: Romanian language file (article)
52: Romanian language file (book)
53: Romanian language file (manpage)
54: RCS $Id$ marker test
55: # UTF-8 BOM test
----------------------------

or, as an example

== Run


----------------------------
python3 testasciidoc3.py run 27

27: German language file (article)
SOURCE: asciidoc3: data/lang-de-test.txt
SKIPPED: docbook: data/lang-de-article-test-docbook.xml
SKIPPED: xhtml11: data/lang-de-article-test-xhtml11.html
SKIPPED: html4: data/lang-de-article-test-html4.html
SKIPPED: html5: data/lang-de-article-test-html5.html

TOTAL SKIPPED: 4
-----------------------------

'TOTAL SKIPPED' pops up because testasciidoc3.py first needs to generate the output to compare
with 'testasciidoc3.py run':


== Update

----------------------------
python3 testasciidoc3.py update 27 xhtml11

WRITING: data/lang-de-article-test-xhtml11.html
----------------------------

Now it works as expected:

----------------------------
python3 testasciidoc3.py run 27 xhtml11

27: German language file (article)
SOURCE: asciidoc3: data/lang-de-test.txt
PASSED: xhtml11: data/lang-de-article-test-xhtml11.html

TOTAL PASSED:  1
-----------------------------

With this information feel free to perform your own test series ...
