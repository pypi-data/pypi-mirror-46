What is stpip?
==============

[![DOI](https://zenodo.org/badge/176632808.svg)](https://zenodo.org/badge/latestdoi/176632808)

stpip is a simple webscraping program the looks for pypi download statistics from the pepy.tech webpage [https://github.com/psincraian/pepy]


How to install stpip?
=====================

A simple `pip install stpip` will do the installation, with the only dependencies. The last version is 19.3.2.


How to use it?
==============

To display the help you can `stpip --help` and you will get:

	`usage: stpip [-h] [-w] [-m] [-t] [--version] package

	A pepy.tech web scraping for pypi download stats, version 19.3.0, Licence: GPL

	optional arguments:
	  -h, --help  show this help message and exit
	  -p P        file, or list of file separated by comas (no space)
	  -w          if you just want the last week download counts
	  -m          if you just want the last month download counts
	  -t          if you just want download counts all time
	  --version   Display the version of stpip

The only mandatory argument is the name of the package. Providing only this one will give all the information. For example, `matplotlip`:

	>> stpip -p matplotlib

will give:

	###############################################
	      Download counts for matplotlib 
	 Total all time: 48011552
	 Total last 30 days: 6327682
	 Total last 7 days: 1790028
	 last day 2019-03-18: 234,726
	--> visit https://pepy.tech/project/matplotlib 
	##############################################

Then you can ask for some particular information with the '-t' (only total), '-m' (last month) and '-w' (only last week):

	>> stpip -p matplotlib -t

will give:

	###############################################
	      Download counts for matplotlib 
	 Total all time: 48011552
	--> visit https://pepy.tech/project/matplotlib 
	##############################################


You can also give multiple packages:

	>> stpip -p matplotlib,numpy

will give:

	###############################################
	      Download counts for matplotlib 
	 Total all time: 48011552
	 Total last 30 days: 6327682
	 Total last 7 days: 1790028
	 last day 2019-03-18: 234,726
	--> visit https://pepy.tech/project/matplotlib 
	##############################################


	###############################################
	      Download counts for numpy 
	 Total all time: 171005305
	 Total last 30 days: 20108764
	 Total last 7 days: 4608706
	 last day 2019-03-18: 736,912
	--> visit https://pepy.tech/project/numpy 
	##############################################

