import datetime
from html_generation import *

INDEX_PAGE = """
<div class="center">
<img src="http://answers.ros.org/m/ros/media/images/logoros.png"/>
<p><a href="users.html">[view all users]</a>
<p><a href="topics.html">[view all topics]</a>
<p><a href="https://github.com/DLu/askbot_crawler">[github]</a>
<p>Last Update: %s
</div>
"""

def generate_index_page(fn='website/index.html'):
    with open(fn, 'w') as f:
        f.write( header() )
        now = datetime.datetime.now()
        date = '%d-%02d-%02d %02d:%02d' % ( now.year, now.month, now.day, now.hour, now.minute )
        f.write(INDEX_PAGE % (date) )
        
