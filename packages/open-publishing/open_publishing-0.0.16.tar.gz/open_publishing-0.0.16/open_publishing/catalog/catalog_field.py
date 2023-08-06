from open_publishing.core.enums import ValueStatus
from open_publishing.core import Field

from . import catalog_types 

class CatalogField(Field):
    def __init__(self,
                 document):
        super(CatalogField, self).__init__(database_object=document,
                                           aspect=":basic" )
        self._is_academic = None
        self._academic = catalog_types.Academic(self._database_object)
        self._non_academic = catalog_types.NonAcademic(self._database_object)

    @property
    def value(self):
        if self.status is ValueStatus.none:
            raise RuntimeError("Accessing to field which is not set")
        else :
            return self._academic if self._is_academic else self._non_academic

    def hard_set(self,
                 value):
        if isinstance(value, catalog_types.Academic):
            self._is_academic = True
            self._academic.hard_set(value)
            self._non_academic = catalog_types.NonAcademic(self._database_object) # Cleaning up non_academic changes
            self._status = ValueStatus.hard
        elif isinstance(value, catalog_types.NonAcademic):
            self._is_academic = False
            self._non_academic.hard_set(value)
            self._academic = catalog_types.Academic(self._database_object) # Cleaning up academic changes
            self._status = ValueStatus.hard
        else :
            raise ValueError("Expected instance of Academic or NonAcademic, got {0}".format(type(value)))

    def update(self,
               gjp):
        master_obj = self._master_object(gjp)
        if self._status is not ValueStatus.hard:
            if 'is_academic' in master_obj:
                if master_obj['is_academic'] == True:
                    self._is_academic = True
                elif master_obj['is_academic'] == False:
                    self._is_academic = False
                else:
                    raise RuntimeError('Unexpected value of is_academic field {0}'.format(master_obj['is_academic']))
                self._status = ValueStatus.soft

        self._academic.update(gjp)
        self._non_academic.update(gjp)
            
    def gjp(self,
            gjp):
        if self._status is not ValueStatus.none:
            if self._status is ValueStatus.hard:
                gjp['is_academic'] = self._is_academic
            if self._is_academic:
                self._academic.gjp(gjp)
            else:
                self._non_academic.gjp(gjp)
