from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import tkinter
from tkinter import ttk

import jsonparse
import nameconfig

#Create GUI & Populate
class Window(ttk.Frame):
    
    def __init__(self, master=None):
        ttk.Frame.__init__(self, master)
        self.master = master
        self.init_window()
        
    #Create & populate GUI
    def init_window(self):
        self.master.title("Auto Order")
        self.master.minsize(width=500, height=500)
        self.pack(fill='both', expand=1, padx=10, pady=10)
        
        entry_array = []
        x = 0
        items = jsonparse.getParts()
        for parts in items:
            l1 = ttk.Label(self, text=parts["Description"])
            e1 = ttk.Entry(self)
            entry_array.append(e1)
            l1.grid(row=x, column=0, padx=2, pady=2)
            e1.grid(row=x, column=1, padx=2, pady=2)
            x = x + 1
            
        submitButton = ttk.Button(self, text="Enter Order", command= lambda:runBrowser(items, entry_array))
        submitButton.grid(row=x, columnspan=2, padx=2, pady=2)
        
def runBrowser(items,entry_array):
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
    item_count = 0
    entered_count = 0
    
    for item in items:
        driver.find_element_by_id("txtItemID" + str(entered_count)).send_keys(item["BANum"])
        driver.find_element_by_id("txtQuantity" + str(entered_count)).send_keys(entry_array[item_count].get())
        item_count = item_count + 1
        entered_count = entered_count + 1
        if entered_count % 5 == 0:
            entered_count = 0
            driver.find_element_by_id("ButtonQOPAddToCart").click()
        
    driver.find_element_by_id("ButtonQOPAddToCart").click()
        

        
root = tkinter.Tk()

app = Window(root)

root.mainloop()


