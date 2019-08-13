# -*- coding: utf-8 -*-
"""
Created on Sun Aug 11 17:48:33 2019

@author: Kenji
"""

import pandas as pd
import numpy as np
import sys, getopt, os
import matplotlib.pyplot as plt



def get_meta_data():
    argv = sys.argv
    print("Arguments: ", argv)
    opts, args = getopt.getopt(argv[1:],"hi:")
    csv_name = ""
    output_file = ""
    for opt, arg in opts:
        print(opt, arg, type(arg))
        
        if opt == "-i":
            if os.path.exists(arg):
                csv_name = arg          
            else:
                sys.exit("input file not found")
        else:
            sys.exit("get_stats_from_csv.py -i <inputfile>")
    print("Input file: " + csv_name)
    return csv_name

if __name__ == '__main__':
    csv_name = get_meta_data()
    print("Loading data...")
    meta_data = pd.read_csv(csv_name)
    print(meta_data.head(5))
    meta_data['percent_annotated'] = (meta_data['num_annotated'] / 
             (meta_data['num_annotated'] + meta_data['num_not_annotated']))   
     
    meta_data['num_views_numeric'] = 0
    for index, views in enumerate(meta_data['num_views']):
        if views[-1] == 'M':
            meta_data['num_views_numeric'][index] = float(views[:-1]) * 1000000
        elif views[-1] == 'K':
            meta_data['num_views_numeric'][index] = float(views[:-1]) * 1000
    plt.figure()
    plt.scatter(np.log(meta_data['num_views_numeric']), meta_data['percent_annotated'],
                alpha = 0.8, edgecolor = 'none', s = 15)
    plt.title("% Annotated vs. log(# Views)")
    plt.xlabel("log(# Views)")
    plt.ylabel("% Annotated")
    plt.savefig('percent_annotated_vs_log_views.png', bbox_inches = 'tight')
    
    num_songs = len(meta_data['num_annotated'])
    total_annotated = sum(meta_data['num_annotated'])
    total_not_annotated = sum(meta_data['num_not_annotated'])
    total_percent_annotated = total_annotated / (total_not_annotated + total_annotated)
    total_sub_ten_percent = sum(i < 0.1 for i in meta_data['percent_annotated'])
    total_sub_five_percent = sum(i < 0.05 for i in meta_data['percent_annotated'])
    total_sub_one_percent = sum(i < 0.01 for i in meta_data['percent_annotated'])
    
    plt.figure()
    [n, bin_edges, __] = plt.hist(meta_data['percent_annotated'], bins = 20)
    plt.ylabel('# of Songs')
    plt.xlabel('% Annotated')
    plt.title('% Annotated Histogram')
    plt.savefig('percent_annotated_histogram.png', bbox_inches = 'tight')
    
    hist_dict = {'num_songs': n, 'lower_bin_edge': bin_edges[:-1]}
    hist_df = pd.DataFrame(hist_dict)
    hist_df.to_csv('hist_data.csv')
    
    stat_str = ("\nTotal Lines Annotated: " + str(total_annotated) +
          "\nTotal Not Annotated: " + str(total_not_annotated) +
          "\n% Annotated Overall: " + str(100 * total_percent_annotated) +
          "\n\nTotal Songs: " + str(num_songs) +
          "\nTotal Annotated < 10%: " + str(total_sub_ten_percent) +
          "\nTotal Annotated < 5%: " + str(total_sub_five_percent) +
          "\nTotal Annotated < 1%: " + str(total_sub_one_percent) +
          "\n% Annotated < 10%: " + str(100 * total_sub_ten_percent / num_songs) +
          "\n% Annotated < 5%: " + str(100 * total_sub_five_percent / num_songs) +
          "\n% Annotated < 1%: " + str(100 * total_sub_one_percent / num_songs))
    
    print(stat_str)
    
    with open("total_stats.txt", "w") as text_file:
        text_file.write(stat_str)
    
    meta_data.to_csv("meta_data_expanded.csv")
    
    