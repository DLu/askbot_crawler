from bs4 import BeautifulSoup
import re
import dateutil.parser, time

USER_PATTERN_S = 'http://answers.ros.org/users/(\d+)/.*/'
USER_PATTERN = re.compile(USER_PATTERN_S)

def find_all(soup, name, cname):
    return soup.find_all(name, {'class': cname})

def find(soup, name, cname):
    return soup.find(name, {'class': cname})

def parse_answers(contents):
    soup = BeautifulSoup(contents)
    answers = {}
    for div in find_all(soup, 'div', 'answer'):
        answer = {}
        answer['id'] = int(div['data-post-id'])
        if 'accepted-answer' in div['class']:
            answer['accepted'] = True
        answer['votes'] = int(find(div, 'div', 'vote-number').text)
        update = find(div, 'div', 'post-update-info-container')
        
        for g in find_all(update, 'div', 'post-update-info'):
            date = g.find('abbr')['title']
            dt = dateutil.parser.parse(date)
            ep = int(time.mktime(dt.timetuple()))
            
            if 'added_at' in answer:
                answer['last_activity_at'] = ep
            else:
                answer['added_at'] = ep
            
        m = USER_PATTERN.search(find(update, 'a', 'avatar-box')['href'])
        if m:
            answer['user'] = int(m.group(1))
        answers[ answer['id'] ] = answer
    return answers


