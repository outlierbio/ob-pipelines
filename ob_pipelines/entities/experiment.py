from datetime import datetime


class Experiment(object):
    def __init__(self, *args, **kwargs):
        if 'id' in kwargs:
            self.key = kwargs['id']

        if 'fields' in kwargs:
            self._name = kwargs['fields']['Name']
            kwargs['fields'].pop('Name', None)
            self.__dict__.update(kwargs['fields'])

        if 'createdTime' in kwargs:
            self._created_at = kwargs['createdTime']
        else:
            self._created_at = datetime.utcnow()

    @property
    def name(self):
        return self._name

    @property
    def created_at(self):
        return self._created_at

    @name.setter
    def name(self, value):
        self._name = value
