from question import Question
from crawler import *
import yaml

DATA_FOLDER = 'data/'

class QuestionDatabase:
    def __init__(self):
        self.data = {}
        for qid, data in yaml.load(open(DATA_FOLDER + 'questions.yaml')).iteritems():
            q = Question(data)
            self.data[qid] = q
    
    def close(self):
        data = {}
        for qid, q in self.data.iteritems():
            data[qid] = q.data()
        yaml.dump(data, open(DATA_FOLDER + 'questions.yaml', 'w'))
        
    def add_questions(self, qs):
        for q in qs:
            self.data[ q.id ] = q
            
        
        
if __name__=='__main__':
    db = QuestionDatabase()
    db.add_questions( load_question_page() )
    db.close()
