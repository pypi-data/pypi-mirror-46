from open_publishing.core import DatabaseObjectsList

from open_publishing.core import SimpleField
from open_publishing.core import FieldDescriptor
from open_publishing.core import DatabaseObject

class DocumentSeries(DatabaseObject):
    _object_class = 'document_series'
    
    def __init__(self,
                 context,
                 document_series_id):
        super(DocumentSeries, self).__init__(context,
                                             document_series_id)

        self._fields['title'] = SimpleField(database_object=self,
                                            aspect='*',
                                            field_locator='title',
                                            dtype=str)

        self._fields['number'] = SimpleField(database_object=self,
                                             aspect='*',
                                             field_locator='number',
                                             dtype=str,
                                             nullable=True)
        


    title = FieldDescriptor('title')
    number = FieldDescriptor('number')

    @property
    def document_series_id(self):
        return self._object_id


class SeriesList(DatabaseObjectsList):
    _database_object_type = DocumentSeries

    def __init__(self,
                 document):
        super(SeriesList, self).__init__(database_object=document,
                                         aspect='series.*',
                                         list_locator = 'series')
        self._document = document

    def add(self,
            title,
            number):
        res = self._database_object._context.gjp.create(DocumentSeries._object_class,
                                                        document_id=self._document.document_id,
                                                        title=title,
                                                        number=number)


        series_id = DocumentSeries.id_from_guid(res["GUID"])
        self._objects[series_id] = DocumentSeries(context = self._document._context,
                                                  document_series_id = series_id)

        self._ids.append(series_id)

