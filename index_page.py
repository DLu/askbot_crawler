import datetime

INDEX_PAGE = """
Last Update: %s
"""

def generate_index_page(fn='website/index.html'):
    with open(fn, 'w') as f:
        now = datetime.datetime.now()
        date = '%d-%02d-%02d %02d:%02d' % ( now.year, now.month, now.day, now.hour, now.minute )
        f.write(INDEX_PAGE % (date) )
        
