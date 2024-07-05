import os
import sys

#Here are specified directories and what filetypes they expect
filetypes = {
    "images": ['png', 'jpg', 'jpeg'],
    #adding directories here for safety
    "directories": [""],
    "documents": ['txt', 'doc', 'pdf']
}


def main(contents: list[str], filetypes: dict[str, list[str]]):
    for filetype in filetypes:
        if filetype not in contents:
            os.mkdir(filetype)

    for file_name in contents:
        split_file = file_name.rsplit(".", 1)
        if len(split_file) == 2:
            #since python doesnt have a normal way of getting key from value I iterate over dictionary and
            for dir, type in filetypes.items():
                if split_file[1] in type:
                    dest = dir + "/" + str(file_name)
                    if os.path.exists(dest):
                        sys.stderr.write("file already exists: " + str(dest) +
                                         "\n")
                        break
                    os.rename(file_name, dest)
                    break
        #if its a directory or something like .tar.bz2 or tar.gz it will move them here
        else:
            if file_name not in filetypes:
                os.rename(file_name, 'directories/' + str(file_name))


main(os.listdir(), filetypes)
