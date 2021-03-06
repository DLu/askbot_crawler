#!/usr/bin/python
import sys
from question_database import AskbotDatabase
from users import generate_users_page
from topics import generate_topics_page
from index_page import generate_index_page

if __name__ == '__main__':
    db = AskbotDatabase()
    try:
        if '-x' not in sys.argv:
            db.super_update()
        generate_users_page(db)
        generate_topics_page(db)
        generate_index_page(db)
    finally:
        db.close()
