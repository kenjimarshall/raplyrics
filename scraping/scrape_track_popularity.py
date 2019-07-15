# -*- coding: utf-8 -*-
"""
Created on Sun Jul 14 21:16:38 2019

@author: Cheng Lin
"""

import csv
import time
import re
import requests
import sys
import bs4
from bs4 import BeautifulSoup
import pdb

if __name__ == '__main__':
    input_file_path = sys.argv[1]
    output_folder = sys.argv[2]