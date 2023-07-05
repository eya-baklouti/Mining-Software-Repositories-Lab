import subprocess


def extract_readability_from_file(BASE_PATH, FILE_NAME):
    # Execute the "ls" command and print the output
    result = subprocess.run(['java',
                            '-jar',
                             BASE_PATH+'/rsm.jar',
                             BASE_PATH+'/tmp/'+FILE_NAME],
                            stdout=subprocess.PIPE)
    string_list = result.stdout.decode('utf-8').split('\n')
    number = -1
    if (len(string_list) >= 2):
        string = string_list[2]

    # Split the string by the tab character and take the second element
        if (len(string.split('\t')) >= 2):
            print('File', FILE_NAME, 'readability ', string_list)
            number = string.split('\t')[1]
    return number


print(extract_readability_from_file(
    '/Users/waleeds/Desktop/dev/readability-project', 'TestFile.java'))
