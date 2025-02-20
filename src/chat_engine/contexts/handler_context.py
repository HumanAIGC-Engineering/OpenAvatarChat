class HandlerContext(object):
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.owner = None
