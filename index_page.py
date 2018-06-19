import datetime
from html_generation import header
from utils import ROOT

INDEX_PAGE = """
<div class="center">
<img src="http://answers.ros.org/m/ros/media/images/logoros.png"/>
<p>%d Questions<br/>
%d Answers<br/>
%d Questions Answered<br/>
%.2f%% Questions Answered<br/>
%d Users
<p>
<p><a href="users.html">[view all users]</a>
   <a href="topics.html">[view all topics]</a>
<p><a href="https://github.com/DLu/askbot_crawler">[github]</a>
<p>Last Update: %s
</div>
"""

def generate_index_page(db, fn='website/index.html'):
    n_questions = len(db.qdb)
    n_answers = len(db.adb)
    n_users = len(db.udb)
    n_answered = len([x for x in db.qdb.values() if 'answered' in x or x.get('closed', False)])
    with open(ROOT + fn, 'w') as f:
        f.write(header())
        now = datetime.datetime.now()
        date = '%d-%02d-%02d %02d:%02d' % (now.year, now.month, now.day, now.hour, now.minute)
        f.write(INDEX_PAGE % (n_questions, n_answers, n_answered, n_answered * 100.0 / n_questions, n_users, date))
