from question_database import AskbotDatabase
from utils import *
from collections import OrderedDict, defaultdict
from html_generation import *
import os

USERS_FOLDER = 'website/users'

def sort_map(m):
    return sorted(m, key=lambda k: len(m[k]), reverse=True)

def get_summary(q_topics, a_topics, qlimit=-1, topic_n=3):
    top = []
    for topic in sort_map(a_topics):
        qs = a_topics[topic]
        if len(qs) > qlimit:
            top.append(topic)
        if len(top) >= topic_n:
            break
            
    for topic in sort_map(q_topics):
        if len(top) >= topic_n:
            break

        qs = q_topics[topic]
        if len(qs) > qlimit and topic not in top:
            top.append(topic)
            
    if len(top)==0:
        return ''
                    
    return ', '.join(top)
    
def generate_topic_viz(topics):
    s = ''
    for topic in sort_map(topics):
        s += '%s: %d <br>\n'%(topic, len( topics[topic] ))
    return s
    
def generate_user_page(db, user, questions, answers, accepted, q_topics, a_topics):
    fn = USERS_FOLDER + '/' + user['username'] + '.html'
    
    #s = generate_question_table(questions, db)
    
    with open(fn, 'w') as f:
        f.write( JQUERY_LINKS )
        f.write('<table><tr><td>%s<td><h1>%s</h1></table>'%(get_avatar_img(user), user['username']))
        if user['id'] != 0:
            f.write(get_user_link(user, local=False, text="%s Profile"%SERVER))
        f.write("<h3>Questions Asked: %d </h3>"%len(questions))
        f.write( generate_topic_viz(q_topics) )
        f.write("<h3>Questions Answered: %d </h3>"%len(answers))
        f.write( generate_topic_viz(a_topics) )
        f.write('<h3>Answers Accepted: %d </h3>'%accepted)
        
        #f.write( s )
        #f.write( s2 )


def generate_users_page(db, fn='website/users.html'):
    data = {}
    questions = db.get_questions_by_user()
    answers = db.get_answers_by_user()
    users = set(questions.keys() + answers.keys())
    
    for uid in users:
        qids = questions.get(uid, [])
        aids = answers.get(uid, [])
        
        qs = [ db.get_question(qid) for qid in qids ] 
        ans = [ db.get_answer(aid) for aid in aids ]
        acc = len([a for a in ans if a.get('accepted', False)])
        
        answered_qs = [ db.get_question(a['qid']) for a in ans ]
        
        q_topics = sort_by_topic(qs)
        a_topics = sort_by_topic(answered_qs)
        
        summary = get_summary(q_topics, a_topics)
        
        X = OrderedDict()
        X['Asked'] = len(qs)
        X['Answered'] = len(ans)
        X['Accepted'] = acc
        
        if len(qs)>0:
            ratio = len(ans)/len(qs)
        else:
            ratio = "&infin;"
        
        X['Helpful Ratio'] = ratio
        X['Top Topics'] = summary
        
        generate_user_page(db, db.get_user(uid), qs, ans, acc, q_topics, a_topics)
        
        data[uid] = X
        
    with open(fn, 'w') as f:
        f.write( JQUERY_LINKS )
        f.write( INFINITY_SORT )
        f.write( generate_user_table(data, db, params={"order": [(3, "desc")], "columnDefs": [{"type": "infinity", "targets": 5}]}) )
         

if __name__=='__main__':
    db = AskbotDatabase()
    if not os.path.exists(USERS_FOLDER):
        os.mkdir(USERS_FOLDER)
    generate_users_page(db)
    db.close()
    
