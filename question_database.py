from crawler import *
import yaml
import collections
import os, sys
from progressbar import ProgressBar
from html_answer_parser import get_answers
from utils import sort_by_topic

DATA_FOLDER = 'data/'

class Database(dict):
    def __init__(self, name):
        self.name = name
        self.changed = False
        filenames = grab_files(DATA_FOLDER, name)
        if len(filenames)>0:
            pbar = ProgressBar(maxval=len(filenames))
            print "Reading %s database"%self.name
            for i, fn in enumerate(filenames):
                self.update(yaml.load(open(fn)))
                pbar.update(i)
            pbar.finish()
        self.print_size()
            
    def print_size(self):
        print '%s Database size: %d' % (self.name, len(self))
            
    def write_database(self, bucketsize=1000):
        if not self.changed:
            print "Skipping writing %s database"%self.name
            return
        pattern = DATA_FOLDER + self.name + '%07d.yaml'
        data = collections.defaultdict(dict)
        print "Writing %s database"%self.name
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
        
    def add_items(self, items):
        self.changed = True
        for q in items:
            self[ q['id'] ] = q
        
            
def grab_files(folder, pattern, small=False):
    fs = sorted([folder + x for x in os.listdir(folder) if pattern in x])
    if small:
        return fs[:1]
    else:
        return fs

class QuestionDatabase(Database):
    def __init__(self, small=False):
        Database.__init__(self, 'questions')
        
    def close(self):
        self.write_database()
            
    def update_from_web(self, max_count=10):
        pages, count = question_info()
        c = 0
        while True:
            n = len(self)
            pn = n/50+1
            if pn>=pages:
                break
            print "Load page %d/%d"%(pn, pages)
            self.add_items( load_questions(page=pn, sort='activity-asc') )
            c += 1
            if c >= max_count:
                break
        self.print_size()
        
    def update_with_latest(self):
        more = True
        page = 0
        ids = []
        while more:
            questions = load_questions(page=page, sort='activity-desc')
            for q in questions:
                qid = q['id']
                print "New question", qid
                if qid not in self:
                    self[ qid ] = q
                    ids.append( qid ) 
                else:
                    old_activity = self[ qid ]['last_activity_at']
                    new_activity = q['last_activity_at']
                    if old_activity != new_activity:
                        self[ qid ] = q
                        ids.append( qid )
                    else:
                        more = False
                        print "Old activity!"
            page += 1
        if len(ids)>0:
            self.changed = True
        return ids
        
class AnswerDatabase(Database):
    def __init__(self):
        Database.__init__(self, 'answers')
        
    def close(self):
        self.write_database()
        
    def update_question(self, qid, q):
        try:
            answers = get_answers(qid)
        except Exception, e:
            print e
            return
        q['answer_ids'] = answers.keys()
        for aid, answer in answers.iteritems():
            if 'accepted' in answer:
                q['answered'] = True
        self.update(answers)
        self.changed = True
    
    def update_from_web(self, qdb, max_count=10):
        c = 0
        pbar = ProgressBar(maxval=max_count)
        for qid, q in qdb.iteritems():
            if 'answer_ids' in q or q.get('answer_ids', -10)==0:
                continue
            self.update_question(qid, q)
            self.qdb.changed = True
            c+=1
            pbar.update(c)
            if c >= max_count:
                break
        pbar.finish()
        self.print_size()
        
    def progressive_update(self):
        for fn in grab_files(DATA_FOLDER, 'question'):
            print "%s (%d)"%(fn, len(self))
            data = yaml.load(open(fn))
            for qid, q in data.iteritems():
                if 'answer_ids' in q or q.get('answer_ids', -10)==0:
                    continue

                self.update_question(qid, q)
                self.qdb.changed = True
            yaml.dump(data, open(fn, 'w'))
            
class UserDatabase(Database):
    def __init__(self):
        Database.__init__(self, 'users')
    
    def close(self):
        self.write_database()
        
    def update_from_web(self, max_count=10):
        pages, count = user_info()
        c = 0
        while True:
            n = len(self)
            pn = n/10+1
            if pn>=pages:
                break
            print "Load page %d/%d"%(pn, pages)
            self.add_items( load_users(page=pn) )
            c += 1
            if c >= max_count:
                break
        self.print_size()
        
    def get_user(self, uid, load=True):
        if uid in self:
            return self[uid]
        if uid == 0:
            return {'id': 0, 'username': 'Anonymous'}
        if load:
            self[uid] = load_user(uid)
            self.changed = True
            return self[uid]
        else:
            return {'id': uid, 'username': 'User%d'%uid}
        
class AskbotDatabase:
    def __init__(self):
        self.qdb = QuestionDatabase()
        self.adb = AnswerDatabase()
        self.udb = UserDatabase()
        
    def close(self):
        self.adb.close()
        self.qdb.close()
        self.udb.close()
        
    def get_topic_map(self):
        return sort_by_topic( self.qdb.values() )
        
    def get_questions_by_user(self):
        questions = collections.defaultdict(list)        
        for qid, q in self.qdb.iteritems():
            questions[ q.get('user', 0) ].append(qid)
        return questions
        
    def get_answers_by_user(self):
        answers = collections.defaultdict(list)        
        for aid, a in self.adb.iteritems():
            answers[ a.get('user', 0) ].append(aid)
        return answers
        
    def get_question(self, qid):
        return self.qdb[qid]
        
    def get_answer(self, aid):
        return self.adb[aid]
        
    def get_user(self, uid):
        return self.udb.get_user(uid)
        
if __name__=='__main__':
    if 'questions' in sys.argv:
        db = QuestionDatabase()
        db.update_from_web()
        db.close()
    elif 'answers' in sys.argv:
        qdb = QuestionDatabase()
        db = AnswerDatabase()
        db.update_from_web(qdb)
        db.close()
        qdb.close()
    elif 'users' in sys.argv:
        udb = UserDatabase()
        udb.update_from_web()
        udb.close()
    elif 'ap' in sys.argv:
        db = AnswerDatabase()
        db.progressive_update()
        db.close()
    else:
        db = QuestionDatabase()
        qids = db.update_with_latest()
        print "%d new questions"%len(qids)
        if len(qids)>0:
            adb = AnswerDatabase()
            pbar = ProgressBar(maxval=len(qids))
            for i, qid in enumerate(qids):
                adb.update_question(qid, db[qid])
                pbar.update(i)
            pbar.finish()
            adb.print_size()
            adb.close()
        db.close()
