from question_database import QuestionDatabase
from html_answer_parser import get_answers
from answer import Answer
import yaml
import collections
import os

DATA_FOLDER = 'data/'

class AnswerDatabase:
    def __init__(self):
        self.data = {}
        for fn in os.listdir(DATA_FOLDER):
            if 'answer' not in fn:
                continue
            self.data.update( yaml.load(open(DATA_FOLDER + fn)) )
    
    def close(self):
        data = collections.defaultdict(dict)
        for aid, a in self.data.iteritems():
            bucket = aid - (aid % 1000)
            data[bucket][aid] = a
        for bucket in sorted(data):
            fn = 'answers%07d.yaml'%bucket
            print 'Writing',fn
            yaml.dump(data[bucket], open(DATA_FOLDER + fn, 'w'))
            
    def update(self, qdb):
        for qid, q in qdb.data.iteritems():
            if hasattr(q, 'answer_ids') or q.answer_count==0:
                continue
            print qid
            try:
                answers = get_answers(qid)
            except Exception, e:
                print e
                break
            print len(answers), q.answer_count
            setattr(q, 'answer_ids', answers.keys())
            self.data.update(answers)
            
        print "Database size: %d"%len(self.data)
        
if __name__=='__main__':

    qdb = QuestionDatabase(True)
    db = AnswerDatabase()
    db.update(qdb)
    db.close()
    qdb.close()
