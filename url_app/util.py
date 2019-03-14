# -*- coding: utf-8 -*-
import shortuuid
from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import re


# generate random short url
short_url_generator = lambda: f"{shortuuid.uuid()[0:8]}"


# function for getting text from url
def get_text(url):
    try:
        html = urlopen(url)
    except HTTPError:
        print("This web-page: " + url + " is not defined.")
        return None
    try:
        soup = BeautifulSoup(html.read(), "html.parser")
        text = soup.find('h1').getText()
    except AttributeError:
        print("Tag was not found")
        return None
    return text


# function of edit string and add "™" to each word with 6 letters
def edit_text(text):
    try:
        pattern = re.compile(r'\w+')
        new_words = pattern.findall(text)
        counter = 0
        new_text = ""
        for word in new_words:
            counter += 1
            if len(word) == 6:
                new_words.remove(word)
                word += "™"
                new_words.insert(counter - 1, word)
            else:
                pass
            new_text += word + " "
    except TypeError:
        new_text = ""
    return new_text
