from collections import OrderedDict
import pprint

KEY_FIELDS = ['id', 'title', 'tags', 'answer_count',  'last_activity_at']

class Question:
    def __init__(self, data):
        for field in KEY_FIELDS:
            setattr(self, field, data[field])
            
            
    def data(self):
        data = OrderedDict()
        for field in KEY_FIELDS:
            data[field] = getattr(self, field)
        return data
        
    def __repr__(self):
        return pprint.pformat(dict(self.data()))

