import os
import re

import pandas as pd
from pydriller import Repository

import cyclomatic_complexity_extraction

folder_name = os.getcwd()+"/tmp"

if not os.path.exists(folder_name):
    os.makedirs(folder_name)
    print(f"Directory {folder_name} created successfully!")
else:
    print(f"Directory {folder_name} already exists.")

results_df = pd.DataFrame(columns=["hash", "file_name", "method_name",
                          "Date", "before_satd", "before_ccn", "after_satd", "after_ccn","commit_message"])

for commit in Repository("https://github.com/apache/commons-vfs").traverse_commits():
    for modified_file in commit.modified_files:

        # Definitions of intermediate temp variables. 
        old_file_values = {}
        HAS_NO_PREV = (modified_file.source_code_before == None)

        # To show local progress if the program is runnning.
        print(commit.hash)

        # write the files which will be analysed by lizzard (to test on function level).
        if ((modified_file.source_code != None) and (re.search(r"\.java$", modified_file.filename)) and (not HAS_NO_PREV)):
            f = open(folder_name+'/'+modified_file.filename, "w")
            f.write(modified_file.source_code)
            f.close()

            #Checking if the previous commit value is available. 
            
            f_old = open(folder_name+'/' +
                             modified_file.filename+'_old', "w")
            f_old.write(modified_file.source_code_before)
            f_old.close()
            
            # Call the function which calculates the cyclomatic complexity value. Will return a DataFrame values of the functions.

            modified_file_df = cyclomatic_complexity_extraction.get_ccn_satd(
                folder_name+'/'+modified_file.filename)
            
            modified_file_old_df = cyclomatic_complexity_extraction.get_ccn_satd(
                folder_name+'/'+modified_file.filename+'_old')
            
        # need to always check if the function has a previous commit
            for index, m in modified_file_old_df.iterrows():
                method = modified_file_old_df['method'][index]
                old_ccn = modified_file_old_df['CCN'][index]
                old_satd = modified_file_old_df['SATD'][index]
                old_file_values[method] = (old_ccn, old_satd)

            # Writing the values for each file,  
            for index, m in modified_file_df.iterrows():
                try:
                    method = modified_file_df['method'][index]
                    ccn = modified_file_df['CCN'][index]
                    satd = modified_file_df['SATD'][index]
                    value_tuple =  old_file_values[method] 
                    old_ccn = value_tuple[0] 
                    old_satd = value_tuple[1] 
                except KeyError:

                    results_df.loc[commit.hash+method] = [commit.hash, modified_file.filename, method,
                                                        'commit.committer_date',  old_satd, old_ccn, satd, ccn,commit.msg]
                    results_df.tail()
                continue

results_df.to_excel('final.xlsx', index=False)
