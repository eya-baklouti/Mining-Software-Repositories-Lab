import os
import glob
import shutil
import git





# Clone repository
repo_url = input("Please enter your repository url : ")#"https://github.com/username/repo.git"
repo_dir = input("Please enter your repository directory : ")#"repo"
git.Repo.clone_from(repo_url, repo_dir)



# create output directory
output_dir = input("Please enter your output directory : ")#"output"
if not os.path.exists(output_dir):
    os.mkdir(output_dir)


files_to_extract = []

# traverse the directory tree
for root, dirs, files in os.walk(repo_dir):
    # loop through all the files in the directory
    for file in files:
        # use glob to filter only java files
        if glob.fnmatch.fnmatch(file, '*.java'):
            files_to_extract.append(os.path.join(root, file))

#print(files_to_extract)

for file in files_to_extract:
    #src_path = os.path.join(repo_dir, file)
    src_path =  file
    file_name = os.path.basename(src_path)
    dst_path = os.path.join(output_dir, file_name)
    shutil.copy(src_path, dst_path)



# Clean up cloned repository
shutil.rmtree(repo_dir)
