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


###3. Program Walkthrough

The correct way to use this program is as follows:

####a. Main Screen

This is the main screen of the program. It has all the options that the user can select by pressing the appropriate button. Usually, you'll want to select the ```Set Twitter Credentials``` button if this is the first time you are running the program.

<img style="float: right" src="https://raw.githubusercontent.com/jazdev/tweetiment/master/screenshots/1.png" alt="Tweetiment: Main screen" />

####b. Set Twitter Credentials Screen

This screen allows the user to save his/her Twitter API access credentials in the program. This step is **required** and must be completed before moving further. The steps to get your own API credentials are mentioned in the same window. (See screenshot below)

<img style="float: right" src="https://raw.githubusercontent.com/jazdev/tweetiment/master/screenshots/2.png" alt="Tweetiment: Set Twitter Credentials Screen" />

####c. Update Twitter Strean File

After filling out your Twitter API credentials, press the ```Download Twitter Stream``` button (if first run) or the ```Update Twitter Stream``` button (if not first run). This causes the program to connect to the Twitter API with the provided credentials, and download a stream of tweets to a local cache file on the users hard drive. This process takes 1-2 minutes to complete because we need sufficient amount of accumulated tweets before we move on to further processing.

<img style="float: right" src="https://raw.githubusercontent.com/jazdev/tweetiment/master/screenshots/3.png" alt="Tweetiment: Update Twitter Strean File" />

####d. Run Tweet Sentiment

After the Twitter stream has been downloaded and saved to the cache, we can proceed to find the sentiments of the cached Tweets. Press the ```Run Tweet Sentiment``` button to start this process. This will open a new window with the results displayed in a table. Plus, an alert will also be shown that summarizes the results. The alert box will show the ratio of positive to negative sentiments. If the resulting ratio is greater than 1, it means that the overall sentiment is positive, else the overall sentiment is negative.

<img style="float: right" src="https://raw.githubusercontent.com/jazdev/tweetiment/master/screenshots/5.png" alt="Tweetiment: Run Tweet Sentiment Summary" />

The figure below shows the table which lists the individual tweets with their corresponding sentiments. The table data is sorted in ascending order for better readability.

<img style="float: right" src="https://raw.githubusercontent.com/jazdev/tweetiment/master/screenshots/6.png" alt="Tweetiment: Run Tweet Sentiment Table" />
