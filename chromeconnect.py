from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import tkinter
from tkinter import ttk
from tkinter import messagebox

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
        
        validate_cmd = (self.register(checkEntry), '%P')
        
        entry_array = []
        x = 0
        items = jsonparse.getParts()
        for parts in items:
            l1 = ttk.Label(self, text=parts["Description"])
            e1 = ttk.Entry(self, validate='key', validatecommand=validate_cmd, invalidcommand= lambda: messagebox.showinfo("Invalid Entry", "Please enter a valid integer"))
            entry_array.append(e1)
            l1.grid(row=x, column=0, padx=2, pady=2)
            e1.grid(row=x, column=1, padx=2, pady=2)
            x = x + 1
        submitButton = ttk.Button(self, text="Enter Order", command= lambda:filterArray(items, entry_array))
        submitButton.grid(row=x, columnspan=2, padx=2, pady=2)
        
""""
Function checkEntry
    ARGS:
        text: the contents of the textbox we are vaildating
        
    Returns: 
        true if it is an integer
        false if it is not an integer
""""
        
def checkEntry(text):
    try:
        int(text)
        print("true")
        return True
    except ValueError:
        print("false")
        return False
    



""""
Function: filterArray
    ARGS:
        items: complete listing of items on given page, from jsonparse
        entry_array: all of the textboxes on the page

    Checks to make sure there is an entry in the textbox:
        textbox empty: do nothing with the item
        textbox has quantity: append to selected_items array as a tuple of the item(0) and its quantity(1)

    Program then passes selected_items to runBrowser to enter onto webpage
"""

def filterArray(items, entry_array):
    selected_items = []
    count = 0
    for item in items:
        quantity = entry_array[count].get()
        if quantity != "":
            selected_items.append((item, quantity))
        count = count + 1
    runBrowser(selected_items)



""""
Function: runBrowser
    Args: 
        selected_items: array of tuples (json element, quantity ordered)
    
    Opens & Maximizes Chrome
    Opens "bel-aqua.com"
    Logs in using info from separate log in info file (nameconfig.py)
    Fills out quick order pad using info from tuples
        quick order pad only allows 5 items at a time, loop keeps counter, submits with 5 entries, then starts again
    Leaves user to validate entries & checkout
""""

def runBrowser(selected_items):
    
    # Open & Maximize Chrome
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("http://www.bel-aqua.com")

    # Login into BA.com
    driver.find_element_by_id("txtEmail").send_keys(nameconfig.username)
    driver.find_element_by_id("txtPassword").send_keys(nameconfig.password)
    driver.find_element_by_id("SubmitLogon").click()

    #Go to Quick Order Pad URL
    #driver.get("http://www.bel-aqua.com/default.aspx?Page=Quick%20OrderPad")
    

    #Fill out form & submit
    item_count = 0
    entered_count = 0
    
    for item in selected_items:
        driver.find_element_by_id("txtItemID" + str(entered_count)).send_keys(item[0]["BANum"])
        driver.find_element_by_id("txtQuantity" + str(entered_count)).send_keys(item[1])
        item_count = item_count + 1
        entered_count = entered_count + 1
        if entered_count % 5 == 0:
            entered_count = 0
            driver.find_element_by_id("ButtonQOPAddToCart").click()
    driver.find_element_by_id("ButtonQOPAddToCart").click()
        

        
        
"""
Opens window & begins running loop
"""

root = tkinter.Tk()

app = Window(root)

root.mainloop()

