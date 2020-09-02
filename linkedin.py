import os, random, time, sys
from selenium import webdriver
from bs4 import BeautifulSoup
from pymongo import MongoClient
browser=webdriver.Chrome("C:\\Users\\EDS\\Desktop\\chromedriver.exe")
browser.get("https://www.linkedin.com/jobs/")
# if you want to search about design
element=browser.find_element_by_name('keywords').send_keys('design')
browser.find_element_by_name('location').clear()
# if the location is in france
element=browser.find_element_by_name('location').send_keys('France')
browser.find_element_by_id("JOBS").submit()
last_height = browser.execute_script("return document.body.scrollHeight")
while True:
    # Scroll down to bottom
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
    time.sleep(2)

        # Calculate new scroll height and compare with last scroll height
    new_height = browser.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        if(browser.find_element_by_xpath("//button[@data-tracking-control-name='infinite-scroller_show-more']")is not None):
            last_height1 = browser.execute_script("return document.body.scrollHeight")
            browser.find_element_by_xpath("//button[@data-tracking-control-name='infinite-scroller_show-more']").click()
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            new_height1 = browser.execute_script("return document.body.scrollHeight")
            if new_height1 == last_height1:
                break

        else:
            # If heights are the same it will exit the function
            break
    last_height = new_height   
try: 
    conn = MongoClient() 
    print("Connected successfully!!!") 
except:   
    print("Could not connect to MongoDB")
# the database of mongodb is called linkedin
db = conn.linkedin 
# the collection is jobs
collection = db.jobs

src=browser.page_source
soup=BeautifulSoup(src,'lxml')
div=soup.find_all('div',{'class':'result-card__contents job-result-card__contents'})

for i in div:
    try:
        dict =
{"job":i.find('h3').get_text().strip(),
 "company":i.find('a').get_text().strip(),
 "place":i.find('span').get_text().strip(),
 "time":i.find('time').get_text().strip(),"contact":i.find('a')['href']}
        #print(dict)
        collection.insert_one(dict)
        #print("/*******************************************/")
    except: 
        continue