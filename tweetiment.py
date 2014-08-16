#!/usr/bin/python

try:
    import Tkinter as tk     ## Python 2.x
except ImportError:
    import tkinter as tk	 ## Python 3.x 


#from PIL import Image, ImageTk
#from Tkinter import Tk, Label, BOTH, Button
from ttk import Frame, Style

class TweetimentFrame(tk.Frame):
	count = 0
	
	def __init__(self, parent):
		tk.Frame.__init__(self, parent)            
		self.parent = parent
		self.initUI()
		
	def initUI(self):
		self.parent.title("Tweetiment")
		self.pack(fill=tk.BOTH, expand=1)
		style = Style()
		style.configure("TFrame", background="#333")  
		TwitterAuthButton = tk.Button(self.parent, text ="Set Twitter Credentials", command = self.setTwitterAuth, bg="blue", fg="white")
		TwitterAuthButton.place(x=100,y=50,width=200, height=30)    
		
	def setTwitterAuth(self):
		self.count += 1
		window = tk.Toplevel(self)
		label = Label(window, text="Twitter Authentication Details")
		label.pack(side="top", fill="both", padx=10, pady=10)
        
		

class TwitterAuthFrame(tk.Frame):
  
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)            
        self.parent = parent
        self.initUI()
        
    def initUI(self):
      
        self.title("Twitter Authentication Details")
        self.pack(fill=BOTH, expand=1)
        style = Style()
        style.configure("TFrame", background="#333")  
          
    	

	
def main():
	global root
	root = tk.Tk()
	root.geometry("800x400+100+100")
	app = TweetimentFrame(root)
	root.mainloop()  


if __name__ == '__main__':
    main() 
