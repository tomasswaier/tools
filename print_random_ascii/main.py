from re import search
import sys
import os
import random
from search import lookup
from write_into_folder import write


def main():
    # if the user inputs in wrong nu,ner pf args then it will kick him out
    if len(sys.argv) < 2:
        print(
            "Usage:\nCall compiled code with 2 arguemnts 'Python3 ./main.py <Direcotry_name> <argumnt>'\nDirectory name can be anything you want for example if I wanted to store cat images I'd name it cats\nargument can be either -w (write) or -r (print random image)\n(if the directory doesnt exist then it will create one so for example ./main.py uwu -w will create a dir and prompt u to write in ascii art)"
        )

        print("call this function with specified directory \nexisting direcotories:")

        path = os.path.dirname(os.path.abspath(__file__))
        list = os.listdir(path + "/images")
        print(list)
        exit()
    # we get path wehere we're currently . i didnt read niether os nor sys lib very much so if there is better way lemme know pls

    path = os.path.dirname(os.path.abspath(__file__))
    contents = os.listdir(path)
    contents.remove("description.txt")

    list = os.listdir(path + "/images")
    try:
        position = list.index(sys.argv[1])
    except ValueError:
        position = -1

    if position != -1:
        print("")
    else:
        os.chdir(path + "/images")
        os.mkdir(sys.argv[1])
        if len(sys.argv) < 3 or sys.argv[2] != "-w":
            print(
                "Direcotry initiated.\nPlease use <Direcotry_name> -w to write in images"
            )
            exit()
    if len(sys.argv) < 3:
        print(
            "Arguments:\n-w :will prompt you to paste in your image\n-r :will print random image from that directory\n-l: will look up images and paste them into said direcotry"
        )
        exit()

    image_list = os.listdir(path + "/images/" + sys.argv[1])
    # adawd

    match (sys.argv[2]):
        case "-r":
            image_count = len(image_list)
            random_number = random.randrange(image_count)
            with open(
                path + "/images/" + sys.argv[1] + "/" + image_list[random_number], "r"
            ) as f:
                image = f.readlines()
            for line in image:
                print(line.strip())
        case "-w":
            write(0, "")
        case "-l":
            lookup(sys.argv[1])


main()
