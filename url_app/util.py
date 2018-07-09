# -*- coding: utf-8 -*-
import string
import random
from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import re


# generate random short url
def short_url_generator():
    rand_list = [random.choice(string.digits),
                 random.choice(string.ascii_uppercase),
                 random.choice(string.ascii_lowercase),
                 random.choice(string.ascii_letters)]
    return "{}{}{}{}{}{}".format(
        random.choice(string.ascii_lowercase),
        random.choice(rand_list),
        random.choice(rand_list),
        random.choice(rand_list),
        random.choice(rand_list),
        random.choice(rand_list))


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
