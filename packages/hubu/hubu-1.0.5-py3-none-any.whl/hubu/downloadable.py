import os
from hubu.base import Base


class Downloadable(Base):
    def __init__(self, bundle, name, platform, filename, url, size):
        super(__class__, self).__init__()
        self.download_path = f"{bundle}/{platform}/{name}/{filename}"
        self.url = url
        self.size = size

    def path(self, base=''):
        return os.path.join(base, self.download_path)

    def __lt__(self, other):
        return self.size < getattr(other, 'size', other)

    def __gt__(self, other):
        return self.size > getattr(other, 'size', other)

    def __aq__(self, other):
        return self.size == getattr(other, 'size', other)
