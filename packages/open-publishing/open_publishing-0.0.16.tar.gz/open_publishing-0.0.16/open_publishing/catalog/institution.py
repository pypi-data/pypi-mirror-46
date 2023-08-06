from open_publishing.core import SimpleField
from open_publishing.core import FieldDescriptor
from open_publishing.core import DatabaseObject
from open_publishing.core.enums import Country, FieldKind
from open_publishing.extendable_enum_field import ExtendableEnumField

class Institution(DatabaseObject):
    _object_class = 'institution'
    
    def __init__(self,
                 context,
                 institution_id):
        super(Institution, self).__init__(context,
                                          institution_id)

        self._fields['name'] = SimpleField(database_object=self,
                                           aspect='*',
                                           field_locator='name',
                                           dtype=str,
                                           kind=FieldKind.readonly)


        self._fields['city'] = SimpleField(database_object=self,
                                           aspect='*',
                                           field_locator='city',
                                           dtype=str,
                                           kind=FieldKind.readonly)                                           


        self._fields['country'] = ExtendableEnumField(database_object=self,
                                                      aspect='*',
                                                      field_locator='country_id',
                                                      dtype=Country,
                                                      nullable=True,
                                                      serialized_null=0,
                                                      kind=FieldKind.readonly)

    name = FieldDescriptor('name')
    city = FieldDescriptor('city')
    country = FieldDescriptor('country')

    @property
    def institution_id(self):
        return self._object_id


class InstitutionField(SimpleField):
    def __init__(self,
                 document):
        super(InstitutionField, self).__init__(database_object=document,
                                               aspect='academic.*',
                                               field_locator='academic.institution',
                                               kind=FieldKind.readonly)

    def _parse_value(self,
                     value):
        if value:
            return Institution(self.database_object.context,
                               institution_id=Institution.id_from_guid(value))
        else:
            return None

    def _value_validation(self,
                          value):
        if value is None:
            return None
        elif isinstance(value, Institution):
            return value
        elif isinstance(value, int):
            return Institution(self.database_object.context,
                           institution_id=value)
        elif isinstance(value, str):
            return Institution(self.database_object.context,
                           institution_id=Institution.id_from_guid(value))
        else:
            raise TypeError("expected instance of institution, institution_id, institution_guid or None, got instance of {0}".format(type(value)))

    def _serialize_value(self,
                         value):
        if value is None:
            return None
        else:
            return value.guid
