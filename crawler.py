import json
import urllib2

import unicodedata

KEY_FIELDS = ['id', 'title', 'tags', 'answer_count',  'answer_ids', 'added_at', 'last_activity_at']

def query(url):
    return json.load(urllib2.urlopen(url))

def clean(s):
    if type(s)==unicode:
        return unicodedata.normalize('NFKD', s).encode('ascii','ignore')
    elif type(s)==list and len(s)>0 and type(s[0])==unicode:
        return [unicodedata.normalize('NFKD', x).encode('ascii','ignore') for x in s]
    return s
    
def load_question_page(page=None, sort=None):
    url = 'http://answers.ros.org/api/v1/questions/?'
    params = []
    if page:
        params.append('page=%d'%page)
    if sort:
        params.append('sort=%s'%sort)
    url += '&'.join(params)
    return query(url)
    
def load_questions(page=None, sort=None):
    x = load_question_page(page, sort)
    questions = []
    for q in x['questions']:
        q2 = {}
        for field in KEY_FIELDS:
            if field in q:
                q2[field] = clean(q[field])
                if field == 'last_activity_at' or field=='added_at':
                    q2[field] = int(q2[field])
        q2['user'] = q['author']['id']
        questions.append( q2 )
    return questions

def question_info():
    x = load_question_page()
    return x['pages'], x['count']
