from open_publishing.core.enums import ValueStatus, FieldKind, Country
from open_publishing.core import Field, DatabaseObject, SimpleField, FieldDescriptor
from open_publishing.extendable_enum_field import ExtendableEnumField

class Imprint(DatabaseObject):
    _object_class = 'realm_imprint'

    def __init__(self,
                 context,
                 imprint_id):
        super(Imprint, self).__init__(context,
                                      imprint_id)

        self._fields['imprint_name'] = SimpleField(database_object=self,
                                                 aspect='imprint_name',
                                                 field_locator='imprint_name',
                                                 dtype=str,
                                                 kind=FieldKind.readonly)

        self._fields['publisher_name'] = SimpleField(database_object=self,
                                                aspect='publisher_name',
                                                field_locator='publisher_name',
                                                dtype=str,
                                                kind=FieldKind.readonly)

        self._fields['publisher_id'] = SimpleField(database_object=self,
                                                   aspect='isbn_publisher_identifier',
                                                   field_locator='isbn_publisher_identifier',
                                                   dtype=str,
                                                   kind=FieldKind.readonly)

        self._fields['publisher_city'] = SimpleField(database_object=self,
                                                     aspect='*',
                                                     field_locator='publisher_city',
                                                     dtype=str,
                                                     kind=FieldKind.readonly)                                           


        self._fields['publisher_country'] = ExtendableEnumField(database_object=self,
                                                                aspect='*',
                                                                field_locator='publisher_country_id',
                                                                dtype=Country,
                                                                nullable=True,
                                                                serialized_null=0,
                                                                kind=FieldKind.readonly)
        

    imprint_name = FieldDescriptor('imprint_name')
    publisher_name = FieldDescriptor('publisher_name')
    publisher_id = FieldDescriptor('publisher_id')
    publisher_city = FieldDescriptor('publisher_city')
    publisher_country = FieldDescriptor('publisher_country')

    @property
    def imprint_id(self):
        return self._object_id

    def __repr__(self):
        return '<Imprint {0}>'.format(self.imprint_name)

    def __str__(self):
        return '{0}'.format(self.imprint_name)
    
class ImprintField(Field):
    def __init__(self,
                 document):
        super(ImprintField, self).__init__(database_object=document,
                                           aspect='imprint.*')
        self._imprint_id = None
    
    @property
    def value(self):
        if self.status is ValueStatus.none:
            raise RuntimeError('Accessing to field which is not set')
        else :
            if self._imprint_id == 0:
                return None
            else:
                for imprint in self.database_object.context.imprints:
                    if imprint.imprint_id == self._imprint_id:
                        return imprint
                raise RuntimeError('Somehow imprint_id not in available imprints, imprint_id: {0}'.format(self._imprint_id))

    def hard_set(self,
                 value):
        new_id = None
        if isinstance(value, str):
            for imprint in self.database_object.context.imprints:
                if value == imprint.imprint_name:
                    new_id = imprint.imprint_id
        elif isinstance(value, Imprint):
            if value in self.database_object.context.imprints:
                new_id = value.imprint_id
        else:
            raise TypeError('Expected str or Imprint, got: {0}'.format(type(value)))

        if new_id:
            self._imprint_id = new_id
            self._status = ValueStatus.hard
        else:
            raise ValueError('Not available imprints used : {0}'.format(value))

    def update(self,
               gjp):
        if self._status is not ValueStatus.hard :
            value = self._master_object(gjp)
            for fname in ['imprint', 'realm_imprint_id']:
                if fname in value:
                    value = value[fname]
                else :
                    value = None
                    break
            if value is not None:
                self._imprint_id = value
                self._status = ValueStatus.soft
            
    def gjp(self,
            gjp):
        if self._status is ValueStatus.hard:
            if 'imprint' not in gjp:
                gjp['imprint'] = {}
            gjp['imprint']['realm_imprint_id'] = self._imprint_id

