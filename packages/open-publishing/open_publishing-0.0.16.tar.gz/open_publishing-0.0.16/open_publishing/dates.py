import datetime
import time

from .core import SimpleField
from .core import FieldDescriptor
from .core import FieldGroup
from .core.enums import FieldKind


class DatesGroup(FieldGroup):
    def __init__(self,
                 document):
        super(DatesGroup, self).__init__(document)
        self._fields['publication'] = PublishDateGroup(document)
        self._fields['expected_publication'] = ExpectedPublishDateGroup(document)
        self._fields['on_sale'] = OnSaleDateGroup(document)

    publication = FieldDescriptor("publication")
    expected_publication = FieldDescriptor("expected_publication")
    on_sale = FieldDescriptor("on_sale")


class ExpectedPublishDateGroup(FieldGroup):
    def __init__(self,
                 document):
        super(ExpectedPublishDateGroup, self).__init__(document)
        self._fields["ebook"] = IsoDateFieldField(database_object=document,
                                                  aspect="ebook.*",
                                                  field_locator="ebook.expected_publish_date")

        self._fields["book"] = IsoDateFieldField(database_object=document,
                                                  aspect="book.*",
                                                  field_locator="book.expected_publish_date")
    book = FieldDescriptor("book")
    ebook = FieldDescriptor("ebook")


class OnSaleDateGroup(FieldGroup):
    def __init__(self,
                 document):
        super(OnSaleDateGroup, self).__init__(document)
        self._fields["ebook"] = IsoDateFieldField(database_object=document,
                                                  aspect="on_sale_date.*",
                                                  field_locator="on_sale_date.ebook",
                                                  kind=FieldKind.readonly)

        self._fields["book"] = IsoDateFieldField(database_object=document,
                                                 aspect="on_sale_date.*",
                                                 field_locator="on_sale_date.book",
                                                 kind=FieldKind.readonly)

        self._fields["audiobook"] = IsoDateFieldField(database_object=document,
                                                 aspect="on_sale_date.*",
                                                 field_locator="on_sale_date.audiobook",
                                                 kind=FieldKind.readonly)

        self._fields["software"] = IsoDateFieldField(database_object=document,
                                                 aspect="on_sale_date.*",
                                                 field_locator="on_sale_date.software",
                                                 kind=FieldKind.readonly)

    book = FieldDescriptor("book")
    ebook = FieldDescriptor("ebook")
    audiobook = FieldDescriptor("audiobook")
    software = FieldDescriptor("software")


class PublishDateGroup(FieldGroup):
    def __init__(self, document):
        super(PublishDateGroup, self).__init__(document)
        self._fields["ebook"] = IsoDateFieldField(
            database_object=document,
            aspect="ebook.*",
            field_locator="ebook.publish_date")

    ebook = FieldDescriptor("ebook")


class IsoDateFieldField(SimpleField):
    def __init__(self,
                 database_object,
                 aspect,
                 field_locator,
                 kind=FieldKind.regular):
        super(IsoDateFieldField, self).__init__(database_object,
                                                aspect=aspect,
                                                field_locator=field_locator,
                                                dtype=datetime.date,
                                                kind=kind,
                                                nullable=True)

    def _parse_value(self,
                     value):
        if value is None and self._nullable:
            return value
        else:
            return datetime.date(*([int(a) for a in value.split('-')]))

    def _serialize_value(self,
                         value):
        if value is None and self._nullable:
            return self._serialized_null
        else:
            return "{year:04}-{month:02}-{day:02}".format(year=value.year,
                                                          month=value.month,
                                                          day=value.day)
