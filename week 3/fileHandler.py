def write_file(folder_name, file_name, source_code):

    f = open(folder_name+'/'+file_name, "w")
    f.write(source_code)
    f.close()
    print(file_name)
    return file_name
