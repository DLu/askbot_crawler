from collections import OrderedDict

SERVER = 'http://answers.ros.org'

def get_sortable_link(prefix=''):
    return '<script src="%ssorttable.js"></script>\n'%prefix

def generate_table(M):
    s = '<table class="sortable">\n'
    s += '<tr><th>'
    s += '<th>'.join(M[0].keys())
    s += '\n'
    for m in M:
        s += '<tr>'
        for k,v in m.iteritems():
            s += '<td>' + str(v)
        s += '\n'
    s += '</table>\n'
    return s
    
def generate_table_page(M, preamble=''):
    s = get_sortable_link()
    s += preamble
    s += generate_table(M)
    return s
    
def bar_images(amount, fn1='bar.png', amount2=0, fn2='barb.png'):
    S = '<img src="%s" width="%dpx" height="16px"/>'
    s = S % (fn1, amount)
    if amount2 > 0:
        s += S % (fn2, amount2)
    return s
    
def generate_question_table(questions, db):
    rows = []
    for q in questions:
        m = OrderedDict()
        m['Title'] = '<a href="%s/question/%d">%s</a>'%(SERVER, q['id'], q['title'])
        m['Answers'] = q['answer_count']
        m['Answered?'] = q.get('answered', False)
        m['Asker'] = db.get_user( q['user'] )['username']
        rows.append(m)
    return generate_table(rows)
    
def get_avatar_url(u, size=100):
    if 'hash' in u:
        return 'http://www.gravatar.com/avatar/%s?s=%d'%(u['hash'], size)
    else:
        return '%s/avatar/render_primary/%d/48/'%(SERVER, u['id'])
        
def generate_user_table(users, db):
    rows = []
    keys = None
    for uid in users:
        if keys is None:
            keys = users[uid].keys()
        user = db.get_user(uid)
        m = OrderedDict()
        m['Avatar'] = '<img src="%s" alt="avatar"/>'%get_avatar_url(user)
        name = user['username']
        m['Name'] = '<a href="%s/users/%d/%s/">%s</a>'%(SERVER, uid, name, name)
        for key in keys:
            m[key] = users[uid][key]
        rows.append(m)
    return generate_table(rows)
