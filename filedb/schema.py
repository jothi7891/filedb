class Record:
    def __init__(self, project, shot, version, status, finish_date, internal_bid, created_date):
        self.project = project
        self.shot = shot
        self.version = version
        self.status = status
        self.finish_date = finish_date
        self.internal_bid = internal_bid
        self.created_date = created_date


class Properties:
    def __init__(self, name, field_type, required, description=None, max_len=None, min_len=None, max_value=None):
        self.name = name
        self.field_type = field_type
        self.required = required
        self.description = description
        self.max_len = max_len
        self.min_len = min_len
        self.max_value = max_value



