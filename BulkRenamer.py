import os
import re



def rename_file(directory, pattern, newname):
    files = os.listdir(directory)
    counter = 0
    for file in files:
        if re.match(pattern, file):
            filetype = file.split('.')[-1]
            os.rename(directory + '/' + file, directory + '/' + newname + str(counter) + '.' + filetype)
            print("Renaming " + file + " to " + newname + str(counter) + "." + filetype )
            counter += 1



#rename_file("C:\\Users\\RichardOjok\\Desktop\\TestDir", "my.*", "Success")

#rename_file("C:\\Users\\RichardOjokPriorityO\\Desktop\\TestDir", ".*\.txt", "Successstory")

rename_file("C:\\Users\\RichardOjokPriorityO\\Desktop\\TestDir", ".*[0-9].*", "number")