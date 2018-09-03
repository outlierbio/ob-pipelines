from datetime import datetime


class Task(object):
    _statuses = ['queued', 'running', 'completed', 'failed']

    def __init__(self, *args, **kwargs):
        if 'id' in kwargs:
            self.key = kwargs['id']

        if 'fields' in kwargs:
            self._name = kwargs['fields']['Name']
            kwargs['fields'].pop('Name', None)

            if 'Status' in kwargs['fields']:
                self._status = kwargs['fields']['Status']
                kwargs['fields'].pop('Status', None)
            else:
                self._status = 'queued'

            if 'Started_at' in kwargs['fields']:
                self._started_at = kwargs['fields']['Started_at']
                kwargs['fields'].pop('Started_at', None)
            else:
                self._started_at = None

            if 'Completed_at' in kwargs['fields']:
                self._completed_at = kwargs['fields']['Completed_at']
                kwargs['fields'].pop('Completed_at', None)
            else:
                self._completed_at = None

            self.__dict__.update(kwargs['fields'])

        if 'createdTime' in kwargs:
            self._created_at = kwargs['createdTime']
        else:
            self._created_at = datetime.utcnow()

        self._exception = None

    @property
    def name(self):
        return self._name

    @property
    def created_at(self):
        return self._created_at

    @property
    def started_at(self):
        return self._started_at

    @property
    def completed_at(self):
        return self._completed_at

    @property
    def status(self):
        return self._status

    @property
    def exception(self):
        return self._exception

    @name.setter
    def name(self, value):
        self._name = value

    @status.setter
    def status(self, value):
        if value not in self._statuses:
            raise ValueError('status value must be within {0}'.format(','.join(self._statuses)))
        self._status = value

    @started_at.setter
    def started_at(self, value):
        self._started_at = value

    @completed_at.setter
    def completed_at(self, value):
        self._completed_at = value

    @exception.setter
    def exception(self, value):
        self._exception = value
