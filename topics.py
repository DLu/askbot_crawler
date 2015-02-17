from question_database import AskbotDatabase
from utils import *
from collections import OrderedDict, defaultdict
import os

TOPICS_FOLDER = ROOT + 'website/topics'

def generate_section(questions, db, name, key):
    s = '<span class="topichead">%s: %d</span>\n'%(name, len(questions))
    if len(questions)==0:
        s += '<br /><br />\n'
        return s
    s += '&nbsp;&nbsp;&nbsp;<a href="javascript:ReverseDisplay(\'%scontainer\')">[expand/collapse]</a><br/>\n'%key
    s += '<span id="%scontainer" style="display: none">\n'%key
    s += '<br />'
    s += generate_question_table(questions, db, tid=key)
    s += '</span>\n<br />\n'
    return s

def generate_topic_page(db, topic, questions):
    fn = TOPICS_FOLDER + '/' + topic + '.html'
    
    closed = []
    lonely = []
    unfinished = []
    
    for question in questions:
        if question.get('answered', False) or question.get('closed', False):
            closed.append(question)
        elif question['answer_count']==0:
            lonely.append(question)
        else:
            unfinished.append(question)
            
    s = generate_section(lonely, db, 'Questions with no answers', "t1") \
        + generate_section(unfinished, db, 'Questions with no accepted answers', "t2") \
        + generate_section(closed, db, 'Closed Questions', 't3')
    
    users = defaultdict( lambda : defaultdict(int) )
    for q in questions:
        users[ q['user'] ]['Asked']+=1
        for aid in q.get('answer_ids', []):
            a = db.get_answer(aid)
            uid = a.get('user', 0)
            users[ uid ]['Answered'] += 1
            if a.get('accepted', False):
                users[ uid ]['Accepted'] += 1
                
    s2 = generate_user_table(users, db, prefix='../', keys=['Asked', 'Answered', 'Accepted'], params={"order": [(3, "desc")]})
    
    with open(fn, 'w') as f:
        f.write( header(topic + " - ROS Answered", JQUERY_LINKS, '../', True))
        f.write( '<h1>%s</h1>\n' % topic )
        f.write( s )
        f.write( '<br /> <hr /> <br />\n' )
        f.write( '<h2>Users</h2>')
        f.write( s2 )


def generate_topics_page(db, fn='website/topics.html'):
    data = []
    #print '<tr><th>Tag<th># answers<th># answered<th># questions'
    m = db.get_topic_map()
    for J in sorted(m, key=lambda d: len(m[d])):
        X = OrderedDict()
        n = len(m[J])
        answered = len([x for x in m[J] if 'answered' in x or x.get('closed', False)])
        answers = sum([x['answer_count'] for x in m[J]])
        X['Tag'] = '<a href="topics/%s.html">%s</a>'%(J,J)
        X['Visualization'] = bar_images(answered, amount2=n-answered)
        X['# questions'] = n
        X['# answered'] = answered
        X['# answers'] = answers
        X['% answered'] = '%.1f%%'%(float(answered)*100/n)
        X['Answer Ratio'] = '%.1f'%(float(answers)/n)
        
        generate_topic_page(db, J, m[J])
        
        data.append(X)
    with open(fn, 'w') as f:
        f.write( header("Topics - ROS Answered", JQUERY_LINKS))
        f.write(generate_table(data,params={"order": [(2, "desc")]}))         

if __name__=='__main__':
    db = AskbotDatabase()
    if not os.path.exists(TOPICS_FOLDER):
        os.mkdir(TOPICS_FOLDER)
    generate_topics_page(db)
    db.close()
    
