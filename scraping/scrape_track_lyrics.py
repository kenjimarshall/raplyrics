# -*- coding: utf-8 -*-
"""
Created on Sun Jul  7 21:28:44 2019

@author: Cheng Lin
"""
import csv
import time
import re
import requests
import sys
from selenium import webdriver
import bs4
from bs4 import BeautifulSoup
import pdb

if __name__ == '__main__':
    input_file_path = sys.argv[1]
    output_folder = sys.argv[2]
    
    #extract song url data
    song_links = []
    with open(input_file_path, encoding='utf-8', mode='r+') as f:
        for line in f:
            song_links.append(line.strip('\n').split(','))
    
    # instantiate selenium browser
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito') # access in incognito
    options.add_argument('--headless')
    
    # create file to hold song meta data
#    with open(output_folder + '/track_meta_data.csv',
#        encoding='utf-8', newline='', mode='w') as f:
#        writer = csv.writer(f)
#        writer.writerow(['song_title_cleaned', 'num_annotated', 
#                         'num_not_annotated', 'num_views'])
    count = 0
    for song in song_links:
        song_title_cleaned = re.sub('[^a-zA-Z_]', '', song[0])
        song_arist_cleaned = re.sub('[^a-zA-Z_]', '', song[1])
        song_file_name = song_title_cleaned + \
                            '_' + song_arist_cleaned + '.csv'
        song_url = song[2]
        
        print('Scraping annotations for: ' + song_file_name)
        print(song_url)
        page_source = requests.get(song_url)
        soup = BeautifulSoup(page_source.content, 'html.parser')
        lyrics = soup.select('div.lyrics')[0].children
        lyrics = [item for item in lyrics][3].children
        lyrics = [item for item in lyrics]
        
        num_annotated = 0
        num_not_annotated = 0
        with open(output_folder + '/lyrics/' + song_file_name, 
            encoding='utf-8', newline='', mode='w') as f:
            writer = csv.writer(f)
            writer.writerow(['line', 'annotated'])
            
            for line in lyrics:
                # if Navigable string contains non-whitespace characters
                if isinstance(line, bs4.element.NavigableString) and \
                        re.sub('\\s', '', line):
                    writer.writerow([line.strip(), 0])
                    num_not_annotated +=1
                
                # if bs4.element.Tag contains text
                if isinstance(line, bs4.element.Tag) and line.get_text():
                    if line.attrs and line.attrs['class']:
                        line_list = re.split('[\\t\\n]', str(line.get_text()))
                        for entry in line_list:
                            writer.writerow([entry, 1])
#                            if isinstance(entry, bs4.element.NavigableString) \
#                                    and re.sub('\\s', '', entry):
#                                writer.writerow([entry.strip(), 1])
#                            if isinstance(entry, bs4.element.Tag) and \
#                                    entry.get_text():
#                                writer.writerow([entry.get_text(), 1])
                            num_annotated +=1
                    else:
                        writer.writerow([line.get_text(), 0])
                        num_not_annotated +=1
        
        print('Scraping track popularity for: ' + song_file_name)
        # scrape track popularity info
        driver = webdriver\
            .Chrome(
                executable_path = r'/mnt/c/Users/Cheng Lin/Documents/3.Coding/Python/raplyrics/scraping/chromedriver.exe',
                options=options)
        driver.get(song_url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        popularity = soup.select(
            'div.header_with_cover_art-metadata_preview-unit')
        popularity = str(popularity[1].get_text().strip())
        
        song_meta_data = [song_title_cleaned, num_annotated,
                          num_not_annotated, popularity]
    
        with open(output_folder + '/track_meta_data.csv',
            encoding='utf-8', newline='', mode='a') as f:
            writer = csv.writer(f)
            writer.writerow(song_meta_data)
        
        driver.quit()
        count +=1
        if count % 20:
            time.sleep(300)
    