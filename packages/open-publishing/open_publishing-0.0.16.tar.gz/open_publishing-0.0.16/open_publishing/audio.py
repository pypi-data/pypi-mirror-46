import datetime

from .core import SimpleField
from .core import FieldGroup
from .core import FieldDescriptor
from .core.enums import FieldKind

class AudioGroup(FieldGroup):
    def __init__(self,
                 document):
        super(AudioGroup, self).__init__(document)
        self._fields["duration"] = DurationField(database_object=document,
                                                 aspect="audiobook.*",
                                                 field_locator="audiobook.duration_in_secs")
        self._fields["number_of_tracks"] = SimpleField(database_object=document,
                                                       aspect="audiobook.*",
                                                       field_locator="audiobook.number_of_tracks",
                                                       dtype=int,
                                                       nullable=True)

    duration = FieldDescriptor("duration")
    number_of_tracks = FieldDescriptor("number_of_tracks")

class DurationField(SimpleField):
    def __init__(self,
                 database_object,
                 aspect,
                 field_locator,
                 kind=FieldKind.regular):
        super(DurationField, self).__init__(database_object,
                                            aspect=aspect,
                                            field_locator=field_locator,
                                            dtype=datetime.timedelta,
                                            kind=kind,
                                            nullable=True)

    def _parse_value(self,
                     value):
        if value is None and self._nullable:
            return value
        else:
            return datetime.timedelta(seconds=value)

    def _serialize_value(self,
                         value):
        if value is None and self._nullable:
            return self._serialized_null
        else:
            return value.total_seconds()
        
