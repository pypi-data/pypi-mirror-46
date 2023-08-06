import logging
import re
import threading
import unicodedata


class Base(object):
    def __init__(self):
        self.log = logging.getLogger(self.__class__.__name__)

    def slugify(self, value):
        """
        Convert to ASCII. Convert spaces to hyphens.
        Remove characters that aren't alphanumerics, underscores, or hyphens.
        Convert to lowercase. Also strip leading and trailing whitespace.

        Source: https://docs.djangoproject.com/en/2.1/_modules/django/utils/text/#slugify
        """
        value = str(value)
        value = unicodedata.normalize(
            'NFKD', value).encode(
            'ascii', 'ignore').decode('ascii')
        value = re.sub(r'[^\w\s-]', '', value).strip().lower()
        return re.sub(r'[-\s]+', '-', value)


class ThreadedBase(threading.Thread):
    def __init__(self, thread_id):
        threading.Thread.__init__(self)
        self.log = logging.getLogger(f'{self.__class__.__name__}#{thread_id}')
