# Mining-Software-Repositories-Lab Group 10

1. Checkout a repository1 to a local folder as a test.
2. Create a Python script which lists the Java files of the repository.
3. Use Lizard2 to extract cyclomatic complexity for the methods of each file.
4. Include our provided plugin for extracting SATD comments within methods3. It uses the patterns provided in previous research4.
5. Extend the Python script so that it uses the plugin and you can extract cyclomatic complexity, name and SATD comments for each method from a file.

## Tuesday
1. After you have your group, create a private Gitlab Repository5 for your group for the week and invite the lecturer.
2. Extend the Python script so that you can run it over all commits of a repository using PyDriller. Include for each file before and after versions as done in the first week. Match the methods in the before and after versions of the file to get the before and after cyclomatic complexity as well as SATD comments for each method.
Hint: If a match between a before and after method cannot be found, drop it from the results.
Required: Only collect the methods which have changed in the commit.
3. Extend the Python script so that you match the patterns also on the commit message. You can include this as boolean feature, i.e., whether the commit message also contained SATD.
Required: Include also the commit hash in the data so that you can distinguish between commits in the analysis later.
4. Your Python script should be able to take a repository URL, clone the repository and traverse over all commits. For each modified (not added, deleted, copied) Java file extract all methods, as well as before and after cyclomatic complexity and before and after SATD comments.
5. Make sure to extract to a format which you can later analyze.
6. Extract at least the changes of commons-net6, commons-compress7, commons-vfs8 and
commons-codec9.
