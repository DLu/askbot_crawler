#!/usr/bin/python
import sys
from question_database import *
from users import generate_users_page
from topics import generate_topics_page

if __name__=='__main__':
    db = AskbotDatabase()
    if '-x' not in sys.argv:
        db.super_update()
    generate_users_page(db)
    generate_topics_page(db)
    db.close()

