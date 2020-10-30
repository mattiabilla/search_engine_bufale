# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 15:23:07 2020

@author: Mattia
"""

import requests
from bs4 import BeautifulSoup
f=open("links.txt","w")
for i in range(1,15):
    
    URL="https://www.butac.it/category/bufala/page/"+str(i)+"/"
    
    print()
    print(URL)
    print()
    
    page = requests.get(URL, headers={"User-Agent":"Mozilla/5.0"})
    
    soup = BeautifulSoup(page.content, "html.parser")
    
   
   
    results=soup.find(class_="td-main-content-wrap td-container-wrap").find_all('a', class_='td-image-wrap')
    
    
    
    for result in results:
        #print(result)
        print(result.get("href"))
        f.write(result.get("href"))
        f.write("\n")

f.close()