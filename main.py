import time
import pandas as pd 

from string_search.string_match import string_match

import os
import numpy as np
from subprocess import Popen, STDOUT, PIPE

def job_cpp(n_patt, n_text):
    p = Popen(["./main"], stdout=PIPE, stdin=PIPE, stderr=STDOUT, bufsize=1, universal_newlines=True)

    out,err = p.communicate()
    mtx = np.array([c=='1' for c in out]).reshape(n_patt, n_text)
    return mtx

def job(input, match):
    col = ";".join(list(input["Keyword"].str.lower()))
    input['Keyword'] = input["Keyword"].str.lower()
    match['match'] = match['match'].str.lower()

    #DEFAULT IMPLEMENTATION
    start_time = time.time()
    matching_phrases = [string_match(input, 'Keyword', i) for i in match['match']]
    end_time = time.time()
    print("Default implementation: {}".format(end_time - start_time))
    
    df = pd.concat(matching_phrases)
    print("Default implementation shape: {}".format(df.shape))

    # BOYER-MOORE - https://stackoverflow.com/questions/12656160/what-are-the-main-differences-between-the-knuth-morris-pratt-and-boyer-moore-sea
    start_time = time.time()
    matching_phrases = [string_match(input, 'Keyword', i, type="BM") for i in match['match']]
    end_time = time.time()
    print("Boyer-Moore: {}".format(end_time - start_time))
    
    df = pd.concat(matching_phrases)
    print("Boyer-Moore shape: {}".format(df.shape))

    # === Collect col ===
    start_time = time.time()
    matching_phrases = [string_match(input, 'Keyword', i, type="BM2", col=col) for i in match['match']]
    end_time = time.time()
    print("Boyer-Moore 2: {}".format(end_time - start_time))
    
    df = pd.concat(matching_phrases)
    print("Boyer-Moore 2 shape: {}".format(df.shape))

    # === C++ ===
    start_time = time.time()
    mtx = job_cpp(len(match), len(input))
    end_time = time.time()
    print("C++: {}".format(end_time - start_time))

    # The computaion is done, this is only to collect the pandas object [this part is quite slow... ]
    matching_phrases = [input.assign(match_exist=mtx[i], match_phrase=match['match'][i]) for i in range(len(match['match']))]
    df = pd.concat(matching_phrases)
    print("C++ shape: {}".format(df.shape))
    
    # AHOCORASICK - https://pypi.org/project/pyahocorasick/
    start_time = time.time()
    matching_phrases = [string_match(input, 'Keyword', i, type="AHOCORASICK") for i in match['match']]
    end_time = time.time()
    print("AHOCORASICK: {}".format(end_time - start_time))

    df = pd.concat(matching_phrases)
    print("AHOCORASICK shape: {}".format(df.shape))

    # KPM VERSION 1 - https://www.geeksforgeeks.org/python-program-for-kmp-algorithm-for-pattern-searching-2/ 
    start_time = time.time()
    matching_phrases = [string_match(input, 'Keyword', i, type="KMP1") for i in match['match']]
    end_time = time.time()
    print("KMP version 1: {}".format(end_time - start_time))
    
    df = pd.concat(matching_phrases)
    print("KPM1 shape: {}".format(df.shape))
    
    # all_data = pd.concat(matching_phases) # concat to get single dataframe
    # match_exist = all_data[all_data['match_exist'] == True] # get rows where match_exist is true
    
    # return match_exist, all_data


if __name__ == '__main__':
    input = pd.read_csv('string_search/test_files/3q_semrush.csv')
    match = pd.read_csv('string_search/test_files/3q_test_bigrams.csv')

    # match_exist, all_data = job(input, match)
    job(input, match)
