import logging
import re #stripping whitespace for slugs
from google.appengine.ext import ndb

'''class UTILS(object):
    def __init__(self):
        return'''
    
def slugify(string):
    #TODO:Lowercase and URL friendly-ify the slugs
    slug = re.sub(r'\s', '', string)
    slug = slug.lower()
    return slug
    
    
    
    