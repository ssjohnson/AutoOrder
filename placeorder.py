from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import nameconfig

"""
Function: runBrowser
    Args: 
        selected_items: array of tuples (json element, quantity ordered)
    
    Opens & Maximizes Chrome
    Opens "bel-aqua.com"
    Logs in using info from separate log in info file (nameconfig.py)
    Fills out quick order pad using info from tuples
        quick order pad only allows 5 items at a time, loop keeps counter, submits with 5 entries, then starts again
    Leaves user to validate entries & checkout
"""

def runBrowser(selected_items):
    
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://www.bel-aqua.com")

    # Login into BA.com
    loginInfo = nameconfig.getInfo()
    driver.find_element_by_id("txtEmail").send_keys(loginInfo[0])
    driver.find_element_by_id("txtPassword").send_keys(loginInfo[1])
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

