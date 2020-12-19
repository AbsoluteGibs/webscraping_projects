#DEPENDENCIES/EXTENSIONS/MODULES NEEDED TO RUN:
#-Selenium
#-WebDriver Chrome (for this specific script)

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

import time
import os

dirname = os.path.dirname(__file__) #directory to file excluding the file itself
PATH = os.path.join(dirname, 'chromedriver.exe') #script is in the same folder as the chromedriver executable

driver = webdriver.Chrome(executable_path=PATH)
driver.get("https://youtube.com/") #url to web scrape, in this case - YouTube

time.sleep(2) #give it some time to load the website contents

######################   WORK IN PROGRESS   #################################
#last_height = driver.execute_script("return document.body.scrollHeight")

#while True:
#    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#    driver.execute_script("window.scrollTo(0, 50000);")
#    time.sleep(SCROLL_PAUSE_TIME)
#    new_height = driver.execute_script("return document.body.scrollHeight")
#    if new_height == last_height:
#        break
#    last_height = new_height
############## trying to optimize scrolling mechanic ########################

ASSUMED_END_OF_PAGE = 50

try:
    results = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "content"))) #quits the script when the element is not found within 10s
    main = driver.find_element_by_tag_name("body") #set the top page

    for num in range(0, ASSUMED_END_OF_PAGE):
        main.send_keys(Keys.PAGE_DOWN) #scrolls to bottom of the page to trigger the website's on-demand loading
        time.sleep(2)

    video_items = results.find_elements_by_xpath("\
        //div[@id='details' and @class='style-scope ytd-rich-grid-media']\
        //div[@id='meta' and @class='style-scope ytd-rich-grid-media']\
        //h3[@class='style-scope ytd-rich-grid-media']\
        //a[@id='video-title-link' and @class='yt-simple-endpoint style-scope ytd-rich-grid-media']")

    file = open('dump.html', 'w', encoding='utf-8')
    for video_item in video_items:
        file.write(video_item.get_attribute("title") + "\n")
        file.write(video_item.get_attribute("href") + "\n")
        views_and_datetime = video_item.find_element_by_xpath("//div[@id='metadata-line' and @class='style-scope ytd-video-meta-block']")
        file.write(views_and_datetime.text)
        file.write("\n\n")
    file.close()

finally:
    driver.quit()