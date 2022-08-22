import pandas as pd 
from string_search.kmp import *
from string_search.kmp2 import *
from string_search.ahocorasick import *

import re

def string_match(full_vals, full_vals_col_name , matching_phrase, all_vals, type="Default"):
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

    full_vals['match_exist'] = None
    
    if type == "Default":
        if matching_phrase in all_vals: # If the matching_phrase is in list of all values, then check for matches
            full_vals['match_exist'] = full_vals[full_vals_col_name].str.contains(matching_phrase) # 1 Default implementation
        else:
            full_vals['match_exist'] = False
            
    elif type == "KMP1": # Using KMP from geeksforgeeks - https://www.geeksforgeeks.org/python-program-for-kmp-algorithm-for-pattern-searching-2/
        if matching_phrase in all_vals: # If the matching_phrase is in list of all values, then check for matches
            full_vals['match_exist'] = [kmp_v1(str, matching_phrase) for str in full_vals[full_vals_col_name]] 
        else:
            full_vals['match_exist'] = False
    
    elif type == "BM": # Using Boyer-Moore - https://stackoverflow.com/questions/12656160/what-are-the-main-differences-between-the-knuth-morris-pratt-and-boyer-moore-sea    
        if matching_phrase in all_vals: # If the matching_phrase is in list of all values, then check for matches
            full_vals['match_exist'] = [(matching_phrase in l) for l in full_vals[full_vals_col_name]]
            
        else: # If the matching_phrase is not in list of all values, then set all values to False
            full_vals['match_exist'] = False
    
    elif type == "AHOCORASICK":
        if matching_phrase in all_vals: # If the matching_phrase is in list of all values, then check for matches
            full_vals['match_exist'] = using_ahocorasick(pd.Series(full_vals[full_vals_col_name]), matching_phrase) # 3 Using ahocorasick library - https://www.geeksforgeeks.org/python-program-for-kmp-algorithm-for-pattern-searching-2/
        else:
            full_vals['match_exist'] = False

    full_vals['match_phrase'] = matching_phrase # add matching phrase to the dataframe

    return full_vals