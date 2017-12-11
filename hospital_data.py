#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 17:57:13 2017

@author: madhu
"""

from selenium import webdriver
from bs4 import BeautifulSoup
import time
import re
import pandas as pd
from multiprocessing import Pool, cpu_count

def get_data(url):
    browser = webdriver.Firefox(executable_path='/home/madhu/Downloads/geckodriver')
    browser.get(url)
    print('Processing for url\n%s'%(url))
    time.sleep(1)
    source = browser.page_source
    soup = BeautifulSoup(source, 'html.parser')
    reqd = soup.find(id="ajax-content").find('div',{'class':["view-content"]}).find_all('div')
    
    out = []
    
    for doc in reqd:
        try:
            if 'views-row' in doc.get('class'):
           #    print(i.get('class'))  
               doc_name = doc.h3.get_text()
               basic_info = doc.find_all('p')
               for j in basic_info:
                   try:
                       if 'designation' in j.get('class'):
                           #print(j.get_text())
                           designation = j.get_text()
                   except:
                       pass
                   try:
                       if 'qualification' in j.get('class'):
                           #print(j.get_text())
                           qualification = j.get_text()
                   except:
                       pass
                   try:
                       if 'specialities' in j.get('class'):
                           #print(j.get_text())
                           location = j.get_text().split()[-1]
                   except:
                       pass
                   try:
                       if 'location' in j.get('class'):
                           #print(j.get_text())
                           speciality = j.get_text()
                   except:
                       pass
                   
               detail_link = doc.find_all('div',{'class':"readmore"})[-1].find('a',href=True).attrs['href']
               details_url = 'http://india.columbiaasia.com'+detail_link
               browser1 = webdriver.Firefox(executable_path='/home/madhu/Downloads/geckodriver')
               browser1.get(details_url)
               time.sleep(1)
               source_detail = browser1.page_source
               soup_detail = BeautifulSoup(source_detail,'html.parser')
               profile_details = ""
               profile = soup_detail.find('div',{'class':"doctorsDetails"}).find('div',{'class':"docProfile"}).find_all('p')
               try:
                   for t in profile:
                       profile_details = profile_details + re.sub(u'\xa0','',t.get_text())
               except:
                   profile_details = ""
               try:
                   background = soup_detail.find('div',{'class':"editor"}).find_all('h3',{'class':"background"})
                   try:
                       speciality_details = background[0].find_next().get_text('\n')
                   except:
                       speciality_details=""
                   try:    
                       experience = background[1].find_next().get_text('\n')
                   except:
                       experience = ""
                   try:    
                       experience_details = re.sub(u'\xa0','',background[1].find_next().find_next().get_text('\n'))
                   except:
                       experience_details = ""
               except:
                   pass   
               browser1.quit()      
    
                   
           
        except:
            pass
        out.append({'Doctor':doc_name, 'Designation':designation, 'Qualification':qualification,\
                    'Location':location, 'Speciality':speciality, \
                    'speciality_details':speciality_details,'experience':experience,\
                    'experience_details':experience_details})
    browser.quit() 
    return out

pool = Pool(processes = cpu_count())


cities_pages = [('yeshwanthpur',20),('hebbal',14),('whitefield',19)]
#('yeshwanthpur',20),('ahmedabad',11),('doddaballapur',3),('ghaziabad',7),('hebbal',14),('kolkata',21)

urls = []

for city, num in cities_pages:
    for i in range(num):
        urls.append('http://india.columbiaasia.com/hospitals/%s/doctors?page=%d'%(city.lower(),i))

out = pool.map(get_data, urls)
out = pd.DataFrame(out)
out = out.drop_duplicates('Doctor')

out.to_csv('colombia_asia.csv', index = False)