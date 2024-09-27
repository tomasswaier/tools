from bs4 import BeautifulSoup
import requests


champion = "Vladimir"
champion = "patch-" + champion.lower()
url = "https://www.leagueoflegends.com/en-pl/news/game-updates/"
page = requests.get(url)
soup = BeautifulSoup(page.text, "html.parser")
last_patch = []
for element in soup.find_all("div"):
    if element.find("div", class_="sc-ce9b75fd-0 lmZfRs"):
        text = element.find("div", class_="sc-ce9b75fd-0 lmZfRs").get_text()
        if text.split()[0] == "Patch":
            newtext = text.replace(".", " ")
            last_patch = newtext.split()
            break


last_patch = "-".join(str(word).lower() for word in last_patch)
url += last_patch + "/"
page = requests.get(url)
soup = BeautifulSoup(page.text, "html.parser")
last_patch = []
changes = ""
for element in soup.find_all("div"):
    if element.has_attr("class") and element["class"][0] == "patch-change-block":
        if element.find("h3", {"id": champion}):
            changes = element.get_text()
print(changes)
