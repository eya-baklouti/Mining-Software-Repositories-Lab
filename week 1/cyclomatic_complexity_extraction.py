import lizard

import pandas as pd 

# import extended lizard functions

import lizardsatd


# Define directory path

#Using a static path is wrong here, will imrpove it in the next iteration. SATD ;)

def get_ccn_satd(file_path):  

    df = pd.DataFrame(columns=["method", "CCN", "SATD"])
    new_df = pd.DataFrame(columns=["method", "CCN", "SATD"])
    
    #Getting the list of functions using Lizard as a FIle analyzer. 
    file_analyzer = lizard.FileAnalyzer(lizard.get_extensions([lizardsatd.LizardExtension()]))
    functions = file_analyzer(file_path).function_list

    rows = []
    
    for function in functions:

        #print("Function name:", function.name, "ccn:", function.cyclomatic_complexity, "SATD", function.satd_comments)
        
        #Each function should be coupled with two values, the CCN and SATD.
        rows.append({

        'method': function.name,

        'CCN': function.cyclomatic_complexity,

        'SATD': function.satd_comments

        })
        new_df = pd.DataFrame(rows)
        #print(new_df)

    df = pd.concat([df, new_df], ignore_index=True)
    return df 

#df=get_ccn_satd(file_path)

#df.to_excel('example.xlsx', index=False)
