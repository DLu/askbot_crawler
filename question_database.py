from crawler import *
import yaml
import collections
import os, sys
from progressbar import ProgressBar
from html_answer_parser import get_answers

DATA_FOLDER = 'data/'

class Database(dict):
    def __init__(self, filenames=[]):
        if len(filenames)>0:
            pbar = ProgressBar(maxval=len(filenames))
            print "Reading database"
            for i, fn in enumerate(filenames):
                self.update(yaml.load(open(fn)))
                pbar.update(i)
            pbar.finish()
        print "Database size:", len(self)
            
    def write_database(self, pattern):
        data = collections.defaultdict(dict)
        print "Writing database"
        for key, value in self.iteritems():
            bucket = key - (key % 1000)
            data[bucket][key] = value
        if len(data)==0:
            return
        pbar = ProgressBar(maxval=len(data))
        for i, bucket in enumerate(sorted(data)):
            fn = pattern % bucket
            yaml.dump(data[bucket], open(fn, 'w'))
            pbar.update(i)
        pbar.finish()
            
def grab_files(folder, pattern, small=False):
    fs = sorted([folder + x for x in os.listdir(folder) if pattern in x])
    if small:
        return fs[:1]
    else:
        return fs

class QuestionDatabase(Database):
    def __init__(self, small=False):
        Database.__init__(self, grab_files(DATA_FOLDER, 'question', small))
    
    def close(self):
        self.write_database(DATA_FOLDER + 'questions%07d.yaml')
        
    def add_questions(self, qs):
        for q in qs:
            self[ q['id'] ] = q
            
    def update_from_web(self, max_count=10):
        pages, count = question_info()
        c = 0
        while True:
            n = len(self)
            pn = n/50+1
            if pn>=pages:
                break
            print "Load page %d"%pn
            self.add_questions( load_questions(page=pn, sort='activity-asc') )
            c += 1
            if c >= max_count:
                break
        print "Database size: %d"%len(self)
        
class AnswerDatabase(Database):
    def __init__(self):
        Database.__init__(self, grab_files(DATA_FOLDER, 'answer'))
        
    def close(self):
        self.write_database(DATA_FOLDER + 'answers%07d.yaml')
    
    def update_from_web(self, qdb, max_count=10):
        c = 0
        for qid, q in qdb.iteritems():
            if 'answer_ids' in q or q.get('answer_ids', -10)==0:
                continue
            print qid
            try:
                answers = get_answers(qid)
            except Exception, e:
                print e
                break
            q['answer_ids'] = answers.keys()
            self.update(answers)
            
            c+=1
            if c >= max_count:
                break
            
        print "Database size: %d"%len(self)

        
if __name__=='__main__':
    if 'questions' in sys.argv:
        db = QuestionDatabase()
        db.update_from_web()
        db.close()
    elif 'answers' in sys.argv:
        qdb = QuestionDatabase(True)
        db = AnswerDatabase()
        db.update_from_web(qdb)
        db.close()
        qdb.close()
