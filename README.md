# newsspider
A parallel data crawler used to build the Bianet corpus.

written by Duygu Ataman

published October 1, 2017.


The news crawling spider is based on the Scrapy library. 

Starting from a given web page, it follows the links page by page, reads each news article, and for each article, extracts the links to its translations to different languages. The articles are limited to the domains specified in the domains list, which can be modified to include other articles in different categories. For each retrieved article id, the program saves two to three documents with the same id representing the original translation and its translation in different languages. The raw text is extracted and saved in the collections of documents.

The collected documents can be processed and aligned to build a single parallel corpus in each language pair. Example scripts are given in /scripts-process. For alignments, the hunalign tool is used.

If you would like to use this tool, make sure to modify the hard-coded website information, and check with permissions from the website from which you will crawl data.

For further questions you can contact Duygu Ataman at ataman@fbk.eu.
