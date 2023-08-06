class Message:
    def __init__(self, **options):
        self._author = options.get('author')
        self._id = options.get('_id')
        self._is_read = options.get('is_read')
        self._subject = options.get('subject')
        self._body = options.get('body')
        self._timestamp = options.get('timestamp')