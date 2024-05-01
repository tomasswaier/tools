import sys
import os
import random
list=os.listdir("images")
image_count=len(list)
if(len(sys.argv)==1):
  random_number=random.randrange(image_count)
  with open('images/' + list[random_number], 'r') as f:
      image = f.readlines()
  for line in image:
      print(line.strip())
  exit()   
match (sys.argv[1]):
  case "-r":
    random_number=random.randrange(image_count)
    with open('images/' + list[random_number], 'r') as f:
        image = f.readlines()
    for line in image:
        print(line.strip())
  case "-w":
    file_name=''
    if(image_count>999):
      print("MAX NUMBER OF IMAGES REACHED")
      exit()
    if(image_count>99):
      file_name=str(image_count+1)+".txt"
    elif(image_count<100):
      file_name="0"+str(image_count+1)+".txt"
    f =open("images/"+file_name,"w")
    print("Writing additional image:")
    try:
      while(True):
        x=str(input()+'\n')
        if(x==''):
          break
        f.write(x)
    except EOFError:
      print("image has been written")

      
