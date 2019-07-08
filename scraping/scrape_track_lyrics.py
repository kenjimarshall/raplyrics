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
from bs4 import BeautifulSoup

if __name__ == '__main__':
    input_file_path = sys.argv[1]
    output_folder = sys.argv[2]
    
    #extract song meta data
    song_links = []
    with open(input_file_path, encoding='utf-8', mode='r+') as f:
        for line in f:
            song_links.append(line.strip('\n').split(','))
    
    for song in song_links:
        song_title_cleaned = re.sub('[^a-zA-Z_]', '', song[0])
        song_arist_cleaned = re.sub('[^a-zA-Z_]', '', song[1])
        song_file_name = song_title_cleaned + '_' + \
                            song_arist_cleaned + '.txt'
        print(song_file_name)
        
        with open(output_folder + '/' + song_file_name, 
            encoding='utf-8', newline='', mode='w') as f:
            writer = csv.writer(f)
