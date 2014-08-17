#!/usr/bin/python

try:
    import Tkinter as tk     ## Python 2.x
except ImportError:
    import tkinter as tk     ## Python 3.x 

import os
#from PIL import Image, ImageTk
#from Tkinter import Tk, Label, BOTH, Button
from ttk import Frame, Style
import tkMessageBox

class TweetimentFrame(tk.Frame):
    count = 0
    twitter_auth_opened = False
    
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)            
        self.parent = parent
        self.initUI()
        
    def initUI(self):
        self.parent.title("Tweetiment")
        self.pack(fill=tk.BOTH, expand=1)
        if not os.path.isfile('Twitter_API_Keys'):
            TwitterAuthButton = tk.Button(self.parent, text ="Set Twitter Credentials", command = self.setTwitterAuth, bg="blue", fg="white")
            TwitterAuthButton.place(x=100,y=50,width=200, height=30)
        else:
            TwitterAuthButton = tk.Button(self.parent, text ="Update Twitter Credentials", command = self.updateTwitterAuth, bg="gray", fg="white")
            TwitterAuthButton.place(x=100,y=50,width=200, height=30)

        TweetimentCloseButton = tk.Button(self.parent, text ="Exit", command = lambda: self.parent.destroy(), bg="blue", fg="white")
        TweetimentCloseButton.place(x=400,y=50,width=70, height=30)

        
    def setTwitterAuth(self):
        self.count += 1
        if self.twitter_auth_opened == False:

            self.twitter_auth_opened = True
            
            global TwitterKeysWindow
            TwitterKeysWindow = tk.Toplevel(self)
            TwitterKeysWindow.minsize(600, 500)
            TwitterKeysWindow.overrideredirect(True)
            TwitterKeysWindow.geometry("600x500+100+100")
            TwitterKeysWindow.title("Twitter API Authentication Details")
            TwitterKeysWindow.config(bd=5)
            L0 = tk.Label(TwitterKeysWindow, justify = tk.LEFT, wraplength = 500, text="""Help:\n
    1. Create a twitter account if you do not already have one.
    2. Go to https://dev.twitter.com/apps and log in with your twitter credentials.
    3. Click "Create New App"
    4. Fill out the form and agree to the terms. Put in a dummy website if you don't have one you want to use.
    5. On the next page, click the "API Keys" tab along the top, then scroll all the way down until you see the section "Your Access Token"
    Click the button "Create My Access Token".
    6. Copy the four values into the provided space. These values are your "API Key", your "API secret", your "Access token" and your "Access token secret". """)

            L1 = tk.Label(TwitterKeysWindow, text="api_key")
            L2 = tk.Label(TwitterKeysWindow, text="api_secret")
            L3 = tk.Label(TwitterKeysWindow, text="access_token_key")
            L4 = tk.Label(TwitterKeysWindow, text="access_token_secret")
            L0.place(x=50, y=10, width=550, height=200)
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
        if self.twitter_auth_opened == False:

            self.twitter_auth_opened = True
            
            global TwitterKeysWindow
            TwitterKeysWindow = tk.Toplevel(self)
            TwitterKeysWindow.minsize(600, 500)
            TwitterKeysWindow.overrideredirect(True)
            TwitterKeysWindow.geometry("600x500+100+100")
            TwitterKeysWindow.title("Twitter API Authentication Details")
            TwitterKeysWindow.config(bd=5)
            L0 = tk.Label(TwitterKeysWindow, justify = tk.LEFT, wraplength = 500, text="""Help:\n
    1. Create a twitter account if you do not already have one.
    2. Go to https://dev.twitter.com/apps and log in with your twitter credentials.
    3. Click "Create New App"
    4. Fill out the form and agree to the terms. Put in a dummy website if you don't have one you want to use.
    5. On the next page, click the "API Keys" tab along the top, then scroll all the way down until you see the section "Your Access Token"
    Click the button "Create My Access Token".
    6. Copy the four values into the provided space. These values are your "API Key", your "API secret", your "Access token" and your "Access token secret". """)

            L1 = tk.Label(TwitterKeysWindow, text="api_key")
            L2 = tk.Label(TwitterKeysWindow, text="api_secret")
            L3 = tk.Label(TwitterKeysWindow, text="access_token_key")
            L4 = tk.Label(TwitterKeysWindow, text="access_token_secret")
            L0.place(x=50, y=10, width=550, height=200)
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
            with open("Twitter_API_Keys", "w") as twitter_keys_file:
                twitter_keys_file.write(E1_text + "|" + E2_text + "|" + E3_text + "|" + E4_text)
            self.twitter_auth_opened = False
            self.parent.update()
            self.parent.update_idletasks()    
            TwitterKeysWindow.destroy()
            
        
    
def main():
    global root
    root = tk.Tk()
    root.geometry("800x400+100+100")
    app = TweetimentFrame(root)
    root.mainloop()  


if __name__ == '__main__':
    main() 
