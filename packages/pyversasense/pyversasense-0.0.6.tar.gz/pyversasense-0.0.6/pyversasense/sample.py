class Sample:

    def __init__(self, unit, value, datatype, measurement, timestamp, parentId):
        self._unit = unit
        self._value = value
        self._datatype = datatype
        self._measurement = measurement
        self._timestamp = timestamp
        self._parentId = parentId

    @property
    def unit(self):
        return self._unit

    @property
    def value(self):
        return self._value

    @property
    def datatype(self):
        return self._datatype

    @property
    def measurement(self):
        return self._measurement

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def parentId(self):
        return self._parentId