# -*- coding: utf-8 -*-
"""
Created on Mon Sep  4 19:10:28 2017

@author: madhu
"""

from selenium import webdriver
from selenium import common
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.action_chains import ActionChains

import time

driver = webdriver.Chrome('/Users/madhu/Downloads/chromedriver')

document = driver.get("https://web.whatsapp.com/")
wait = WebDriverWait(driver, 20)

#with open('Know your IITB alumni association -) (Responses) - List of trek enthu.csv') as f:
with open('Korigad trek enthu remaining list - Sheet1.csv') as f:
    for line in f:
        lis = line.strip().split(',')
        target = '"'+lis[0] + " AA Trek Enthusiast"+'"'
#        target = '"'+lis[0]+'"'
        name  = lis[0]
        string = \
        """Hi """+name+","
        
        _search_arg = '//button[@class="icon icon-search-morph"]'
        _search = wait.until(EC.presence_of_element_located((
            By.XPATH, _search_arg)))
        _search.click()
        
        
        search_pre = '//input[@type="text"][@dir="auto"][@data-tab="2"]'    
        search_pre_box = wait.until(EC.presence_of_element_located((
            By.XPATH, search_pre)))

        try:
                            
            search_pre_box.send_keys(eval(target))
            #search_pre_box.send_keys("Aditya Dutta")
            #class="empty empty-top"
            
            #inp_xpath = '//div[@class="input"][@dir="auto"][@data-tab="1"]'
            inp_xpath = '//span[@class="matched-text"]'
            input_box = wait.until(EC.presence_of_element_located((
                By.XPATH, inp_xpath)))
            input_box.click()   
            
            msg_xpath = '//div[@class="input"][@dir="auto"][@data-tab="1"]'
            msg_box = wait.until(EC.presence_of_element_located((
                By.XPATH, msg_xpath)))
           # selectAll = Keys.chord(Keys.SHIFT,Keys.ENTER);
            #driver.findElement(By.tagName("html")).sendKeys(selectAll);    
            msg_box.send_keys(string) 
            ActionChains(driver).key_down(Keys.SHIFT).send_keys(Keys.ENTER).key_up(Keys.SHIFT).perform()
            ActionChains(driver).key_down(Keys.SHIFT).send_keys(Keys.ENTER).key_up(Keys.SHIFT).perform()
            msg_box.send_keys("""This is Madhu Lekha from IITBAA - Mumbai Chapter Executive Committee. I'm sending this across as you've expressed interest in a trek and haven't registered yet for the upcoming one. In case you missed out on the mail, here's the form -> https://goo.gl/xH6tNY and the poster.""")
            ActionChains(driver).key_down(Keys.SHIFT).send_keys(Keys.ENTER).key_up(Keys.SHIFT).perform()
            ActionChains(driver).key_down(Keys.SHIFT).send_keys(Keys.ENTER).key_up(Keys.SHIFT).perform()
            msg_box.send_keys("""Hope to see u on Saturday.""")
            ActionChains(driver).key_down(Keys.SHIFT).send_keys(Keys.ENTER).key_up(Keys.SHIFT).perform()
            msg_box.send_keys("Cheers !")    
            ActionChains(driver).key_down(Keys.SHIFT).send_keys(Keys.ENTER).key_up(Keys.SHIFT).perform()
            ActionChains(driver).key_down(Keys.SHIFT).send_keys(Keys.ENTER).key_up(Keys.SHIFT).perform()
            msg_box.send_keys("P. S : It's a beginner's trek - Beautiful, totally safe and doable by all. We can look into forming groups going ahead for more challenging and regular ones :)" + Keys.ENTER)
        
        
            time.sleep(10)
        except:
            
            print("failed "+name)
            pass