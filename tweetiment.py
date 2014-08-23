#!/usr/bin/python

try:
    import Tkinter as tk     ## Python 2.x
except ImportError:
    import tkinter as tk     ## Python 3.x 

import os
import ttk
from ttk import Frame, Style
import tkMessageBox
import ConfigParser
import time, datetime
import json
import oauth2 as oauth
import urllib2 as urllib
from threading import Thread

class TweetimentFrame(tk.Frame):
    """

    """

    count = 0
    
    twitterAuthOpenedFlag = False
    twitterAuthCompletedFlag = False
    
    twitterStreamUpdatedFlag = False
    
    TwitterKeysFile = "Twitter_API_Keys"
    ConfigFile = "config.json"

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

        var = tk.StringVar()
       
        if os.path.isfile(self.ConfigFile):

            with open(self.ConfigFile, 'r') as f:
                cfg = json.load(f)
            try:        
                updated = cfg['TwitterStreamLastUpdated']
            except:
                updated = None
                
            if updated:
                var.set("Last updated on: " + updated)
                
                TwitterStreamStatusLabel = tk.Label(self.parent, textvariable = var)
                TwitterStreamStatusLabel.place(x = 320, y = 100, width = 300, height = 30)

                TweetimentCloseButton = tk.Button(self.parent, text = "Update Twitter Stream", command = self.updateTwitterStream, bg="gray", fg="white")
                TweetimentCloseButton.place(x = 100, y = 100, width = 200, height = 30)
            
        else:
            var.set("Download Required")
        
            TwitterStreamStatusLabel = tk.Label(self.parent, textvariable = var)
            TwitterStreamStatusLabel.place(x = 320, y = 100, width = 200, height = 30)

            TweetimentCloseButton = tk.Button(self.parent, text = "Download Twitter Stream", command = self.updateTwitterStream, bg="blue", fg="white")
            TweetimentCloseButton.place(x = 100, y = 100, width = 200, height = 30)


        TweetimentCloseButton = tk.Button(self.parent, text = "Exit", command = lambda: self.parent.destroy(), bg="blue", fg="white")
        TweetimentCloseButton.place(x = 100, y = 150, width = 70, height = 30)

        
    def setTwitterAuth(self):
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
                with open('config.json', 'w') as f:
                    json.dump(cfg, f)

            else:    
                cfg = {}
                cfg['twitterAuthCompletedFlag'] = True
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
 
            def threadedTwitterRequest():
                with open("Twitter_API_Keys", "r") as twitter_keys_file:
                    twitter_keys = twitter_keys_file.read().split("|")
                    print twitter_keys

                api_key = twitter_keys[0]
                api_secret = twitter_keys[1]
                access_token_key = twitter_keys[2]
                access_token_secret = twitter_keys[3]

                _debug = 0

                oauth_token    = oauth.Token(key=access_token_key, secret=access_token_secret)
                oauth_consumer = oauth.Consumer(key=api_key, secret=api_secret)

                signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()

                http_method = "GET"

                http_handler  = urllib.HTTPHandler(debuglevel=_debug)
                https_handler = urllib.HTTPSHandler(debuglevel=_debug)

                url = "https://stream.twitter.com/1/statuses/sample.json"
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

                response = opener.open(url, encoded_post_data)

                for line in response:
                    print line.strip()


            t = Thread(target = threadedTwitterRequest)
            t.daemon = True               
            t.start()

            run_time = 5 #* 60
            sleep(run_time)

            
            #t1 = threading.Thread(target = threadedTwitterRequest)
            #t1.start()
            #t1.join()
            
            
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
            
            #self.pb.stop()
            self.pb.pack_forget()
            self.initUI()

        else:
            tkMessageBox.showerror("ERROR", "Twitter API credentials not filled.", parent = self.parent)
            
        
    
def main():
    global root
    root = tk.Tk()
    root.geometry("800x400+100+100")
    app = TweetimentFrame(root)
    root.mainloop()  


if __name__ == '__main__':
    main() 
