import json
import urllib2
import re
import unicodedata
from utils import SERVER

KEY_FIELDS = ['id', 'title', 'tags', 'answer_count',  'answer_ids', 'added_at', 'last_activity_at']
GRAVATAR_PATTERN_S = '//www.gravatar.com/avatar/([^\?]*)\?.*'
GRAVATAR_PATTERN = re.compile(GRAVATAR_PATTERN_S)
AVATAR_PATTERN_S = SERVER + '/avatar/render_primary/(\d+)/48/'
AVATAR_PATTERN = re.compile(AVATAR_PATTERN_S)

def query(url):
    return json.load(urllib2.urlopen(url))

def clean(s):
    if type(s)==unicode:
        return unicodedata.normalize('NFKD', s).encode('ascii','ignore')
    elif type(s)==list and len(s)>0 and type(s[0])==unicode:
        return [unicodedata.normalize('NFKD', x).encode('ascii','ignore') for x in s]
    return s
    
def load_page(name, page=None, sort=None):
    url = '%s/api/v1/%s/?'%(SERVER, name)
    params = []
    if page:
        params.append('page=%d'%page)
    if sort:
        params.append('sort=%s'%sort)
    url += '&'.join(params)
    return query(url)
    
def load_question_page(page=None, sort=None):
    return load_page('questions', page, sort)
    
def load_user_page(page=None, sort=None):
    return load_page('users', page, sort)
    
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
    
def process_user(u):
    u2 = {}
    for field in ['username', 'id']:
        u2[field] = clean(u[field])
    m = GRAVATAR_PATTERN.match(u['avatar'])
    if m:
        u2['hash'] = clean(m.group(1))
    else:
        m2 = AVATAR_PATTERN.match(u['avatar'])
        if not m2:
            u2['avatar'] = clean(u['avatar'])
            print u2['avatar']
    return u2    
    
def load_users(page=None):
    x = load_user_page(page=page, sort='recent')
    users = []
    for u in x['users']:
        users.append( process_user(u) )
    return users
    
def load_user(uid):
    x = load_page('users/%d'%uid)
    return process_user(x) 
    
def question_info():
    x = load_question_page()
    return x['pages'], x['count']
    
def user_info():
    x = load_user_page()
    return x['pages'], x['count']
