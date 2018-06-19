from collections import OrderedDict, defaultdict
from html_generation import generate_table
import datetime

SERVER = 'http://answers.ros.org'
ROOT = ''

def sort_by_topic(questions):
    topics = defaultdict(list)
    for q in questions:
        for tag in q['tags']:
            topics[tag].append(q)
    return topics

def bar_images(amount, fn1='bar.png', amount2=0, fn2='barb.png', factor=0.3):
    S = '<img src="%s" width="%dpx" height="16px"/>'
    pixels1 = max(1, int(amount * factor))
    s = S % (fn1, pixels1)
    if amount2 > 0:
        pixels2 = max(1, int(amount2 * factor))
        s += S % (fn2, pixels2)
    return s

def generate_question_table(questions, db, tid=None, params={}):
    rows = []
    for q in questions:
        m = OrderedDict()
        m['Title'] = '<a href="%s/question/%d">%s</a>' % (SERVER, q['id'], q['title'])
        m['Answers'] = q['answer_count']
        m['Answered?'] = q.get('answered', False)
        m['Asker'] = db.get_user(q['user'])['username']
        m['Created'] = str(datetime.datetime.fromtimestamp(q['added_at']))
        m['Updated'] = str(datetime.datetime.fromtimestamp(q.get('last_activity_at', q['added_at'])))
        rows.append(m)
    if not tid:
        tid = 'questions'
    return generate_table(rows, id=tid, params=params)

def get_avatar_url(u, size=100):
    if u['id'] == 0:
        return 'http://www.gravatar.com/avatar/?s=%d' % (size)
    elif 'hash' in u:
        return 'http://www.gravatar.com/avatar/%s?s=%d&d=identicon' % (u['hash'], size)
    else:
        return '%s/avatar/render_primary/%d/48/' % (SERVER, u['id'])

def get_avatar_img(u, size=100, autoload=True):
    url = get_avatar_url(u, size)
    if autoload:
        return '<img src="%s" alt="avatar"/>' % url
    else:
        return '<img src="http://www.metrorobots.com/answers/default.jpg" data-src="%s" alt="avatar"/>' % url

def get_user_link(user, local=True, text=None, prefix=''):
    name = user['username']
    if text is None:
        text = name
    if local:
        link = '%susers/%s.html' % (prefix, name)
    else:
        link = '%s/users/%d/%s/' % (SERVER, user['id'], name)
    return '<a href="%s">%s</a>' % (link, text)

def generate_user_table(users, db, prefix='', tid=None, params={}, keys=None):
    rows = []
    for uid in users:
        if keys is None:
            keys = users[uid].keys()
        user = db.get_user(uid)
        m = OrderedDict()
        m['Avatar'] = get_avatar_img(user, autoload=False)
        m['Name'] = get_user_link(user, prefix=prefix)
        for key in keys:
            m[key] = users[uid][key]
        rows.append(m)
    if not tid:
        tid = 'users'
    params['rowCallback'] = "function(nRow, aData) { var img = $('img', nRow); img.attr('src', img.attr('data-src')); }"
    return generate_table(rows, id=tid, params=params)
