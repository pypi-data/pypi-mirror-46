from open_publishing.country import CountryInfo
from open_publishing.core.enums import Country

class Countries(object):
    def __init__(self,
                 ctx):
        self._ctx = ctx
        self._refs = set() #TODO: Consider using weakref

    def load(self,
             guid = None,
             country_id = None,
             code = None,
             enum = None,
             fetch = True):
        if len([x for x in [guid, country_id, code, enum] if x is not None]) != 1:
            raise TypeError('Exectly one of guid/document_id/ean/isbn should be specified')
        if guid is not None:
            country_id = CountryInfo.id_from_guid(guid)
        elif code is not None:
            country_id = self._ctx.gjp.resolve_enum(dtype=Country, code=code).internal_id
        elif enum is not None:
            country_id = self._ctx.gjp.resolve_enum(dtype=Country, enum=enum).internal_id
            
        doc = CountryInfo(self._ctx,
                          country_id)
        if fetch:
            doc._fetch(["*"])
        return doc
        

    def flush(self):
        refs = self._refs.copy()
        for ref in refs:
            ref.flush()
        self._refs = set()

    def _add_to_changed(self,
                        database_object):
        self._refs.add(database_object)

    def _remove_from_changed(self,
                             database_object):
        if database_object in self._refs:
            self._refs.remove(database_object)
