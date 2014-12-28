import pprint

KEY_FIELDS = ['id', 'title', 'tags', 'answer_count',  'answer_ids', 'last_activity_at']

class Question:
    def __init__(self, data):
        for field in KEY_FIELDS:
            if field in data:
                setattr(self, field, data[field])

    def data(self):
        data = {}
        for field in KEY_FIELDS:
            if hasattr(self, field):
                data[field] = getattr(self, field)
        return data
        
    def __repr__(self):
        return pprint.pformat(dict(self.data()))

