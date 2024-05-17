
import sys
import os
def write(option, text):

  path=os.path.dirname(os.path.abspath(__file__))
  image_list=os.listdir(path+'/images/'+sys.argv[1])
  image_count=len(image_list)
  image_count=len(image_list)
  file_name=''
  if(image_count>999):
    print("MAX NUMBER OF IMAGES REACHED")
    exit()
  if(image_count>99):
    file_name=str(image_count+1)+".txt"
  elif(image_count<10):
    file_name="00"+str(image_count+1)+".txt"
  elif(image_count<100):
    file_name="0"+str(image_count+1)+".txt"
  f =open(path+"/images/"+sys.argv[1]+"/"+file_name,"w")
  if(option==0):
    print("Writing additional image:")
    try:
      while(True):
        x=str(input()+'\n')
        if(x==''):
          break
        f.write(x)
    except EOFError:
      print("image has been written")
  elif option==1:
    f.write(text)
