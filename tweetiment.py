#!/usr/bin/python

try:
    import Tkinter as tk     ## Python 2.x
except ImportError:
    import tkinter as tk     ## Python 3.x 

import os
import re
import sys
import ttk
import uuid
from ttk import Frame, Style
import tkMessageBox
import ConfigParser
import time, datetime
import json
import oauth2 as oauth
import urllib2 as urllib
from threading import Thread
from time import sleep
from tkintertable.Tables import TableCanvas
from tkintertable.TableModels import TableModel

class TweetimentFrame(tk.Frame):
    """

    """

    count = 0
    
    twitterAuthOpenedFlag = False
    tweetSentimentOpenedFlag = False
    termFrequenciesOpenedFlag = False
    happiestStateOpenedFlag = False
    twitterAuthCompletedFlag = False
    
    twitterStreamUpdatedFlag = False
    
    TwitterKeysFile = "Twitter_API_Keys"
    ConfigFile = "config.json"
    AFINNFile = "word_scores/AFINN-111.txt"
    TwitterStreamFile = "TwitterStream.txt"

    config = {}
    
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)            
        self.parent = parent
        self.initUI()
        
    def initUI(self):
        self.parent.title("Tweetiment")
        self.pack(fill=tk.BOTH, expand=1)

        
        if not os.path.isfile(self.TwitterKeysFile):
            TwitterAuthButton = tk.Button(self.parent, text = "Set Twitter Credentials", command = self.setTwitterAuth, bg="blue", fg="white")
            TwitterAuthButton.place(x = 100, y = 50, width = 200, height = 30)
        else:
            TwitterAuthButton = tk.Button(self.parent, text = "Update Twitter Credentials", command = self.updateTwitterAuth, bg="gray", fg="white")
            TwitterAuthButton.place(x = 100, y = 50, width = 200, height = 30)

        
        self.var = tk.StringVar()
       
        if os.path.isfile(self.ConfigFile):

            with open(self.ConfigFile, 'r') as f:
                cfg = json.load(f)
            try:        
                updated = cfg['TwitterStreamLastUpdated']
            except:
                updated = None
                
            if updated:
                self.var.set("Stream last updated on: " + updated)
                
                TwitterStreamStatusLabel = tk.Label(self.parent, textvariable = self.var, justify = tk.LEFT, wraplength = 400)
                TwitterStreamStatusLabel.place(x = 320, y = 100, width = 400, height = 30)

                UpdateTwitterStreamButton = tk.Button(self.parent, text = "Update Twitter Stream", command = self.updateTwitterStream, bg="gray", fg="white")
                UpdateTwitterStreamButton.place(x = 100, y = 100, width = 200, height = 30)
            
        else:
            self.var.set("Download Required")
        
            TwitterStreamStatusLabel = tk.Label(self.parent, textvariable = self.var, justify = tk.LEFT, wraplength = 400)
            TwitterStreamStatusLabel.place(x = 320, y = 100, width = 400, height = 30)

            DownloadTwitterStreamButton = tk.Button(self.parent, text = "Download Twitter Stream", command = self.updateTwitterStream, bg="blue", fg="white")
            DownloadTwitterStreamButton.place(x = 100, y = 100, width = 200, height = 30)

