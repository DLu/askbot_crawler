from question_database import AskbotDatabase
from utils import *
from collections import OrderedDict, defaultdict
import os

USERS_FOLDER = 'website/users'

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
        
        X = OrderedDict()
        X['Asked'] = len(qs)
        X['Answered'] = len(ans)
        X['Accepted'] = len([a for a in ans if a.get('accepted', False)])
        
        if len(qs)>0:
            ratio = len(ans)/len(qs)
        else:
            ratio = "Infinity"
        
        X['Helpful Ratio'] = ratio
        
        #generate_user_page(db, J, m[J])
        
        data[uid] = X
        
    with open(fn, 'w') as f:
        f.write( get_sortable_link() )
        f.write( generate_user_table(data, db) )
         

if __name__=='__main__':
    db = AskbotDatabase()
    if not os.path.exists(USERS_FOLDER):
        os.mkdir(USERS_FOLDER)
    generate_users_page(db)
    db.close()
    
