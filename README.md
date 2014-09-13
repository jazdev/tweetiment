tweetiment v1.0
===============

Tweetiment: Twitter Sentiment Analysis

This project is NOT under active development.

======================

This document gives a quick overview on how to use this program.


###1. Installation

Download the whole project source from GitHub. [Do this by clicking here](https://github.com/jazdev/tweetiment/archive/master.zip). Once downloaded, extract the source to a directory of your choice. 

The project has the following directory structure:

```
your-working-dir/
 |
 |-word_scores/
 |  |-AFINN-111.txt
 |
 |-screenshots/
 |-tweetiment.py
 |-LICENSE
 |-README.md
 |-requirements.txt

```

* The ```word_scores/``` directory contains the AFFIN file, which is a list of English words rated for valence with an integer between minus five (negative) and plus five (positive).

* ```screenshots/``` contains runtime screenshots of the program.

* The ```tweetiment.py``` file is the main executable program code. We'll run this file to use the program.

* The ```LICENSE``` contains important copyright references and redistribution terms.

* The ```requirements.txt``` file lists all the requirements that need to be satisfied in order to run this software. 

To install the required packages use the following command: 

``` 
		$ pip install -r /path/to/requirements.txt
```	

In particular, this program requires you to have the following libraries:
* Tkinter
* ttk
* tkintertable
* oauth2
* urllib2

###2. Running the Program

The program can be run in the following ways:

* Command Line method:
	
	```python tweetiment.py```

* Using IDLE:

	Open the file in IDLE IDE and press F5 to run the program