##        global TweetSentimentTermEntry
##        TweetSentimentTermEntry = tk.Entry(self.parent, bd =5)
##        TweetSentimentTermEntry.place(x = 400, y = 150, width = 200, height = 30)
##        TweetSentimentTermEntry.focus()
        
        RunTweetSentimentButton = tk.Button(self.parent, text = "Run Tweet Sentiment", command = self.findTweetSentiment, bg="blue", fg="white")
        RunTweetSentimentButton.place(x = 100, y = 150, width = 200, height = 30)

        TermFrequencyButton = tk.Button(self.parent, text = "Show Term Frequencies", command = self.findTermFrequencies, bg="blue", fg="white")
        TermFrequencyButton.place(x = 100, y = 200, width = 200, height = 30)

        HappiestStateButton = tk.Button(self.parent, text = "Show Happiest State", command = self.findHappiestState, bg="blue", fg="white")
        HappiestStateButton.place(x = 100, y = 250, width = 200, height = 30)
        
        TweetimentCloseButton = tk.Button(self.parent, text = "Exit", command = lambda: self.parent.destroy(), bg="blue", fg="white")
        TweetimentCloseButton.place(x = 100, y = 300, width = 70, height = 30)

        
    def setTwitterAuth(self):
        self.count += 1
        if self.twitterAuthOpenedFlag == False:

            self.twitterAuthOpenedFlag = True
            
            global TwitterKeysWindow
            TwitterKeysWindow = tk.Toplevel(self)
            TwitterKeysWindow.minsize(600, 500)
            TwitterKeysWindow.geometry("600x500+100+100")
            TwitterKeysWindow.title("Twitter API Authentication Details")
            TwitterKeysWindow.config(bd=5)
            L0 = tk.Label(TwitterKeysWindow, justify = tk.LEFT, wraplength = 500, text="""Help:\n\n1. Create a twitter account if you do not already have one.\n2. Go to https://dev.twitter.com/apps and log in with your twitter credentials.\n3. Click "Create New App"\n4. Fill out the form and agree to the terms. Put in a dummy website if you don't have one you want to use.\n5. On the next page, click the "API Keys" tab along the top, then scroll all the way down until you see the section "Your Access Token". Click the button "Create My Access Token" \n6. Copy the four values into the provided space. These values are your "API Key", your "API secret", your "Access token" and your "Access token secret". """)

            L1 = tk.Label(TwitterKeysWindow, text="api_key")
            L2 = tk.Label(TwitterKeysWindow, text="api_secret")
            L3 = tk.Label(TwitterKeysWindow, text="access_token_key")
            L4 = tk.Label(TwitterKeysWindow, text="access_token_secret")
            L0.place(x=10, y=10, width=550, height=200)
            L1.place(x=50, y=250, width=150, height=30)
            L2.place(x=50, y=300, width=150, height=30)
            L3.place(x=50, y=350, width=150, height=30)
            L4.place(x=50, y=400, width=150, height=30)

            global E1, E2, E3, E4
            E1 = tk.Entry(TwitterKeysWindow, bd =5)
            E2 = tk.Entry(TwitterKeysWindow, bd =5)
            E3 = tk.Entry(TwitterKeysWindow, bd =5)
            E4 = tk.Entry(TwitterKeysWindow, bd =5)
            E1.place(x=250, y=250, width=300, height=30)
            E2.place(x=250, y=300, width=300, height=30)
            E3.place(x=250, y=350, width=300, height=30)
            E4.place(x=250, y=400, width=300, height=30)

            E1.focus()

            TwitterKeysWindow.update()
            self.parent.update()
            self.parent.update_idletasks() 

            TwitterVerifyButton = tk.Button(TwitterKeysWindow, text ="Save and Close", command = self.validateTwitterAuth, bg="blue", fg="white")
            TwitterVerifyButton.place(x=250, y=450, width=200, height=30)

            TwitterKeysCloseButton = tk.Button(TwitterKeysWindow, text ="Cancel", command = lambda: TwitterKeysWindow.withdraw(), bg="blue", fg="white")
            TwitterKeysCloseButton.place(x=480, y=450, width=70, height=30)
        else:
            TwitterKeysWindow.deiconify()


    def updateTwitterAuth(self):
        self.count += 1
        if self.twitterAuthOpenedFlag == False:

            self.twitterAuthOpenedFlag = True
            
            global TwitterKeysWindow
            TwitterKeysWindow = tk.Toplevel(self)
            TwitterKeysWindow.minsize(600, 500)
            #TwitterKeysWindow.overrideredirect(True)
            TwitterKeysWindow.geometry("600x500+100+100")
            TwitterKeysWindow.title("Twitter API Authentication Details")
            TwitterKeysWindow.config(bd=5)
            L0 = tk.Label(TwitterKeysWindow, justify = tk.LEFT, wraplength = 500, text="""Help:\n\n1. Create a twitter account if you do not already have one.\n2. Go to https://dev.twitter.com/apps and log in with your twitter credentials.\n3. Click "Create New App"\n4. Fill out the form and agree to the terms. Put in a dummy website if you don't have one you want to use.\n5. On the next page, click the "API Keys" tab along the top, then scroll all the way down until you see the section "Your Access Token". Click the button "Create My Access Token" \n6. Copy the four values into the provided space. These values are your "API Key", your "API secret", your "Access token" and your "Access token secret". """)

            L1 = tk.Label(TwitterKeysWindow, text="api_key")
            L2 = tk.Label(TwitterKeysWindow, text="api_secret")
            L3 = tk.Label(TwitterKeysWindow, text="access_token_key")
            L4 = tk.Label(TwitterKeysWindow, text="access_token_secret")
            L0.place(x=10, y=10, width=550, height=200)
            L1.place(x=50, y=250, width=150, height=30)
            L2.place(x=50, y=300, width=150, height=30)
            L3.place(x=50, y=350, width=150, height=30)
            L4.place(x=50, y=400, width=150, height=30)

            global E1, E2, E3, E4
            E1 = tk.Entry(TwitterKeysWindow, bd =5)
            E2 = tk.Entry(TwitterKeysWindow, bd =5)
            E3 = tk.Entry(TwitterKeysWindow, bd =5)
            E4 = tk.Entry(TwitterKeysWindow, bd =5)
            E1.place(x=250, y=250, width=300, height=30)
            E2.place(x=250, y=300, width=300, height=30)
            E3.place(x=250, y=350, width=300, height=30)
            E4.place(x=250, y=400, width=300, height=30)

            with open("Twitter_API_Keys", "r") as twitter_keys_file:
                twitter_keys = twitter_keys_file.read().split("|")
                print twitter_keys
                E1.insert(0, twitter_keys[0])
                E2.insert(0, twitter_keys[1])
                E3.insert(0, twitter_keys[2])
                E4.insert(0, twitter_keys[3])

            E1.focus()
            
            TwitterKeysWindow.update()
            self.parent.update()
            self.parent.update_idletasks() 
            
            TwitterVerifyButton = tk.Button(TwitterKeysWindow, text ="Update and Close", command = self.validateTwitterAuth, bg="blue", fg="white")
            TwitterVerifyButton.place(x=250, y=450, width=200, height=30)

            TwitterKeysCloseButton = tk.Button(TwitterKeysWindow, text ="Cancel", command = lambda: TwitterKeysWindow.withdraw(), bg="blue", fg="white")
            TwitterKeysCloseButton.place(x=480, y=450, width=70, height=30)
        else:
            TwitterKeysWindow.deiconify()        

    def validateTwitterAuth(self):
        E1_text = E1.get()
        E2_text = E2.get()
        E3_text = E3.get()
        E4_text = E4.get()
        
        if (E1_text == "" or E2_text == "" or E3_text == "" or E4_text == ""):
            tkMessageBox.showerror("ERROR", "Please fill all the fields", parent = TwitterKeysWindow)
        else:
            E1_text = E1.get()
            E2_text = E2.get()
            E3_text = E3.get()
            E4_text = E4.get()
            with open( self.TwitterKeysFile, "w" ) as twitter_keys_file:
                twitter_keys_file.write(E1_text + "|" + E2_text + "|" + E3_text + "|" + E4_text)
                
            self.twitterAuthOpenedFlag = False
            self.twitterAuthCompletedFlag = True

            if os.path.isfile(self.ConfigFile):
                cfg = {}
                with open('config.json', 'r') as f:
                    cfg = json.load(f)
                cfg['twitterAuthCompletedFlag'] = True
                st = datetime.datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y %H:%M:%S')
                cfg['twitterAuthLastUpdated'] = st
                with open('config.json', 'w') as f:
                    json.dump(cfg, f)

            else:    
                cfg = {}
                cfg['twitterAuthCompletedFlag'] = True
                st = datetime.datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y %H:%M:%S')
                cfg['twitterAuthLastUpdated'] = st
                with open('config.json', 'w') as f:
                    json.dump(cfg, f)



            self.initUI()
            TwitterKeysWindow.destroy()


    def updateTwitterStream(self):
        
        with open('config.json', 'r') as f:
            cfg = json.load(f)
                    
        if cfg['twitterAuthCompletedFlag'] == True:

            print "twitterAuthCompletedFlag = True"
            self.pb = ttk.Progressbar(self.parent, orient=tk.HORIZONTAL, mode='indeterminate', length = 200)
            self.pb.pack(side = tk.BOTTOM, fill = tk.BOTH)
            self.pb.start()

            self.var.set("Updating stream ... This operation takes 4-5 minutes to complete.")
            
            t= Thread(target=self.threadedTwitterRequest)
            t.start()
            
            st = datetime.datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y %H:%M:%S')
            if os.path.isfile(self.ConfigFile):
                cfg = {}
                with open('config.json', 'r') as f:
                    cfg = json.load(f)
                cfg['TwitterStreamLastUpdated'] = st
                with open('config.json', 'w') as f:
                    json.dump(cfg, f)
            else:    
                cfg = {}
                cfg['TwitterStreamLastUpdated'] = st
                with open('config.json', 'w') as f:
                    json.dump(cfg, f)

            self.initUI()

        else:
            tkMessageBox.showerror("ERROR", "Twitter API credentials not filled.", parent = self.parent)
            


    def threadedTwitterRequest(self):
        start_time = time.time()

