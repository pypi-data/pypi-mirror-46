# coding=utf-8
#---------------------------------------------------------------------------
# Copyright 2011 utahta
#---------------------------------------------------------------------------
from bs4 import BeautifulSoup
import logging
import six
import requests

def html_parser(html):
    try:
        soup = BeautifulSoup(html,features = "lxml")
    except:
        soup = BeautifulSoup(html, "html5lib")
    return soup

def use_debug():
    logging.basicConfig(level=logging.DEBUG, format="[%(asctime)s][%(levelname)s] %(message)s")

def debuglog(val):
    logging.debug(val)
    
def to_utf8(val):
    try:
        return str(val.encode('utf-8'))
    except:
        return val

def to_unicode(val):
    try:
        return str(val.decode('utf-8'))
    except:
        return str

def create_session():
    return requests.Session()
