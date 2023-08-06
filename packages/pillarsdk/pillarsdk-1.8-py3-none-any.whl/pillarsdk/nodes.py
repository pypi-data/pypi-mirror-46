import json
import copy
import os.path

from .resource import List
from .resource import Find
from .resource import Create
from .resource import Post
from .resource import Update
from .resource import Delete
from .resource import Replace
from .resource import Patch
from .exceptions import ResourceNotFound

from . import utils
from .api import Api


class Node(List, Find, Create, Post, Update, Delete, Replace, Patch):
    """Node class wrapping the REST nodes endpoint
    """
    path = "nodes"
    ensure_query_projections = {'project': 1, 'node_type': 1, 'permissions': 1}

    @classmethod
    def find_one(cls, params, api=None):
        """Get one resource starting from parameters different than the resource
        id. TODO if more than one match for the query is found, raise exception.
        """
        api = api or Api.Default()

        # Force delivery of only 1 result
        params['max_results'] = 1
        cls._ensure_projections(params, cls.ensure_query_projections)
        url = utils.join_url_params(cls.path, params)

        response = api.get(url)
        # Keep the response a dictionary, and cast it later into an object.
        if response['_items']:
            item = utils.convert_datetime(response['_items'][0])
            return cls(item)
        else:
            raise ResourceNotFound(response)

    def update(self, attributes=None, api=None):
        api = api or self.api
        attributes = attributes or self.to_dict()
        etag = attributes['_etag']
        attributes = utils.remove_private_keys(attributes)
        attributes = utils.remove_none_attributes(attributes)

        url = utils.join_url(self.path, str(self['_id']))
        headers = utils.merge_dict(
            self.http_headers(),
            {'If-Match': str(etag)})
        new_attributes = api.put(url, attributes, headers)
        self.error = None
        self.merge(new_attributes)
        return self.success()

    def has_method(self, method):
        if not self.allowed_methods:
            return False

        if method in self.allowed_methods:
            return True
        return False

    @classmethod
    def latest(cls, node_type, api=None):
        """Get list of latestnodes."""

        api = api or Api.Default()
        url = 'latest/%s' % node_type

        response = api.get(url)
        for item in response['_items']:
            utils.convert_datetime(item)
        return cls.list_class(response)

    @classmethod
    def create_asset_from_file(cls, project_id, parent_node_id, asset_type, filename,
                               mimetype=None,
                               always_create_new_node=False,
                               extra_where=None,
                               fileobj=None,
                               api=None):
        """Uploads the file to the Cloud and creates an asset node.

        If a node with the project, node_type (always 'asset') and name (always
        basename of the given filename) exists, it will be updated (unless
        always_create_new_node is True).

        :param project_id: the project ID
        :param parent_node_id: node ID to attach this asset node to. Can be None.
        :param asset_type: 'image', 'file', 'video', etc.
        :param filename: path of the file to upload. Must be readable.
        :param mimetype: MIME type of the file, such as "image/jpeg". If
            None, it will be guessed from the filename.
        :param always_create_new_node: when True, a new node is always created,
            possibly with the same name & parent as an existing one.
        :param extra_where: dict of properties to use, in addition to project, node_type
            and name, to find any existing node. Use this to restrict the
            nodes that may be re-used to attach this file to.
        :param fileobj: file object to read the file from. If None, it is read
            by opening 'filename'. The file object will not be closed after uploading.
        :returns: the updated/created node
        :rtype: Node
        """

        api = api or Api.Default()

        # Guess mime type from filename.
        if not mimetype:
            mimetype = cls._guess_mimetype(filename)

        from .files import File

        # Upload the file to project storage.
        file_upload_resp = File.upload_to_project(project_id, mimetype, filename, fileobj, api=api)
        file_upload_status = file_upload_resp.get('_status') or file_upload_resp.get('status')
        if file_upload_status != 'ok':
            raise ValueError('Received bad status %s from Pillar: %s' %
                             (file_upload_status, json.dumps(file_upload_resp)))
        file_id = file_upload_resp['file_id']

        # Create or update the node.
        basic_properties = {
            'project': project_id,
            'node_type': 'asset',
            'name': os.path.basename(filename)
        }
        if parent_node_id:
            basic_properties['parent'] = parent_node_id

        if not always_create_new_node:
            # Try to find an existing one to see if there is anything to update.
            where = copy.deepcopy(basic_properties)
            if extra_where:
                where.update(extra_where)
            existing_node = cls.find_first({'where': where}, api=api)
            if existing_node:
                # Just update the file ID and we're done.
                existing_node.properties.content_type = asset_type
                existing_node.properties.file = file_id
                existing_node.update(api=api)
                return existing_node

        basic_properties.update({
            'properties': {'content_type': asset_type,
                           'file': file_id},
        })
        node = cls(basic_properties)
        node.create(api=api)

        return node

    @classmethod
    def _guess_mimetype(cls, filename):
        """Guesses the MIME type from the filename.

        :return: the MIME type
        :rtype: str
        """

        import mimetypes
        mimetype, _ = mimetypes.guess_type(filename, strict=False)
        return mimetype

    def share(self, api=None):
        """Creates a short-link.

        :returns: a dict like {
                'short_code': 'XXXXXX',
                'short_link': 'https://blender.cloud/r/XXXXX',
            }
        :rtype: dict
        """

        api = api or Api.Default()

        return api.post('nodes/%s/share' % self['_id'])

    def get_share_links(self, api=None):
        """Returns short-link info for this node.

        :returns: a dict like {
                'short_code': 'XXXXXX',
                'short_link': 'https://blender.cloud/r/XXXXX',
            }, or an empty dict if the node wasn't shared.
        :rtype: dict
        """

        api = api or Api.Default()

        return api.get('nodes/%s/share' % self['_id'])
