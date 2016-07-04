import time
import json


class DBObject(object):
    """This class defines how objects in the mongoDB should be represented."""

    def __init__(
            self,
            classes=[],
            type='',
            meta={}
            ):
        self.created = time.strftime("%Y-%m-%d %H:%M:%S")
        self.updated = time.strftime("%Y-%m-%d %H:%M:%S")
        self.classes = classes
        self.type = type
        self.meta = meta
        self.structure = '{}{}'.format('#', self.__class__.__name__)


    def export(self):
        """This function exports the object as a dict. This is used when
        putting an object in the database."""

        return self.__dict__


class URLEntry(DBObject):

    def __init__(
            self,
            domain='',
            url='',
            last_scraped=time.strftime("%Y-%m-%d %H:%M:%S"),
            *args,
            **kwargs
            ):
        DBObject.__init__(self, *args, **kwargs)
        self.domain = domain
        self.url = url
        self.last_scraped = last_scraped
