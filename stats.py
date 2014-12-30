from question_database import AskbotDatabase

if __name__=='__main__':
    db = AskbotDatabase()
   
    m = db.get_topic_map()
    for J in sorted(m, key=lambda d: len(m[d])):
        pct = len([x for x in m[J] if 'answered' in x])
        n = len(m[J])
        print '%20s'%J, '*'*pct + '-'*(n-pct)
