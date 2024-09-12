#!/usr/bin/python
from os import write
from bs4 import BeautifulSoup
import collections
import requests


def lookup():
    # website for checking today's names_days in slovakia
    url = "https://kalendar.aktuality.sk/"
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    # this website uses class bg-success to mark todays names_day so we get its text
    text = soup.find("div", class_="bg-success")
    # there are other text elements insite that div but they all have classes so we can just return one that doesn't
    newtext = text.find("span", class_="")
    return newtext.get_text()


def compare_friends(todays_namesday):
    # names.csv should contain names of all of your friends
    def write_to_file(message):
        writefile = open("namesday.csv", "w")
        writefile.write(message)
        print(message)

    file = open("names.csv", "r")
    names = file.read().split(",")

    # if today has only one names_day then we check the singular name else we check for intersection between 2 lists
    if type(todays_namesday) is str:
        if todays_namesday in names:
            message = (
                "REMINDER that today is your friend's "
                + todays_namesday
                + "'s namesday\n"
            )
            write_to_file(message)
    else:
        intersection = collections.Counter(names) & collections.Counter(todays_namesday)
        if intersection != []:
            message = (
                "REMINDER that today is your friend's " + todays_namesday + "namesday\n"
            )
            write_to_file(message)


todays_namesday = lookup()
compare_friends(todays_namesday)
