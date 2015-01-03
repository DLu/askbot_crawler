from question_database import AskbotDatabase
from utils import *
from collections import OrderedDict

def generate_topics_page(db, fn='table.html'):
    data = []
    #print '<tr><th>Tag<th># answers<th># answered<th># questions'
    m = db.get_topic_map()
    for J in sorted(m, key=lambda d: len(m[d])):
        X = OrderedDict()
        n = len(m[J])
        answered = len([x for x in m[J] if 'answered' in x])
        answers = sum([x['answer_count'] for x in m[J]])
        X['Tag'] = J
        X['Visualization'] = bar_images(answered, amount2=n-answered)
        X['# answered'] = answered
        X['# answers'] = answers
        X['# questions'] = n
        X['% answered'] = '%.1f%%'%(float(answered)*100/n)
        X['Answer Ratio'] = '%.1f'%(float(answers)/n)
        data.append(X)
    with open(fn, 'w') as f:
        f.write( generate_table_page( data ) )
         

if __name__=='__main__':
    db = AskbotDatabase()
    generate_topics_page(db)
    
