import json
import urllib2
from question import *

def query(url):
    return json.load(urllib2.urlopen(url))
    
def load_question_page(page=None):
    url = 'http://answers.ros.org/api/v1/questions/'
    if page:
        url += '?page=%d'%page
    x = query(url)
    questions = []
    for q in x['questions']:
        questions.append( Question(q) )
    return questions

