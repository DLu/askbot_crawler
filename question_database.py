from question import Question
from crawler import *
import yaml
import collections
import os

DATA_FOLDER = 'data/'

class QuestionDatabase:
    def __init__(self, small=False):
        self.data = {}
        for fn in sorted(os.listdir(DATA_FOLDER)):
            if 'question' not in fn:
                continue
            for qid, data in yaml.load(open(DATA_FOLDER + fn)).iteritems():
                q = Question(data)
                self.data[qid] = q
            if small:
                break
    
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
            
    def update(self, max_count=10):
        pages, count = question_info()
        c = 0
        while True:
            n = len(self.data)
            pn = n/50+1
            if pn>=pages:
                break
            print "Load page %d"%pn
            self.add_questions( load_questions(page=pn, sort='activity-asc') )
            c += 1
            if c >= max_count:
                break
        print "Database size: %d"%len(self.data)
        
if __name__=='__main__':
    db = QuestionDatabase()
    db.update()
    db.close()
