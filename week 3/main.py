from pydriller import Repository
from datetime import datetime
import pandas as pd
import os
import fileHandler
import sys
import readabilityHandler

df = pd.DataFrame(columns=["Commit_hash", "author_name", "msg", "author_email", "date",
                  "Number_changed_files", "file_name", "complexity",
                           "readibility_old", "readibility"])
rows = []
repo = "https://github.com/apache/commons-vfs"


to = datetime(2022, 12, 31, 0, 0, 0)

commits = Repository(repo, only_in_branch='master',
                     to=to,
                     only_modifications_with_file_types=['.java']).traverse_commits()

# Define variables needed
commit_hash = ''
commit_msg = ''
author_name = ''
author_email = ''
commiter_date = ''
edited_files_num = ''
file_name = ''
file_nloc = ''
file_complexity = ''
edited_files = ''
file_path = ''
file_readability = ''
file_readability_old = ''
BASE_PATH = os.getcwd()

tmp_file = BASE_PATH+"/tmp"

for commit in commits:

    commit_hash = commit.hash
    commit_msg = commit.msg
    author_name = commit.author.name
    author_email = commit.author.email
    commiter_date = commit.committer_date

    for modified_file in commit.modified_files:
        IS_JAVA = modified_file.filename.endswith(".java")
        if (IS_JAVA):
            edited_files_num = len(commit.modified_files)
            file_name = modified_file.filename
            file_nloc = modified_file.nloc
            file_complexity = modified_file.complexity
            file_complexity_old = ''
            file_path = ''
            file_readability = ''
            file_readability_old = ''

            modified_file.source_code
            # Definitions of intermediate temp variables.
            old_file_values = {}
            HAS_NO_PREV = modified_file.source_code_before == None
            HAS_NO_POST = modified_file.source_code == None
            # To show local progress if the program is runnning.
            print(commit.hash)
            print('HAS_NO_PREV ', HAS_NO_PREV)
            print('HAS_NO_POST', HAS_NO_POST)

            # write the files which will be analysed by lizzard (to test on function level).
            if (not HAS_NO_POST) and (not HAS_NO_PREV):
                new_file = fileHandler.write_file(
                    tmp_file, modified_file.filename, modified_file.source_code)

                old_file = fileHandler.write_file(
                    tmp_file, 'old_'+modified_file.filename, modified_file.source_code_before)

                # Call the function which calculates the cyclomatic complexity value. Will return a DataFrame values of the functions.
                file_readability_old = readabilityHandler.extract_readability_from_file(BASE_PATH,
                                                                                        old_file)
                file_readability = readabilityHandler.extract_readability_from_file(BASE_PATH,
                                                                                    new_file)
                print('file_readability_old', file_readability_old)
                print('file_readability', file_readability)
                rows.append({

                "Commit_hash": commit_hash,
                "author_name": author_name,
                "msg": commit_msg,
                "author_email": author_email,
                "Number_changed_files": edited_files_num,
                "file_name": file_name,
                "complexity": file_complexity,
                "complexity_old": file_complexity_old,
                "readibility_old": file_readability_old,
                "readibility": file_readability
                })

df = pd.DataFrame(rows)
df.to_excel('commons-vfs.xlsx', index=False)
