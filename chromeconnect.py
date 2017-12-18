import sys

import tkinter
from tkinter import ttk
from tkinter import Menu
from tkinter import messagebox

import placeorder
import jsonparse
import nameconfig

class AutoOrder(tkinter.Tk):
    
    def __init__(self, *args, **kwargs):
        tkinter.Tk.__init__(self,*args,**kwargs)
        tkinter.Tk.wm_title(self, "AutoOrder")
        
        menubar = Menu(self)
        self.config(menu=menubar)
        
        optionsMenu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Options", menu=optionsMenu)
        optionsMenu.add_command(label="Change Login Info", command=lambda:app.show_frame(LoginInfoChange))
        optionsMenu.add_command(label="Quit", command=sys.exit)
        
        
        container = tkinter.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        
        for F in (PartsPage, OrderPage, LoginInfoChange):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame(PartsPage)
        
    def show_frame(self, container):
        frame = self.frames[container]
        frame.tkraise()

        
        
class PartsPage(tkinter.Frame): 
    
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)
        
        validate_cmd = (self.register(checkEntry), '%d', '%P')
        
        entry_array = []
        x = 0
        items = jsonparse.getParts()
        for parts in items:
            partName = ttk.Label(self, text=parts["Description"])
            entryBox = ttk.Entry(self, validate='key', validatecommand=validate_cmd, invalidcommand= 
                                 lambda: messagebox.showinfo("Invalid Entry", "Please enter a valid integer"))
            crmNumber = ttk.Label(self, text=parts["SKU"])
            entry_array.append(entryBox)
            partName.grid(row=x, column=0, padx=2, pady=2)
            entryBox.grid(row=x, column=1, padx=2, pady=2)
            crmNumber.grid(row=x, column=2, padx=2, pady=2)
            x = x + 1
        submitButton = ttk.Button(self, text="Enter Order", command= lambda: filterArray(items, entry_array))
        submitButton.grid(row=x, columnspan=3, padx=2, pady=2)
        
        
        
class OrderPage(tkinter.Frame):
    
    def __init__(self, parent, controller):
        tkinter.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Thanks, Yo")
        label.pack(pady=10,padx=10)
        button = ttk.Button(self, text="new order", command= lambda:controller.show_frame(PartsPage))
        button.pack()
       
        
class LoginInfoChange(tkinter.Frame):
    
    def __init__(self,parent,controller):
        tkinter.Frame.__init__(self,parent)
        usernamelabel = ttk.Label(self, text="New Username:")
        passwordlabel = ttk.Label(self, text = "New Password:")
        usernameEntry = ttk.Entry(self)
        passwordEntry = ttk.Entry(self, show='*')
        
        usernamelabel.grid(row=0, column=0, padx=2, pady=2)
        passwordlabel.grid(row=1, column=0, padx=2, pady=2)
        usernameEntry.grid(row=0, column=1, padx=2, pady=2)
        passwordEntry.grid(row=1, column=1, padx=2, pady=2)
        
        savebtn = ttk.Button(self, text="Save Info", command= lambda:saveInfo(usernameEntry, passwordEntry))
        savebtn.grid(row=2, columnspan=2, padx=2, pady=2)

"""
Function saveInfo
    ARGS:
        username: Entry object containing the input username from LoginInfoChange page
        password: Entry object containing the input password from LoginInfoChange page
    
    Saves username & pw to config file, shows msg box that it is successful, switches back to parts order page
"""
        
def saveInfo(username, password):
    nameconfig.setInfo(username.get(),password.get())
    username.delete(0,'end')
    password.delete(0,'end')
    messagebox.showinfo("Save Successful", "Information Saved Successfully")
    app.show_frame(PartsPage)
                
"""
Function checkEntry
    ARGS:
        text: the contents of the textbox we are vaildating
        
    Returns: 
        true if it is an integer
        false if it is not an integer
"""
        
def checkEntry(action, text):
    if(action == '1'):
        try:
            int(text)
            print("true")
            return True
        except ValueError:
            print("false")
            return False
    return True
    
"""
Function: filterArray
    ARGS:
        items: complete listing of items on given page, from jsonparse
        entry_array: all of the textboxes on the page

    Checks to make sure there is an entry in the textbox:
        textbox empty: do nothing with the item
        textbox has quantity: append to selected_items array as a tuple of the item(0) and its quantity(1)

    Program then passes selected_items to runBrowser to enter onto webpage
    After runBrowser completes - show OrderPage
"""

def filterArray(items, entry_array):
    selected_items = []
    count = 0
    for item in items:
        quantity = entry_array[count].get()
        if quantity != "":
            selected_items.append((item, quantity))
        count = count + 1
    
    for entry in entry_array:
        entry.delete(0, 'end')
    
    placeorder.runBrowser(selected_items)
    app.show_frame(OrderPage)
        

        
"""
Opens window & begins running loop
"""    
        
app = AutoOrder()
app.mainloop()
