import json
import urllib2
from question import *

def query(url):
    return json.load(urllib2.urlopen(url))
    
def load_question_page(page=None, sort=None):
    url = 'http://answers.ros.org/api/v1/questions/?'
    params = []
    if page:
        params.append('page=%d'%page)
    if sort:
        params.append('sort=%s'%sort)
    url += '&'.join(params)
    x = query(url)
    questions = []
    for q in x['questions']:
        questions.append( Question(q) )
    return questions

