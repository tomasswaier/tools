import os


#checks for dirs and files with similar names
def dir_check(contents, filetypes):
    #function checks if there are files inside the directories that have the same name
    def check_insides(name):
        subdir = os.listdir(name)
        for file in contents:
            if file in subdir:
                print('cant sort:' + file)
                contents.remove(file)

    #checks if directory exists and if yest then
    for filetype in filetypes:
        if filetype in contents:
            check_insides(filetype)
        else:
            os.mkdir(filetype)

    return contents


def move(contents, filetypes):

    for file_name in contents:
        split_file = file_name.rsplit(".", 1)
        if len(split_file) == 2:
            #since python doesnt have a normal way of getting key from value I iterate over dictionary and
            for dir, type in filetypes.items():
                if split_file[1] in type:
                    os.rename(file_name, dir + "/" + str(file_name))
                    break
        #if its a directory or something like .tar.bz2 or tar.gz it will move them here
        else:
            if file_name not in filetypes:
                os.rename(file_name, 'directories/' + str(file_name))


def main(contents, filetypes):
    #creates list of images to move
    contetns = dir_check(contents, filetypes)
    #moves images
    move(contents, filetypes)


filetypes = {
    "images": ['png', 'jpg', 'jpeg'],
    #adding directories here for safety
    "directories": [""],
    "documents": ['txt', 'doc', 'pdf']
}
main(os.listdir(), filetypes)
