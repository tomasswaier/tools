import requests
from write_into_folder import write 
from bs4 import BeautifulSoup
#opens website.html in bs4
def lookup(name):
  url_text=name
  url=("https://emojicombos.com/"+url_text)
  page=requests.get(url)
  soup = BeautifulSoup(page.text, 'html.parser')
  #finds everything with pre tag and prints it out
  for line in soup.find_all('div'):
    tag=line.div
    if tag is not None and 'data-type' in tag.attrs:
      if('dot_art' in tag['data-type']): 
        print(tag.text)
        write(1,tag.text) 
  #print(tag.text)

