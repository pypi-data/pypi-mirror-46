import random
import string
import datetime
import os
import mimetypes
import json
import collections
import requests
import jsonschema
import pkg_resources

from open_publishing.core.enums import DocumentStatus, Language, Country, VLBCategory
from open_publishing.core.enums import License, PreviewFileType, FileType, ContributorRole, BisacCode, ThemaCode, UsersSearchType
from open_publishing.core.enums import OnixStatus
from .stubbornness import stubborn, RetryNotPossible

class ObjectHasChanged(RetryNotPossible, Exception):
    pass

class ObjectNotFound(RetryNotPossible, Exception):
    pass

class AssetCreationError(RetryNotPossible, Exception):
    pass

class TemporaryNotAvailable(Exception):
    pass

class GJP():
    def __init__(self,
                 ctx,
                 validate_json):
        self._ctx = ctx
        self._validate_json = validate_json
        self._enum_cache = {}
        self._log = self._ctx.log.getChild('gjp')
        self._session = requests.Session()

    @property
    def session(self):
        return self._session

    @property
    def log(self):
        return self._log

    def update(self, object_class, object_id, version, gjp):
        """ General method to update a gjp object """
        path = '/resource/v2/'
        data = [{
            'GUID': '{object_class}.{object_id}'.format(object_class=object_class,
                                                        object_id=object_id),
            'VERSION': version,
        }]
        data[0].update(gjp)
        headers = {
            'Content-type': 'application/json',
            'Accept': 'text/plain',
            'Authorization': 'Bearer ' + self._ctx.auth_context.auth_token
            }

        response = self._session.put(self._ctx.host + path,
                                     data=json.dumps(data),
                                     headers=headers,
                                     **self._ctx.requests_kwargs)
        self._check_response(response, self._validate_json)

    def update_chunk(self, gjp_list):
        """ General method to update a gjp object """
        path = '/resource/v2/'
        data = []
        for gjp_info in gjp_list:
            gjp = gjp_info['gjp'].copy()
            gjp['GUID'] = gjp_info['guid']
            gjp['VERSION'] = gjp_info['version']
            data.append(gjp)
        headers = {
            'Content-type': 'application/json',
            'Accept': 'text/plain',
            'Authorization': 'Bearer ' + self._ctx.auth_context.auth_token,
            }
        response = self._session.put(self._ctx.host + path,
                                     data=json.dumps(data),
                                     headers=headers,
                                     **self._ctx.requests_kwargs)
        self._check_response(response, self._validate_json)

    @stubborn
    def get(self, object_class, object_id, fields, params=None):
        """ General method to retrieve a gjp object """
        if object_id is None:
            path = '/resource/v2/{object_class}[{fields}]'.format(object_class=object_class,
                                                                  fields=','.join(fields))
        else:
            path = '/resource/v2/{object_class}.{object_id}[{fields}]'.format(object_class=object_class,
                                                                              object_id=object_id,
                                                                              fields=','.join(fields))

        headers = {
            'Authorization': 'Bearer ' + self._ctx.auth_context.auth_token,
        }
        response = self._session.get(self._ctx.host + path,
                                     params=params,
                                     headers=headers,
                                     **self._ctx.requests_kwargs)
        return self._check_response(response, self._validate_json)['OBJECTS']

    @stubborn
    def get_chunk(self, guids, fields):
        """ General method to retrieve a gjp objects in chunk """
        if len(guids) == 0:
            return {}
        fields_str = ','.join(fields)
        path = '/resource/v2/' + ','.join(['{guid}[{fields}]'.format(guid=guid,
                                                                     fields=fields_str) for guid in set(guids)])
        headers = {
            'Authorization': 'Bearer ' + self._ctx.auth_context.auth_token,
            }
        self.log.debug(path + '&' + ','.join(['='.join(item) for item in list(params.items())]))
        response = self._session.get(self._ctx.host + path,
                                     headers=headers,
                                     **self._ctx.requests_kwargs)
        return self._check_response(response, self._validate_json)['OBJECTS']

    def delete(self, object_class, object_id):
        """ General method to delete a gjp object """
        path = '/resource/v2/{object_class}.{object_id}'.format(object_class=object_class,
                                                                object_id=object_id)
        headers = {
            'Authorization': 'Bearer ' + self._ctx.auth_context.auth_token,
            }
        response = self._session.delete(self._ctx.host + path,
                                        headers=headers,
                                        **self._ctx.requests_kwargs)
        self._check_response(response, self._validate_json)

    def create(self, object_class, **fields):
        """ General method to create a gjp object """
        data = [{
            'GUID': '{0}.'.format(object_class),
            'VERSION': 0,
            }]
        data[0].update(fields)
        headers = {
            'Content-type': 'application/json',
            'Accept': 'text/plain',
            'Authorization': 'Bearer ' + self._ctx.auth_context.auth_token,
            }
        response = self._session.post(self._ctx.host + '/resource/v2',
                                      data=json.dumps(data),
                                      headers=headers,
                                      **self._ctx.requests_kwargs)
        gjp = self._check_response(response, self._validate_json)
        guid = gjp['RESULTS'][0]
        return gjp['OBJECTS'][guid]

    @staticmethod
    def _encode_params(params):
        res = {}
        for key, value in list(params.items()):
            if isinstance(value, str):
                res[key] = value.encode('utf-8')
            else:
                res[key] = value
        return res

    def documents_search(self,
                         query=None,
                         status=None,
                         created=None,
                         language=None,
                         page_count=None,
                         license=None):
        """ RPC to search entities"""
        params = {
            'display': 0,
            }
        headers = {
            'Authorization': 'Bearer ' + self._ctx.auth_context.auth_token,
            }
        if isinstance(query, str):
            params['query'] = query
        elif query is None:
            pass
        else:
            raise ValueError('Invalid `query`')

        if status is not None:
            if not isinstance(status, collections.Iterable):
                status = [status]
            for st in status:
                if st not in DocumentStatus:
                    raise ValueError("Ivalid `status`")
            if DocumentStatus.new in status:
                params['new_status'] = 'new'
            if DocumentStatus.published in status:
                params['published_status'] = 'published'
            if DocumentStatus.unpublished in status:
                params['unpublished_status'] = 'unpublished'
            if DocumentStatus.deleted in status:
                params['del_status'] = 'deleted'

        if created is None:
            pass
        elif isinstance(created, datetime.date):
            params['created-date-from'] = created.strftime("%Y-%m-%d")
            params['created-date-to'] = created.strftime("%Y-%m-%d")
        elif isinstance(created, tuple) and len(created) == 2:
            for date in created:
                if not (isinstance(date, datetime.date) or date is None):
                    raise ValueError("Invalid `created`")
            if created[0] is not None:
                params['created-date-from'] = created[0].strftime("%Y-%m-%d")
            if created[1] is not None:
                params['created-date-to'] = created[1].strftime("%Y-%m-%d")
        else:
            raise ValueError("Invalid `created`")

        if language is None:
            pass
        elif language in Language:
            params['language_id'] = self.resolve_enum(Language, enum=language).internal_id
        elif isinstance(language, str) and len(language) == 3:
            params['language_id'] = self.resolve_enum(Language, code=language).internal_id
        else:
            raise ValueError("Invalid `language`")

        def page_tuple_to_range(t):
            def count_to_str(count):
                if count is None:
                    return ""
                if isinstance(count, int):
                    return str(count)
                raise ValueError("Invalid page range")

            if t is None:
                return ""
            if t == (None, None):
                return ""
            if isinstance(t, int):
                return str(t)
            if isinstance(t, tuple) and len(t) == 2:
                return count_to_str(t[0]) + "-" + count_to_str(t[1])
            raise ValueError("Invalid page range")

        if page_count is None:
            pass
        elif isinstance(page_count, int):
            params['page-count'] = str(page_count)
        elif isinstance(page_count, tuple) and len(page_count) == 2:
            params['page-count'] = page_tuple_to_range(page_count)
        elif isinstance(page_count, list):
            _page_count = []
            for pc in page_count:
                _page_count.append(page_tuple_to_range(pc))
            params['page-count'] = ",".join(_page_count)
        else:
            raise ValueError("Invalid `page_count`")


        if license is None:
            pass
        elif license in License:
            params['license'] = license.identifier
        else:
            raise ValueError("Invalid `license`")

        response = self._session.get(self._ctx.host + '/rpc/resource_search/admin-document/',
                                     params=self._encode_params(params),
                                     headers=headers,
                                     **self._ctx.requests_kwargs)
        return self._check_response(response)['OBJECTS']

    def users_search(self,
                     query=None,
                     search_type=None):
        """ RPC to search entities"""
        headers = {
            'Authorization': 'Bearer ' + self._ctx.auth_context.auth_token,
            }
        params = {
            'display': 0,
            }
        data = {}
        if isinstance(query, str):
            data['query'] = query
        elif query is None:
            pass
        else:
            raise ValueError('Invalid `query`')

        if search_type is None:
            pass
        elif search_type in UsersSearchType:
            data['search-type'] = search_type.identifier
        else:
            raise ValueError('Invalid `search_type`')

        response = self._session.get(self._ctx.host + '/rpc/resource_search/admin-user/',
                                     params=self._encode_params(params),
                                     headers=headers,
                                     data=data,
                                     **self._ctx.requests_kwargs)
        return self._check_response(response)['OBJECTS']

    def _upload(self, file_name, upload_module, upload_method, alias_name=None, rpc_parameter=None):

        headers = {
            'Authorization': 'Bearer ' + self._ctx.auth_context.auth_token,
        }
        params = {
            "method" : upload_method,
        }

        if alias_name is None:
            alias_name = file_name
        files = {'file': (alias_name, open(file_name, 'rb'), mimetypes.guess_type(file_name))}

        response = self._session.put(self._ctx.host + '/rpc/' + upload_module,
                                     data=rpc_parameter,
                                     files=files,
                                     params=params,
                                     headers=headers,
                                     **self._ctx.requests_kwargs)

        self._check_response(response)


    def preview_upload(self, document_id, file_name, preview_file_type):
        if preview_file_type not in PreviewFileType:
            raise ValueError("file_type should be one of op.files.filetype.*")

        self._upload(
            file_name=file_name,
            upload_module="document_admin_preview_upload",
            upload_method="upload",
            rpc_parameter={
                "file_type":preview_file_type,
                "source_type":"document",
                "reference_id":document_id}
            )


    def upload_asset(self, document_id, file_name, file_type):

        if file_type not in FileType:
            raise ValueError("file_type should be one of op.files.filetype.*")

        self._upload(
            file_name=file_name,
            upload_module="document_admin_upload",
            upload_method="upload",
            rpc_parameter={
                "file_type":file_type.identifier,
                "document_id":document_id}
            )


    def download_asset(self, file_id):
        headers = {
            'Authorization': 'Bearer ' + self._ctx.auth_context.auth_token,
        }
        params = {
            'method' : 'download',
            'file_id' : file_id
            }
        response = self._session.get(self._ctx.host + '/rpc/document_admin_upload',
                                     params=params,
                                     headers=headers,
                                     **self._ctx.requests_kwargs)
        self._check_status_code(response)
        return response.content

    def upload_avatar(self, user_id, file_name):

        self._upload(
            file_name=file_name,
            upload_module="upload_picture",
            upload_method="upload_picture",
            rpc_parameter={
                "response": "gjp",
                "source_type": "user",
                "reference_id": user_id}
            )

    def enqueue_import(self, file_name, alias_name):
        self._upload(
            file_name=file_name,
            alias_name=alias_name,
            upload_module="admin_asset_upload",
            upload_method="upload",
            rpc_parameter={
                "filename": alias_name or file_name,
                "response": "gjp"}
        )

    def download_from_archive(self, url):
        headers = {
            'Authorization': 'Bearer ' + self._ctx.auth_context.auth_token,
            }
        response = self._session.get(url,
                                     headers=headers,
                                     **self._ctx.requests_kwargs)
        self._check_status_code(response)
        return response.content

    def _user_rpc(self, data):
        headers = {
            'Authorization': 'Bearer ' + self._ctx.auth_context.auth_token,
            }
        response = self._session.put(self._ctx.host + '/rpc/users',
                                     data=data,
                                     headers=headers,
                                     **self._ctx.requests_kwargs)
        return self._check_response(response)

    def _price_periods_rpc(self, data):
        headers = {
            'Authorization': 'Bearer ' + self._ctx.auth_context.auth_token,
            }
        response = self._session.get(self._ctx.host + '/rpc/price_periods',
                                     data=data,
                                     headers=headers,
                                     **self._ctx.requests_kwargs)
        return self._check_response(response)

    def get_price_periods(
            self,
            document_id,
            country,
            date_from=None,
            date_to=None,
            include_campains=True,
            remove_outdated=None
    ):
        data = {
            'document_id': document_id,
        }

        if country in Country:
            data['country_ids'] = self.resolve_enum(Country, enum=country).internal_id
        elif isinstance(country, str):
            data['country_ids'] = self.resolve_enum(Country, code=country).internal_id
        else:
            raise ValueError("Invalid `country`")

        if date_from:
            data['date_from'] = date_from

        if date_to:
            data['date_to'] = date_to

        if include_campains:
            data['include_campains'] = True

        if remove_outdated is not None:
            data['remove_outdated'] = remove_outdated

        return self._price_periods_rpc(data)['OBJECTS'][0]

    def reset_password(self, user_id):
        data = {
            'method': 'send_passwd',
            'user_id': user_id,
            }
        self._user_rpc(data)

    def set_password(self, user_id, password):
        data = {
            'method': 'change_user_passwd',
            'user_id': user_id,
            'changepassword': password,
            }
        self._user_rpc(data)

    def create_user(self,
                    first_name,
                    last_name,
                    email):
        data = {
            'method': 'create_user',
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            }
        return self._user_rpc(data)['user_id']

    def set_document_external_availability(self, name, country_code, document_id, publication_type,
                                           availability_status, availability, in_stock_quantity,
                                           price_cent, currency_code, shop_url):
        data = {
            'method': 'report',
            'name': name,
            'country_code': country_code,
            'document_id': document_id,
            'publication_type': publication_type,
            'availability_status': availability_status,
            'availability': availability,
            'in_stock_quantity': in_stock_quantity,
            'shop_url': shop_url
        }

        if price_cent is not None:
            data['price_cent'] = price_cent
        if currency_code is not None:
            data['currency_code'] = currency_code

        self._document_external_availability_rpc(data)

    def _document_external_availability_rpc(self, data):
        headers = {
            'Authorization': 'Bearer ' + self._ctx.auth_context.auth_token,
            }
        response = self._session.put(self._ctx.host + '/rpc/document_external_availability',
                                     data=data,
                                     headers=headers,
                                     **self._ctx.requests_kwargs)
        return self._check_response(response)

    def set_document_external_salesrank(self, name, country_code, document_id, publication_type, salesrank):
        data = {
            'method': 'report',
            'name': name,
            'country_code': country_code,
            'document_id': document_id,
            'publication_type': publication_type
        }

        if salesrank is not None:
            data['salesrank'] = salesrank

        self._document_external_salesrank_rpc(data)

    def _document_external_salesrank_rpc(self, data):
        headers = {
            'Authorization': 'Bearer ' + self._ctx.auth_context.auth_token,
            }
        response = self._session.put(self._ctx.host + '/rpc/document_external_salesrank',
                                     data=data,
                                     headers=headers,
                                     **self._ctx.requests_kwargs)
        return self._check_response(response)

    def set_document_external_rating(self, name, country_code, document_id, publication_type, average_rating, review_count, shop_review_url):
        data = {
            'method': 'report',
            'name': name,
            'country_code': country_code,
            'document_id': document_id,
            'publication_type': publication_type,
            'review_count': review_count,
            'shop_review_url': shop_review_url
        }

        if average_rating is not None:
            data['average_rating'] = average_rating

        self._document_external_rating_rpc(data)

    def _document_external_rating_rpc(self, data):
        headers = {
            'Authorization': 'Bearer ' + self._ctx.auth_context.auth_token,
            }
        response = self._session.put(self._ctx.host + '/rpc/document_external_rating',
                                     data=data,
                                     headers=headers,
                                     **self._ctx.requests_kwargs)
        return self._check_response(response)

    def _document_rpc(self, data):
        headers = {
            'Authorization': 'Bearer ' + self._ctx.auth_context.auth_token,
            }
        response = self._session.put(self._ctx.host + '/rpc/document',
                                     data=data,
                                     headers=headers,
                                     **self._ctx.requests_kwargs)
        return self._check_response(response)

    def _testdata_rpc(self, data):
        headers = {
            'Authorization': 'Bearer ' + self._ctx.auth_context.auth_token,
            }
        response = self._session.put(self._ctx.host + '/rpc/testdata',
                                     data=data,
                                     headers=headers,
                                     **self._ctx.requests_kwargs)
        return self._check_response(response)

    def set_display_mode(self, document_id, mode):
        data = {
            'method': 'document_preview_display_mode',
            'document_id': document_id,
            'display_mode': mode.identifier,
            }
        self._document_rpc(data)

    def set_toc_visible(self, document_id, mode):
        data = {
            'method': 'document_preview_display_mode',
            'document_id': document_id,
            'toc_visible': mode.identifier,
            }
        self._document_rpc(data)

    def publish_document(self,
                         document_id):
        data = {
            'method': 'publish',
            'skip-checks': 'yes',
            'document_id': document_id,
            }
        self._document_rpc(data)

    def delete_document(self,
                        document_id):
        data = {
            'method': 'delete',
            'document_id': document_id,
            }
        self._document_rpc(data)

    def undelete_document(self,
                          document_id):
        data = {
            'method': 'undelete',
            'document_id': document_id,
            }
        self._document_rpc(data)

    def final_check_ok(self,
                       document_id):
        data = {
            'method': 'final_check_ok',
            'document_id': document_id,
            }
        self._document_rpc(data)

    def testdata_publish_document(self,
                                  document_id):
        data = {
            'method': 'publish',
            'document_id': document_id,
            }
        self._testdata_rpc(data)

    def testdata_create_license(self,
                                short_name=None):
        random_string = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(6))
        data = {
            'method': 'create_test_license',
            'short_name': short_name if short_name else 'test-' + random_string
            }
        return self._testdata_rpc(data)['short_name']

    def testdata_init_testcase(self,
                               testcase_id,
                               testrun_id):
        data = {
            'method': 'init_testcase',
            'testcase_id': testcase_id,
            'testrun_id': testrun_id,
            }
        self._testdata_rpc(data)

    def unpublish_document(self,
                           document_id):
        data = {
            'method': 'unpublish',
            'document_id': document_id,
            }
        self._document_rpc(data)

    def assign_isbn(self,
                    document_id,
                    isbn_type,
                    ean=None):
        data = {
            'type': isbn_type,
            'document_id': document_id,
        }
        if ean:
            data['method'] = 'assign_isbn'
            data['ean'] = ean
        else:
            data['method'] = 'assign_pool_isbn'
        self._document_rpc(data)

    def recalculate_prices(self,
                           document_id):
        data = {
            'method': 'recalculate_prices',
            'document_id': document_id,
            }
        self._document_rpc(data)

    @stubborn
    def resolve_email(self, email):
        headers = {
            'Authorization': 'Bearer ' + self._ctx.auth_context.auth_token,
            }
        data = {}
        data['method'] = 'resolve_email'
        data['email'] = email
        response = self._session.put(self._ctx.host + '/api/users',
                                     data=data,
                                     headers=headers,
                                     **self._ctx.requests_kwargs)
        return self._check_response(response)['result']

    @stubborn
    def resolve_ean(self, ean):
        headers = {
            'Authorization': 'Bearer ' + self._ctx.auth_context.auth_token,
            }
        data = {}
        data['method'] = 'resolve_ean'
        data['ean'] = ean

        response = self._session.put(self._ctx.host + '/api/documents',
                                     data=data,
                                     headers=headers,
                                     **self._ctx.requests_kwargs)
        return self._check_response(response)['result']

    def vlb_to_bisac(self, category_id):
        headers = {
            'Authorization': 'Bearer ' + self._ctx.auth_context.auth_token,
            }
        data = {}
        data["category_id"] = category_id
        data["method"] = "vlb_to_bisac"
        response = self._session.get(self._ctx.host + '/api/enumerations',
                                     data=data,
                                     headers=headers,
                                     **self._ctx.requests_kwargs)
        return self._check_response(response)['result']

    def _enumerations(self, data):
        headers = {
            'Authorization': 'Bearer ' + self._ctx.auth_context.auth_token,
            }
        response = self._session.get(self._ctx.host + '/api/enumerations',
                                     data=data,
                                     headers=headers,
                                     **self._ctx.requests_kwargs)
        return self._check_response(response)['result']

    @stubborn
    def resolve_enum(self,
                     dtype,
                     enum=None,
                     code=None,
                     internal_id=None):
        data = {}
        if dtype is Language:
            data['method'] = 'language'
        elif dtype is Country:
            data['method'] = 'country'
        elif dtype is VLBCategory:
            data['method'] = 'vlb_kat'
        elif dtype is ContributorRole:
            data['method'] = 'contributor_role'
        elif dtype is BisacCode:
            data['method'] = 'bisac_code'
        elif dtype is ThemaCode:
            data['method'] = 'thema_code'
        else:
            raise ValueError('Unexpected dtype {0}'.format(dtype))

        if enum is not None:
            if enum in dtype:
                data['code'] = enum.identifier
            else:
                raise ValueError('expected one of dtype, got {}'.format(enum))
        elif code is not None:
            data['code'] = code
        elif internal_id is not None:
            data['id'] = internal_id
        else:
            raise ValueError('At least one of enum, iso_code and internal_id should be set, method: {0}'.format(data['method']))

        cache_key = (data.get('code', None), data.get('id', None))
        if dtype not in self._enum_cache:
            self._enum_cache[dtype] = {}
        cache = self._enum_cache[dtype]

        if cache_key not in cache:
            result = self._enumerations(data)
            IDs = collections.namedtuple("IDs", ['internal_id', 'enum', 'code'])
            cache[cache_key] = IDs(result['id'],
                                   dtype.extend(result['code']),
                                   result['code'])
        return cache[cache_key]

    @stubborn
    def list_imprints(self):
        data = {
            'method': 'list_imprints',
            }
        result = self._enumerations(data)
        return result['available_imprints']

    @stubborn
    def list_genres(self):
        data = {
            'method': 'list_genres',
            }
        result = self._enumerations(data)
        return result['available_genres']

    @stubborn
    def list_brands(self):
        data = {
            'method': 'list_brands',
            }
        result = self._enumerations(data)
        return result['available_brands']

    @stubborn
    def list_countries(self):
        data = {
            'method': 'list_countries',
            }
        result = self._enumerations(data)
        return result['countries']

    @stubborn
    def get_me(self):
        path = '/rpc/me'
        headers = {
            'Authorization': 'Bearer ' + self._ctx.auth_context.auth_token
        }
        response = self._session.get(self._ctx.host + path,
                                     headers=headers,
                                     **self._ctx.requests_kwargs)
        return self._check_response(response)['RESULT']

    @stubborn
    def fetch_events(self,
                     method,
                     event_types=None,
                     references=None,
                     from_timestamp=None,
                     to_timestamp=None,
                     resumption_token=None):
        path = '/rpc/event'
        headers = {
            'Authorization': 'Bearer ' + self._ctx.auth_context.auth_token,
            }
        params = {
            'method': method,
            'event_types': event_types,
            'refGUID': references,
            'from': from_timestamp,
            'to':  to_timestamp,
            'resumption_token': resumption_token,
            }
        response = self._session.get(self._ctx.host + path,
                                     params=params,
                                     headers=headers,
                                     **self._ctx.requests_kwargs)
        return self._check_response(response)['result']

    def trigger_event(self,
                      guid,
                      target,
                      action,
                      type,
                      note=None,
                      uuid=None):
        path = '/rpc/event'
        headers = {
            'Authorization': 'Bearer ' + self._ctx.auth_context.auth_token,
            }
        params = {
            'method': 'trigger',
            'refGUID': guid,
            'target': target.identifier,
            'action': action.identifier,
            'type':  type.identifier,
            'note': note,
            'uuid': uuid
            }
        response = self._session.get(self._ctx.host + path,
                                     params=params,
                                     headers=headers,
                                     **self._ctx.requests_kwargs)
        self._check_response(response)

    def log_event(self,
                  guid,
                  target,
                  action,
                  type,
                  result,
                  note=None):
        path = '/rpc/event'
        headers = {
            'Authorization': 'Bearer ' + self._ctx.auth_context.auth_token,
            }
        params = {
            'method': 'log',
            'refGUID': guid,
            'target': target.identifier,
            'action': action.identifier,
            'type':  type.identifier,
            'result': result.identifier,
            'note': note,
            }
        response = self._session.get(self._ctx.host + path,
                                     params=params,
                                     headers=headers,
                                     **self._ctx.requests_kwargs)
        self._check_response(response)

    def request_onix(self,
                     products,
                     status=OnixStatus.current,
                     onix_style=None,
                     onix_type=None,
                     contract_type=None,
                     country_codes=None,
                     codelist_issue=None,
                     subject_keyword_in_separate_tag=False,
                     sales_rights_country_codes=None):
        path = '/rpc/onix'
        params = {}
        headers = {
            'Authorization': 'Bearer ' + self._ctx.auth_context.auth_token,
            'Content-Type': 'application/json',
            }
        if onix_style is not None:
            params['style'] = onix_style.identifier
        if onix_type is not None:
            params['onix_type'] = onix_type.identifier
        if contract_type:
            params['contract_type'] = contract_type
        if country_codes:
            params['country_codes'] = country_codes
        if codelist_issue is not None:
            params['codelist_issue'] = codelist_issue
        if subject_keyword_in_separate_tag:
            params['subject_keyword_in_separate_tag'] = 'yes'
        if sales_rights_country_codes is not None:
            params['sales_rights_country_codes'] = sales_rights_country_codes
        params['publication_status'] = status.identifier

        resources = []
        for product in products:
            resource = {
                'document_id': product.document_id,
                'publication_type': product.publication_type.identifier,
            }
            if product.availability is not None:
                resource['availability'] = product.availability
            resources.append(resource)

        data = {'resources': resources}
        response = self._session.get(self._ctx.host + path,
                                     params=params,
                                     headers=headers,
                                     data=json.dumps(data),
                                     **self._ctx.requests_kwargs)
        self._check_status_code(response)
        if 'text/json' in response.headers.get('Content-Type', ''):
            self._check_response(response)
        return response.content, response.headers

    def allocate_isbns_block(self,
                             prefix):
        path = '/rpc/isbn'
        headers = {
            'Authorization': 'Bearer ' + self._ctx.auth_context.auth_token,
            }
        params = {
            'method': 'import',
            'prefix': prefix,
            }
        response = self._session.get(self._ctx.host + path,
                                     params=params,
                                     headers=headers,
                                     **self._ctx.requests_kwargs)
        self._check_response(response)

    def accept_license(self,
                       document_id,
                       user_id,
                       license_short_name,
                       ip_address,
                       option):
        path = '/rpc/licenses'
        headers = {
            'Authorization': 'Bearer ' + self._ctx.auth_context.auth_token,
            }
        params = {
            'method': 'accept_api',
            'document_id': document_id,
            'user_id': user_id,
            'ip': ip_address,
            'option': option,
            'license_text_short_name' : license_short_name,
            }

        response = self._session.get(self._ctx.host + path,
                                     params=params,
                                     headers=headers,
                                     **self._ctx.requests_kwargs)
        self._check_response(response)

    def create_file(self,
                    document_id,
                    asset_module,
                    asset_priority=None,
                    supports=None,
                    exclude_tags=None,
                    include_tags=None,
                    **kwargs):
        path = '/rpc/asset_converter_control'
        headers = {
            'Authorization': 'Bearer ' + self._ctx.auth_context.auth_token,
            }
        params = {
            'method': 'create',
            'document_id': document_id,
            'module' : asset_module.identifier,
            }
        if asset_priority:
            params['asset-priority'] = asset_priority
        if supports is not None:
            params['supports'] = ','.join(supports)
        if exclude_tags is not None:
            params['exclude-tags'] = ','.join(exclude_tags)
        if include_tags is not None:
            params['include-tags'] = ','.join(include_tags)
        params.update(kwargs)

        response = self._session.get(self._ctx.host + path,
                                     params=params,
                                     headers=headers,
                                     **self._ctx.requests_kwargs)

        return self._check_response(response)['result']['file_id']

    def request_file(self,
                     file_id):
        path = '/rpc/asset_converter_download'
        params = {
            'method': 'download',
            'file_id': file_id,
        }

        response = self._session.get(self._ctx.host + path,
                                     params=params,
                                     **self._ctx.requests_kwargs)

        self._check_status_code(response)
        if response.headers['content-type'].find('text/json') != -1:
            response_json = self._check_response(response)
            return response_json['result']['status'], None, None
        return 'ready', response.content, response.headers

    def check_file(self,
                   document_id,
                   modules,
                   epub_asset_priority=None,
                   epub_supports=None,
                   epub_exclude_tags=None,
                   epub_include_tags=None,
                   mobi_asset_priority=None,
                   ibooks_asset_priority=None):
        path = '/rpc/asset_converter_control'
        headers = {
            'Authorization': 'Bearer ' + self._ctx.auth_context.auth_token,
            }
        params = {
            'method': 'availability',
            'document_id': document_id,
            'modules' : ','.join(modules)
            }

        if epub_asset_priority is not None:
            params['epub-asset-priority'] = epub_asset_priority
        if epub_supports is not None:
            params['epub-supports'] = ','.join(epub_supports)
        if epub_exclude_tags is not None:
            params['epub-exclude-tags'] = ','.join(epub_exclude_tags)
        if epub_include_tags is not None:
            params['epub-include-tags'] = ','.join(epub_include_tags)
        if mobi_asset_priority is not None:
            params['mobi-asset-priority'] = ','.join(mobi_asset_priority)
        if ibooks_asset_priority is not None:
            params['ibooks-asset-priority'] = ','.join(ibooks_asset_priority)

        response = self._session.get(self._ctx.host + path,
                                     params=params,
                                     headers=headers,
                                     **self._ctx.requests_kwargs)

        return self._check_response(response)['result']['available']

    def current_price(self,
                      document_id,
                      product,
                      country_code,
                      currency_code=None):
        params = {
            'method' : 'current',
            'document_id' : document_id,
            'product' : product,
            'country_code' : country_code,
            }
        headers = {
            'Authorization': 'Bearer ' + self._ctx.auth_context.auth_token,
            }
        if currency_code is not None:
            params['currency_code'] = currency_code

        response = self._session.put(self._ctx.host + '/rpc/price',
                                     params=params,
                                     headers=headers,
                                     **self._ctx.requests_kwargs)
        return self._check_response(response)['OBJECTS'][0]

    def get_record_reference(self, ean, app_name):
        headers = {
            'Authorization': 'Bearer ' + self._ctx.auth_context.auth_token,
            }
        params = {
            'ean' : ean,
            'app_name' : app_name,
            'method' : 'get'
            }
        response = self._session.put(self._ctx.host + '/rpc/record_reference',
                                     params=params,
                                     headers=headers,
                                     **self._ctx.requests_kwargs)
        return self._check_response(response)['result']['record_reference']

    def _raise(self, error):
        def find_parameter(name):
            for param in error['PARAMETERS']:
                if name in param:
                    return param[name]
            return None

        if error['ID'] == 'request_api_file_download::file_creating_error':
            raise AssetCreationError(error['LOCALE_STR'])
        else:
            message = error['LOCALE_STR'] if 'LOCALE_STR' in error else json.dumps(error)
            raise Exception(error['ID'], message)

    def _check_status_code(self, response):
        if response.status_code == 409:
            raise ObjectHasChanged("Object has changed on server, pls reload it first")
        elif response.status_code == 404:
            raise ObjectNotFound()
        elif response.status_code in range(501, 512):
            raise TemporaryNotAvailable('Status code: {0}'.format(response.status_code))
        elif not response.ok:
            response.raise_for_status()

    def _check_response(self,
                        response,
                        schema_validation=False):
        self._check_status_code(response)
        try:
            res_json = response.json()
            self.log.debug("JSON response: {0}".format(res_json))
        except:
            self.log.error("Cannot parse JSON from response, response: '{0}'".format(response.content.decode('utf-8')))
            raise

        if schema_validation:
            schemas_dir = pkg_resources.resource_filename('open_publishing', 'schemas')
            jsonschema.validate(res_json, {'$ref': 'file://' + os.path.join(schemas_dir, 'GjpResponseSchema.json')})

        if 'OK' in res_json:
            if 'FAILURES' in res_json['OK']:
                self._raise(res_json['OK']['FAILURES'][0]['ERROR'])
            return res_json
        self._raise(res_json['ERROR'])
