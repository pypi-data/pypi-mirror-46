from open_publishing.core import SimpleField
from open_publishing.core import FieldDescriptor
from open_publishing.core import DatabaseObject
from open_publishing.core.enums import FieldKind

class CountryInfo(DatabaseObject):
    _object_class = 'country'
    
    def __init__(self,
                 context,
                 country_id):
        super(CountryInfo, self).__init__(context,
                                          country_id)

        self._fields['name'] = SimpleField(database_object=self,
                                           aspect='*',
                                           field_locator='country',
                                           dtype=str,
                                           kind=FieldKind.readonly)


        self._fields['code'] = SimpleField(database_object=self,
                                           aspect='*',
                                           field_locator='code_iso',
                                           dtype=str,
                                           kind=FieldKind.readonly)                                           

        self._fields['code_2'] = SimpleField(database_object=self,
                                             aspect='*',
                                             field_locator='code_iso_2',
                                             dtype=str,
                                             kind=FieldKind.readonly)                                           
        

    name = FieldDescriptor('name')
    code = FieldDescriptor('code')
    code_2 = FieldDescriptor('code_2')

    @property
    def country_id(self):
        return self._object_id


