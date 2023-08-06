import datetime

from .core.enums import AssetsModules, AssetsCoverType, ValueStatus
from .core import FieldGroup
from .core import SequenceItem, SequenceField
from .core import FieldDescriptor

from .gjp.stubbornness import RetryNotPossible
from .content import Content

class AssetNotReady(Exception):
    pass

class AssetExpired(RetryNotPossible, Exception):
    pass

class AssetNotFound(RetryNotPossible, Exception):
    pass


class AssetLink(object):
    def __init__(self,
                 ctx,
                 file_id):
        self._ctx = ctx
        self._file_id = file_id

    @property
    def file_id(self):
        return self._file_id

    def download(self):
        status, data, headers = self._ctx.gjp.request_file(self._file_id)
        if status == 'ready':
            return Content(data, headers)
        elif status in ['new', 'inprogress']:
            raise AssetNotReady('Status: {0}'.format(status))
        elif status in ['expired']:
            raise AssetExpired('Status: {0}'.format(status))
        elif status in ['notfound']:
            raise AssetNotFound('Status: {0}'.format(status))
        else:
            ValueError('Unexpected status: {0}'.format(status))

    def save(self,
             filename = None):
        content = self.download()
        with open(filename if filename else content.filename, 'wb') as f:
            f.write(content.data)

class OriginalAssetLink(object):
    def __init__(self,
                 ctx,
                 file_id):
        self._ctx = ctx
        self._file_id = file_id

    @property
    def file_id(self):
        return self._file_id

    def download(self):
        return self._ctx.gjp.download_asset(self._file_id)

    def save(self,
             file_name):
        with open(file_name, 'wb') as f:
            f.write(self.download())


class AssetsGroup(FieldGroup):
    def __init__(self,
                 document):
        super(AssetsGroup, self).__init__(document)
        self._document = document
        self._fields['original'] = OriginalAssetsList(document)

    original = FieldDescriptor('original')


    def _create_file(self, module, asset_priority, **params):
        file_id = self._document.context.gjp.create_file(self._document.document_id,
                                                         module,
                                                         asset_priority,
                                                         **params)
        return AssetLink(self._document.context, file_id)

    def cover(self,
              cover_type,
              asset_priority=None):
        if cover_type not in AssetsCoverType:
            raise ValueError('Asset type should be on of op.assets.cover.*, got {0}'.format(cover_type))
        return self._create_file(AssetsModules.cover, asset_priority=asset_priority, type=cover_type)

    def epub(self,
             channel,
             asset_priority=None,
             exclude_tags=None):
        if not isinstance(channel, str):
            raise ValueError('Channel should be string, got {0}'.format(channel))
        return self._create_file(AssetsModules.epub,
                                 asset_priority=asset_priority,
                                 channel=channel,
                                 exclude_tags=exclude_tags)

    def mobi(self,
             channel,
             asset_priority=None):
        return self._create_file(AssetsModules.mobi, asset_priority=asset_priority, channel=channel)

    def ibooks(self,
             asset_priority=None):
        return self._create_file(AssetsModules.ibooks, asset_priority=asset_priority)

    def pdf(self,
            asset_priority=None):
        return self._create_file(AssetsModules.pdf, asset_priority=asset_priority)

    def pod(self,
            asset_priority=None):
        return self._create_file(AssetsModules.pod, asset_priority=asset_priority)
    
    def audiobook(self,
            asset_priority=None):
        return self._create_file(AssetsModules.audiobook, asset_priority=asset_priority)

    def software(self,
            asset_priority=None):
        return self._create_file(AssetsModules.software, asset_priority=asset_priority)

    def extract(self,
                asset_priority=None,
                supports=None):
        return self._create_file(AssetsModules.extract, asset_priority=asset_priority, supports=supports)

    def availability(self,
                     **kwargs):
        for key in kwargs:
            if key not in ['cover', 'epub', 'mobi', 'ibooks', 'pdf', 'pod', 'extract', 'audiobook', 'software']:
                raise TypeError("availability() got an unexpected keyword argument '{}'".format(key))
        modules = []
        params = {}
        for module, module_params in kwargs.items():
            if params is not None:
                modules.append(module)
                params.update({module + '_' + key : value for key, value in module_params.items()})

        return self._document.context.gjp.check_file(self._document.document_id,
                                                     modules,
                                                     **params)

class ImageAttributes(object):
    def __init__(self,
                 width,
                 height):
        self._width = width
        self._height = height

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @classmethod
    def from_gjp(cls, gjp, database_object):
        if gjp is not None:
            width = gjp['width']
            height = gjp['height']
            return cls(width,
                       height)
        else:
            return None
        
    
class OriginalAsset(SequenceItem):
    def __init__(self,
                 ctx,
                 file_name,
                 file_type,
                 type_specification,
                 tags,
                 distribution_tags,
                 file_id,
                 md5,
                 timestamp,
                 image_attributes):
        super(OriginalAsset, self).__init__(ValueStatus.soft)
        self._ctx = ctx
        self._file_name = file_name
        self._file_type = file_type
        self._type_specification = type_specification
        self._tags = tags
        self._distribution_tags = distribution_tags
        self._file_id = file_id
        self._md5 = md5
        self._timestamp = timestamp
        self._image_attributes = image_attributes

    @property
    def file_type(self):
        return self._file_type

    @property
    def type_specification(self):
        return self._type_specification

    @property
    def distribution_tags(self):
        return self._distribution_tags

    @property
    def tags(self):
        return self._tags

    @property
    def filename(self):
        return self._file_name

    @property
    def md5(self):
        return self._md5

    @property
    def link(self):
        return OriginalAssetLink(self._ctx, self._file_id)

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def image_attributes(self):
        return self._image_attributes

    @classmethod
    def from_gjp(cls, gjp, database_object):
        file_name = gjp['original_filename']
        file_id = gjp['id']
        file_type = gjp['type']
        type_specification = gjp['type_specification']
        tags = gjp['tags']
        distribution_tags = gjp['distribution_tags']
        md5 = gjp['md5']
        timestamp = datetime.datetime.fromtimestamp(gjp['upload_timestamp'])
        image_attributes = ImageAttributes.from_gjp(gjp['image_attributes'], database_object)
        return cls(database_object.context,
                   file_name,
                   file_type,
                   type_specification,
                   tags,
                   distribution_tags,
                   file_id,
                   md5,
                   timestamp,
                   image_attributes)


class OriginalAssetsList(SequenceField):
    _item_type = OriginalAsset

    def __init__(self,
                 document):
        super(OriginalAssetsList, self).__init__(document,
                                                 'uploaded_files',
                                                 'uploaded_files')
