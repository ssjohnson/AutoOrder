from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import jsonparse
import nameconfig

import tkinter
from tkinter import ttk

class Window(ttk.Frame):
    
    def __init__(self, master=None):
        ttk.Frame.__init__(self, master)
        self.master = master
        self.init_window()
        
    #Create GUI
    def init_window(self):
        self.master.title("Auto Order")
        self.master.minsize(width=500, height=500)
        self.pack(fill='both', expand=1)
        startButton = ttk.Button(self, text="Open Chrome", command=self.runBrowser)
        startButton.place(x=20, y=20)
        
    def runBrowser(self):
        # Open & Maximize Chrome
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get("http://www.bel-aqua.com")

        # Login into BA.com
        driver.find_element_by_id("txtEmail").send_keys(nameconfig.username)
        driver.find_element_by_id("txtPassword").send_keys(nameconfig.password)
        driver.find_element_by_id("SubmitLogon").click()

        #Go to Quick Order Pad URL
        driver.get("http://www.bel-aqua.com/default.aspx?Page=Quick%20OrderPad")

        #Fill out form & submit
        driver.find_element_by_id("txtItemID0").send_keys("dpd1box")
        driver.find_element_by_id("txtQuantity0").send_keys("6")
        driver.find_element_by_id("ButtonQOPAddToCart").click()

        
root = tkinter.Tk()

app = Window(root)

root.mainloop()


