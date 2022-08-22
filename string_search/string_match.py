import pandas as pd 
from string_search.kmp import *
from string_search.kmp2 import *
from string_search.ahocorasick import *

import re

def string_match(full_vals, full_vals_col_name , matching_phrase, type="Default", col=None):
    """string_match

    Args:
        full_vals (DataFrame): Input dataframe with all values.
        full_vals_col_name (Str):  Name of the column with items to check for matching.
        matching_phrase (Str): Phrase to check against the full_vals column.

    Returns:
        DataFrame: Dataframe with two new columns:
            - 'match_exist': Boolean value indicating if the matching_phrase was found in the full_vals column.
            - 'match_phrase': String value with the matching_phrase if it was found.
    """
    if type == "BM2":
        pass
    else:
        pass
        #full_vals = full_vals.copy() # copy full_val to avoid mutating it
        #full_vals[full_vals_col_name] = full_vals[full_vals_col_name].str.lower() # lowercase all phrases
        #matching_phrase = matching_phrase.lower() # lowercase all phrases 

    full_vals['match_exist'] = None
    
    if type == "Default":
        full_vals['match_exist'] = full_vals[full_vals_col_name].str.contains(matching_phrase) # 1 Default implementation

    elif type == "KMP1":
        full_vals['match_exist'] = [kmp_v1(str, matching_phrase) for str in full_vals[full_vals_col_name]] # Using KMP from geeksforgeeks - https://www.geeksforgeeks.org/python-program-for-kmp-algorithm-for-pattern-searching-2/
    
    elif type == "KMP2":
        full_vals['match_exist'] = [kmp_v2(str, matching_phrase) for str in full_vals[full_vals_col_name]] # using KMP from John Lekberg - https://johnlekberg.com/blog/2020-11-15-string-search.html
    
    elif type == "BM":
        full_vals['match_exist'] = [(matching_phrase in str) for str in full_vals[full_vals_col_name]] # 2 Using Boyer-Moore - https://stackoverflow.com/questions/12656160/what-are-the-main-differences-between-the-knuth-morris-pratt-and-boyer-moore-sea
    
    elif type == "BM2":
        full_vals['match_exist'] = False if not (matching_phrase in col) else [(matching_phrase in l) for l in full_vals[full_vals_col_name]]
        #full_vals['match_exist'] = False if not (matching_phrase in col) else full_vals[full_vals_col_name].apply(lambda l: (matching_phrase in l))
    
    elif type == "AHOCORASICK":
        full_vals['match_exist'] = using_ahocorasick(pd.Series(full_vals[full_vals_col_name]), matching_phrase) # 3 Using ahocorasick library - https://www.geeksforgeeks.org/python-program-for-kmp-algorithm-for-pattern-searching-2/
    
    full_vals['match_phrase'] = matching_phrase # add matching phrase to the dataframe
    
    return full_vals