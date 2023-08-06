# 1.Introduction to pyMd2Doc

Use python to convert markdown to a directory document with retractable text content.


# 2. Method of use

This program requires a python environment of python3 or above.


## 2.1 Prepare Markdown file

Prepare the Markdown file that needs to be converted into a document.


## 2.2 Install pyMd2Doc

Install the program using

	pip install pyMd2Doc


## 2.3 Start the conversion

### 2.3.1 md file to HTML

> creates [yourFileName].py file to prepare the markdown file that needs to be converted, such as mymarkdown.md

> introduces the required module, calls the function and passes in the markdown file to be converted, as shown in the following example:



	from pymd2doc import createDoc


	createDoc.create("myMarkdown")


The successful execution of > will generate the mymarkdown.html file


### 2.3.2 String md content to HTML

> introduces the required module, calls the function, and passes in the markdown file that needs to be converted

> passes in String md content, as shown in the following example:


	from pymd2doc import createDoc


	STR = u'''
			Here is the String md content
			'''

	# param strs passes in the MD string
	# param myMarkdown definition will generate the name of the HTML file
	# return myMarkdown.html

	createDoc.createByString(strs, "myMarkdown")

> The successful execution of > will generate the mymarkdown.html file


## 2.4 Check the documentation

Open the mymarkdown.html file you just generated with your browser.

Click the directory to jump to the corresponding document content.

