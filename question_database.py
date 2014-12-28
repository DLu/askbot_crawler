from question import Question
from crawler import *
import yaml
import collections
import os

DATA_FOLDER = 'data/'

class QuestionDatabase:
    def __init__(self):
        self.data = {}
        for fn in os.listdir(DATA_FOLDER):
            for qid, data in yaml.load(open(DATA_FOLDER + fn)).iteritems():
                q = Question(data)
                self.data[qid] = q
    
    def close(self):
        data = collections.defaultdict(dict)
        for qid, q in self.data.iteritems():
            bucket = qid - (qid % 1000)
            data[bucket][qid] = q.data()
        for bucket in sorted(data):
            fn = 'questions%07d.yaml'%bucket
            print 'Writing',fn
            yaml.dump(data[bucket], open(DATA_FOLDER + fn, 'w'))
        
    def add_questions(self, qs):
        for q in qs:
            self.data[ q.id ] = q
            
    def update(self):
        n = len(self.data)
        pn = n/50+1
        print "Load page %d"%pn
        self.add_questions( load_question_page(page=pn, sort='activity-asc') )
            
        
        
if __name__=='__main__':
    db = QuestionDatabase()
    for x in range(10):
        db.update()
        print len(db.data)
    db.close()
