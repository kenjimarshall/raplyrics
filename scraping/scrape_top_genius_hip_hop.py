# -*- coding: utf-8 -*-
"""
Created on Sun Jul  7 20:27:05 2019

@author: Cheng Lin
"""
import csv
import time
import re
import sys
from selenium import webdriver
from bs4 import BeautifulSoup


if __name__ == '__main__':
    output_file_path = sys.argv[1]
    
    # instantiate selenium browser
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito') # access in incognito
    options.add_argument('--headless')
    driver = webdriver\
        .Chrome(
                executable_path = r'/mnt/c/Users/Cheng Lin/Documents/3.Coding/Python/raplyrics/scraping/chromedriver.exe',
                options=options)

    MAIN_SITE_URL = 'https://genius.com/tags/hip-hop/all?fbclid=IwAR3tDMKzFgC0ljuLTpl1mO1hWuKxplEgf4brapYV7oC14QX_sPL1_Anak4U'
    driver.get(MAIN_SITE_URL)
    
    with open(output_file_path, 
              encoding='utf-8', newline='', mode='w') as f:
        writer = csv.writer(f)
        
        # click the "more" button multiple times to load more songs
        print('------------populate page with songs------------')
        for x in range(0,50):
            print('populate page iteration ' + str(x))
            more_button = driver.find_element_by_css_selector("a.more.button")
            if more_button:
                more_button.click()
            else:
                break
            time.sleep(5)

        # use bs4 to parse the rendered page
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        songs = soup.select('a.song_link', href=True)
        
        print('------------collecting song links------------')
        for song in songs:
            # get and clean song title
            song_title = song.select('span.song_title')[0]\
                .get_text().strip()
            song_title = re.sub('\\s', '_', song_title)
            print(song_title)
            #get author
            song_artist = song.select('span.primary_artist_name')[0]\
                .get_text().strip()
            song_artist = re.sub('\\s', '_', song_artist)
            # get URL
            song_URL = song['href']
            
            # write to file
            writer.writerow([song_title, song_author, song_URL])
            
    driver.quit()