##        search_term = TweetSentimentTermEntry.get()
        
        
        with open("Twitter_API_Keys", "r") as twitter_keys_file:
            twitter_keys = twitter_keys_file.read().split("|")
            print twitter_keys

        api_key = twitter_keys[0]
        api_secret = twitter_keys[1]
        access_token_key = twitter_keys[2]
        access_token_secret = twitter_keys[3]

        try:
            _debug = 0

            oauth_token    = oauth.Token(key=access_token_key, secret=access_token_secret)
            oauth_consumer = oauth.Consumer(key=api_key, secret=api_secret)

            signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()

            http_method = "GET"

            http_handler  = urllib.HTTPHandler(debuglevel=_debug)
            https_handler = urllib.HTTPSHandler(debuglevel=_debug)


##            if search_term == "":
##                url = "https://stream.twitter.com/1/statuses/sample.json"
##            else:
##                url = "https://api.twitter.com/1.1/search/tweets.json?q="
##                url += search_term.strip().split()[0]
##            print search_term

            url = "https://stream.twitter.com/1/statuses/sample.json"    
            print url
            
            parameters = []

            
            req = oauth.Request.from_consumer_and_token(oauth_consumer,
                                                         token=oauth_token,
                                                         http_method=http_method,
                                                         http_url=url, 
                                                         parameters=parameters)

            req.sign_request(signature_method_hmac_sha1, oauth_consumer, oauth_token)

            headers = req.to_header()

            if http_method == "POST":
                encoded_post_data = req.to_postdata()
            else:
                encoded_post_data = None
                url = req.to_url()

            opener = urllib.OpenerDirector()
            opener.add_handler(http_handler)
            opener.add_handler(https_handler)
            if os.path.isfile(self.TwitterStreamFile):
                os.remove(self.TwitterStreamFile)
            response = opener.open(url, encoded_post_data)
            
            
            for line in response:
                #print line
                self.var.set("Updating... This process takes 4-5 minutes to complete.")
                
                print "abs(time.time() - start_time)", abs(time.time() - start_time)
                
                if abs(time.time() - start_time) >= 20:
                    self.pb.pack_forget()
                    self.var.set("Update complete.")
                    return
                
                with open(self.TwitterStreamFile, "a") as twitter_stream_file:
                    twitter_stream_file.write(line.strip()  + os.linesep)
        except:
            print "EXCEPTION"


            
    def findTweetSentiment(self):

        self.count += 1
        if self.tweetSentimentOpenedFlag == False:

            self.tweetSentimentOpenedFlag = True

            global TweetSentimentWindow
            
            def toggleFlag():
                self.tweetSentimentOpenedFlag = False
                TweetSentimentWindow.destroy()

                
            
            TweetSentimentWindow = tk.Toplevel(self)
            TweetSentimentWindow.minsize(600, 500)
            #TwitterKeysWindow.overrideredirect(True)
            TweetSentimentWindow.geometry("1000x500+100+100")
            TweetSentimentWindow.title("Tweet Sentiments (Zero values omitted)")
            TweetSentimentWindow.config(bd=5)

            TweetSentimentWindow.protocol("WM_DELETE_WINDOW", toggleFlag)

            model = TableModel()
            table = TableCanvas(TweetSentimentWindow, model=model,
                                 editable=False)
            table.createTableFrame()

            tableData = {}
            
            afinnfile = open(self.AFINNFile)
            scores = {} 
            for line in afinnfile:
                    term, score  = line.split("\t")  
                    scores[term] = int(score)  

            #print scores.items() 

            positive = 0.0
            negative = 0.0
            
            outfile = open(self.TwitterStreamFile)
            for line in outfile:
                    json_obj = json.loads(line)
                    sentiment = 0
                    try:            
                        text = json_obj['text'].decode('utf-8')
                        text = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)","",text).split())
                        text = re.sub(r'^https?:\/\/.*[\r\n]*', '', text, flags=re.MULTILINE)
                        text = re.sub(r'RT', '', text, flags=re.MULTILINE)
                        
                        #print text
                        text_list = text.split(' ')
                        for char in text_list:
                            if char in scores:
                                    sentiment += scores[char]

                        if sentiment != 0:
                            tableData[uuid.uuid4()] = {'Tweet': text, 'Score': str(sentiment)}
                            if sentiment > 0:
                                positive += 1
                            elif sentiment < 0:
                                negative += 1
                            #print text + "   " + str(sentiment) + "\n\n"
                            

                    except:
                        #print "passed"
                        pass
            if positive > 0 and negative > 0:
                ratio = round(float(positive) / float(negative), 2)
                
            model.importDict(tableData)
            #table.adjustColumnWidths()
            table.resizeColumn(0, 850)
            table.resizeColumn(1, 50)
            table.sortTable(columnName='Score')
            table.redrawTable()

            if positive > negative:
                extra = "The overall sentiment is POSITIVE."
            else:    
                extra = "The overall sentiment is NEGATIVE."
            
            tkMessageBox.showinfo("Score Ratio", "The ratio of positive vs. negative tweets is " + str(ratio) + ". " + extra, parent = TweetSentimentWindow)

                    
    def findTermFrequencies(self):
        self.count += 1
        if self.termFrequenciesOpenedFlag == False:
            self.termFrequenciesOpenedFlag = True
            global TermFrequenciesWindow

            def toggleFlag():
                self.termFrequenciesOpenedFlag = False
                TermFrequenciesWindow.destroy()
                
            TermFrequenciesWindow = tk.Toplevel(self)
            TermFrequenciesWindow.minsize(500, 500)
            #TwitterKeysWindow.overrideredirect(True)
            TermFrequenciesWindow.geometry("500x500+100+100")
            TermFrequenciesWindow.title("Term Frequencies (only > 0.5%)")
            TermFrequenciesWindow.config(bd=5)

            TermFrequenciesWindow.protocol("WM_DELETE_WINDOW", toggleFlag)

            model = TableModel()
            table = TableCanvas(TermFrequenciesWindow, model=model,
                                 editable=False)
            table.createTableFrame()

            tableData = {}
            
            freqs = {}
            total = 0
            outfile = open(self.TwitterStreamFile)
            for line in outfile:
                json_obj = json.loads(line)
                try:            
                    text = json_obj['text'].decode('utf-8')
                    text = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)","",text).split())
                    text = re.sub(r'^https?:\/\/.*[\r\n]*', '', text, flags=re.MULTILINE)
                    text = re.sub(r'RT', '', text, flags=re.MULTILINE)
                    #print text
                    text_list = text.split(' ')
                    for char in text_list:
                        if char.isalnum():
                            if char not in freqs:
                                freqs[char] = 1
                            else:
                                freqs[char] += 1
                            total += 1  

                except:
                    #print "passed"
                    pass
                    
            for key in freqs.keys():
                if freqs[key]/float(total) > 0.005:
                    tableData[uuid.uuid4()] = {'Term': key, 'Frequency (%)': str(round((freqs[key]/float(total))*100, 2))}
                #print key + " " + str(freqs[key]/float(total)) 


            model.importDict(tableData)
            #sort in descending order
            model.setSortOrder(columnIndex = 1, reverse = 1)
            table.adjustColumnWidths()
            table.resizeColumn(0, 200)
            table.resizeColumn(1, 200)
            #table.sortTable(columnName='Frequency')
            table.redrawTable()


    def findHappiestState(self):
        states = {
            'AK': 'Alaska',
            'AL': 'Alabama',
            'AR': 'Arkansas',
            'AS': 'American Samoa',
            'AZ': 'Arizona',
            'CA': 'California',
            'CO': 'Colorado',
            'CT': 'Connecticut',
            'DC': 'District of Columbia',
            'DE': 'Delaware',
            'FL': 'Florida',
            'GA': 'Georgia',
            'GU': 'Guam',
            'HI': 'Hawaii',
            'IA': 'Iowa',
            'ID': 'Idaho',
            'IL': 'Illinois',
            'IN': 'Indiana',
            'KS': 'Kansas',
            'KY': 'Kentucky',
            'LA': 'Louisiana',
            'MA': 'Massachusetts',
            'MD': 'Maryland',
            'ME': 'Maine',
            'MI': 'Michigan',
            'MN': 'Minnesota',
            'MO': 'Missouri',
            'MP': 'Northern Mariana Islands',
            'MS': 'Mississippi',
            'MT': 'Montana',
            'NA': 'National',
            'NC': 'North Carolina',
            'ND': 'North Dakota',
            'NE': 'Nebraska',
            'NH': 'New Hampshire',
            'NJ': 'New Jersey',
            'NM': 'New Mexico',
            'NV': 'Nevada',
            'NY': 'New York',
            'OH': 'Ohio',
            'OK': 'Oklahoma',
            'OR': 'Oregon',
            'PA': 'Pennsylvania',
            'PR': 'Puerto Rico',
            'RI': 'Rhode Island',
            'SC': 'South Carolina',
            'SD': 'South Dakota',
            'TN': 'Tennessee',
            'TX': 'Texas',
            'UT': 'Utah',
            'VA': 'Virginia',
            'VI': 'Virgin Islands',
            'VT': 'Vermont',
            'WA': 'Washington',
            'WI': 'Wisconsin',
            'WV': 'West Virginia',
            'WY': 'Wyoming'
        }
        
        happy_locations = {}
        full_states = states.values()
        afinnfile = open(self.AFINNFile)
        scores = {} # initialize an empty dictionary
        for line in afinnfile:
            term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
            scores[term] = int(score)  # Convert the score to an integer.
                
        outfile = open(self.TwitterStreamFile)
        for line in outfile:
            json_obj = json.loads(line)
            try:	 
                user = json_obj['user']
                location = user['location'].decode('utf-8')
                if location != "":
                    if location in states.values():
                        #print location
                        sentiment = 0
                        text = json_obj['text'].decode('utf-8')
                        text_list = text.split(' ')		
                        for char in text_list:
                            if char in scores:
                                sentiment += scores[char]
                        
                        if location not in happy_locations:	
                            happy_locations[location] = sentiment
                        else:
                            happy_locations[location] += sentiment	
            except:
                pass	
                        
                        
        slist = [(k, happy_locations[k]) for k in sorted(happy_locations, key=happy_locations.get, reverse=True)]
        happiest_state = ""
        for k, v in states.iteritems():
            if v == slist[0][0]:
                happiest_state = v

        tkMessageBox.showinfo("Happiest State", "The happiest state in the US is " + str(happiest_state) + ".\n\n(Based on positive sentiments per state)", parent = self.parent)

            
    
def main():
    global root
    root = tk.Tk()
    root.geometry("800x400+100+100")
    app = TweetimentFrame(root)
    root.mainloop()  


if __name__ == '__main__':
    main() 
