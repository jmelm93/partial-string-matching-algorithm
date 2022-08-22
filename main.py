import time
import pandas as pd 

from string_search.string_match import string_match

import os
import numpy as np
from subprocess import Popen, STDOUT, PIPE


def job_cpp(n_patt, n_text):
    # os.system("g++ job.cpp -o job.exe") # compile C++ program
    # only do this once when actual application deploys. Don't need to compile every time the application is run.
    
    p = Popen(["./job.exe"], stdout=PIPE, stdin=PIPE, stderr=STDOUT, bufsize=1, universal_newlines=True) # run C++ program

    out,err = p.communicate() # get output from C++ program
    
    mtx = np.array([c=='1' for c in out]).reshape(n_patt, n_text) # convert output to numpy array
    
    return mtx


def job(input, match):
    input['Keyword'] = input["Keyword"].str.lower()
    match['match'] = match['match'].str.lower()
    all_vals = ";".join(list(input["Keyword"].str.lower()))
    
    #DEFAULT IMPLEMENTATION
    start_time = time.time()
    matching_phrases = [string_match(input, 'Keyword', i, all_vals=all_vals) for i in match['match']]
    end_time = time.time()
    df = pd.concat(matching_phrases)
    df_match_true = df[df['match_exist']==True]
    print(f"Default implementation: \n Time: {end_time - start_time} \n Shape full df: {df.shape} \n Shape of matching phrases: {df_match_true.shape}")
    
    #BOYER-MOORE - https://stackoverflow.com/questions/12656160/what-are-the-main-differences-between-the-knuth-morris-pratt-and-boyer-moore-sea
    start_time = time.time()
    matching_phrases = [string_match(input, 'Keyword', i, type="BM", all_vals=all_vals) for i in match['match']]
    end_time = time.time()
    df = pd.concat(matching_phrases)
    df_match_true = df[df['match_exist']==True]
    print(f"Boyer-Moore: \n Time: {end_time - start_time} \n Shape full df: {df.shape} \n Shape of matching phrases: {df_match_true.shape}")
    
    #C++
    start_time = time.time()
    mtx = job_cpp(len(match), len(input))
    end_time = time.time()
    matching_phrases = [input.assign(match_exist=mtx[i], match_phrase=match['match'][i]) for i in range(len(match['match']))] # The computaion is done, this is only to collect the pandas object [this part is quite slow... ]
    df = pd.concat(matching_phrases)
    df_match_true = df[df['match_exist']==True]
    print(f"C++: \n Time: {end_time - start_time} \n Shape full df: {df.shape} \n Shape of matching phrases: {df_match_true.shape}")

    # AHOCORASICK - https://pypi.org/project/pyahocorasick/
    start_time = time.time()
    matching_phrases = [string_match(input, 'Keyword', i, type="AHOCORASICK", all_vals=all_vals) for i in match['match']]
    end_time = time.time()
    df = pd.concat(matching_phrases)
    df_match_true = df[df['match_exist']==True]
    print(f"AHOCORASICK: \n Time: {end_time - start_time} \n Shape full df: {df.shape} \n Shape of matching phrases: {df_match_true.shape}")

if __name__ == '__main__':
    input = pd.read_csv('string_search/test_files/3q_semrush.csv')
    match = pd.read_csv('string_search/test_files/3q_test_bigrams.csv')

    # match_exist, all_data = job(input, match)
    job(input, match)
