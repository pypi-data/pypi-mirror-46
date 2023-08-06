"""Client classes for POST/inserting data into a perfsonar MA."""

import json

import requests
from requests.exceptions import ConnectionError

from ..util import add_apikey_header, AlertMixin
from .query import Metadata, ApiFilters, PS_ROOT

# Custom exceptions and warnings


class PostException(Exception):
    """Custom Post exception"""
    def __init__(self, value):
        # pylint: disable=super-init-not-called
        self.value = value

    def __str__(self):
        return repr(self.value)


class MetadataPostException(PostException):
    """Metadata exception"""
    pass


class EventTypePostException(PostException):
    """EventType exception."""
    pass


class EventTypeBulkPostException(PostException):
    """EventType bulk exception."""
    pass


class MetadataPostWarning(Warning):
    """Metadata warning."""
    pass


class EventTypePostWarning(Warning):
    """EventType warning."""
    pass


class EventTypeBulkPostWarning(Warning):
    """EventType bulk warning."""
    pass

# Base class for the post clients and message specific subclasses.


class PostBase(AlertMixin, object):
    """
    Base class for perfsonar API post functionality.  Should not
    be directly instantiated.
    """
    _schema_root = '{0}/archive'.format(PS_ROOT)

    def __init__(self, api_url, username, api_key, script_alias, ssl_verify=True, timeout=20):
        """
        The api_url, username and api_key args all have their usual usages.

        The script_alias arg (which defaults to 'esmond') is in place
        for the perfsonar CentOS distributions.  The 'root' of the
        perfsonar api as defined in esmond.api.perfsonar.api is
        is http://host:port/perfsonar/archive/... When deployed under
        Apache on the canned perfsonar installations, a ScriptAlias
        of /esmond is employed so the rest api won't 'take over' the
        default webserver.  When running this way it yields a base
        of http://host:port/esmond/perfsonar/archive/... - this is
        the default of the canned system install.

        The script_alias arg can be set to None when doing development
        against the django dev runserver, or set to something else if
        running under a similar but different deployment.

        Setting the arg to '/' will yield the same result as setting it
        to None - this makes it easier for calling programs that are
        setting that value via a command line arg/config file/etc.
        """
        super(PostBase, self).__init__()
        self.api_url = api_url
        if self.api_url:
            self.api_url = api_url.rstrip('/')

        self.username = username
        self.api_key = api_key
        self.script_alias = script_alias
        self.headers = {'content-type': 'application/json'}
        self.ssl_verify=ssl_verify
        self.timeout=timeout
        if self.username and self.api_key:
            add_apikey_header(self.username, self.api_key, self.headers)
        else:
            self.warn('username and api_key not set')
        # sublass override
        self._payload = {}

        try:
            getattr(self, 'wrn')
        except AttributeError:
            raise PostException('Do not instantiate base class, use appropriate subclass')

        if self.script_alias:
            self.script_alias = script_alias.rstrip('/')
            self.script_alias = script_alias.lstrip('/')
            if self.script_alias:
                self._schema_root = '{0}/{1}'.format(self.script_alias, self._schema_root)

    def ex(self, msg):
        """Abstract method, raise exceptions, implement in subclasses."""
        raise NotImplementedError('Must be implemented in subclass')

    def _validate(self):
        """Will be overridden in subclass.  Needs to run whatever validation
        checks on the internal payload data before sending it to the API."""
        raise NotImplementedError('Must be implemented in subclass')

    def json_payload(self, pp=False):
        """Dump internal payload to json."""
        self._validate()
        if pp:
            return json.dumps(self._payload, indent=4)
        else:
            return json.dumps(self._payload)


class MetadataPost(PostBase):  # pylint: disable=too-many-instance-attributes
    """
    Client class to POST metadata data/objects to the perfsonar
    relational database.
    """
    wrn = MetadataPostWarning

    def __init__(self, api_url, username='', api_key='',  # pylint: disable=too-many-arguments
                 subject_type=None, source=None, destination=None,
                 tool_name=None, measurement_agent=None, input_source=None,
                 input_destination=None, time_duration=None,
                 ip_transport_protocol=None, script_alias='esmond', ssl_verify=True, timeout=20):
        super(MetadataPost, self).__init__(api_url, username, api_key, script_alias, ssl_verify=ssl_verify, timeout=timeout)
        # required
        self.subject_type = subject_type
        self.source = source
        self.destination = destination
        self.tool_name = tool_name
        self.measurement_agent = measurement_agent
        self.input_source = input_source
        self.input_destination = input_destination
        # optional - if not defined, don't send at all
        self.time_duration = time_duration
        self.ip_transport_protocol = ip_transport_protocol

        self._required_args = (
            'subject_type',
            'source',
            'destination',
            'tool_name',
            'measurement_agent',
            'input_source',
            'input_destination'
        )

        self._optional_args = (
            'time_duration',
            'ip_transport_protocol'
        )

        self._payload = {
            'subject-type': self.subject_type,
            'source': self.source,
            'destination': self.destination,
            'tool-name': self.tool_name,
            'measurement-agent': self.measurement_agent,
            'input-source': self.input_source,
            'input-destination': self.input_destination,
            'time-duration': self.time_duration,
            'ip-transport-protocol': self.ip_transport_protocol,
            'event-types': []
        }

    def add_event_type(self, etype):
        """Add event-type data to the metadata before POSTing to
        the backend.  Will normally be called more than once."""

        for i in self._payload['event-types']:
            if i.get('event-type', None) == etype:
                self.warn('Event type {0} already exists - skipping'.format(etype))

        self._payload['event-types'].append({'event-type': etype, 'summaries': []})

    def add_summary_type(self, etype, stype, windows=[]):  # pylint: disable=dangerous-default-value
        """Add associated summary-type data to metadata before POSTing."""

        if not windows:
            self.warn('No summary windows were defined - skipping')
            return

        for i in windows:
            try:
                int(i)
            except ValueError:
                raise MetadataPostException('Invalid summary window int: {0}'.format(i))

        for existing_et_def in self._payload['event-types']:
            if existing_et_def.get('event-type', None) == etype:
                # add new summaries
                new_summaries = [{'summary-type': stype, 'summary-window': x} for x in windows]
                # clear out old summaries
                for summ in existing_et_def['summaries']:
                    if summ['summary-type'] == stype:
                        # remove any existing summaries of same type
                        pass
                    else:
                        new_summaries.append(summ)
                existing_et_def['summaries'] = new_summaries
                return

        # if event type does not exist then create and add summaries
        suminfo = {
            'event-type': etype,
            'summaries': [
                {'summary-type': stype, 'summary-window': x} for x in windows
            ]
        }

        self._payload['event-types'].append(suminfo)

    def add_freeform_key_value(self, k, v):
        """Add key/values pairs to metadata payload to be stored in the
        ps_metadata_parameters table."""
        if not self._payload.get(k, None):
            self._payload[k] = v
        else:
            self.warn('Payload key {0} exists - skipping'.format(k))

    def post_metadata(self):
        """Void method that will post the new metadata to the API and
        return the newly created metadata information wrapped in an
        esmond.api.perfsonar.query.Metadata object."""
        url = '{0}/{1}/'.format(self.api_url, self._schema_root)

        try:
            r = requests.post(url, data=self.json_payload(), 
                                headers=self.headers, 
                                verify=self.ssl_verify, 
                                timeout=self.timeout
                             )
        except ConnectionError, ex:
            self.ex('POST connection error: {0}'.format(str(ex)))
            return None

        if r.status_code != 201:
            # Change this to an exception?
            self.ex('POST error: status_code: {0}, message: {1}'.format(r.status_code, r.content))
            return None

        filters = ApiFilters()

        if self.username and self.api_key:
            filters.auth_username = self.username
            filters.auth_apikey = self.api_key

        return Metadata(json.loads(r.content), self.api_url, filters)

    def ex(self, msg):
        raise MetadataPostException(msg)

    def _validate(self):

        def redash(val):
            """Change values from_this_style back-to-this-style."""
            return val.replace('_', '-')

        # make sure required args are present
        for arg in self._required_args:
            if not getattr(self, arg):
                raise MetadataPostException('Reqired arg {0} not set'.format(arg))

        # remove any optional args from payload
        for arg in self._optional_args:
            if not getattr(self, arg) and redash(arg) in self._payload:
                del self._payload[redash(arg)]


class EventTypePost(PostBase):
    """Client code to POST data to a single event type to the perfsonar API."""
    wrn = EventTypePostWarning

    def __init__(self, api_url, username='', api_key='', metadata_key=None,  # pylint: disable=too-many-arguments
                 event_type=None, script_alias='esmond', ssl_verify=True, timeout=20):
        """
        The api_url, username and api_key args have their usual uses.  The
        event_type arg is outlined in the base class.

        The metadata_key and event_type args are the associated metadata
        / event-type new data is being added to.
        """
        super(EventTypePost, self).__init__(api_url, username, api_key, script_alias, ssl_verify=ssl_verify, timeout=timeout)

        self.metadata_key = metadata_key
        self.event_type = event_type

        if not self.metadata_key or not self.event_type:
            raise EventTypePostException('Must set metadata_key and event_type args')

        # Slightly different than payload in meta data class.
        # List will hold data points, but whole thing will not
        # be sent to server.
        self._payload = []

    def add_data_point(self, ts, val):
        """Add a new ts/datapoint to the payload for the meta/event type
        before sending to api.  Will be called more than once."""
        if not isinstance(ts, int):
            raise EventTypePostException('ts arg must be an integer')
        self._payload.append({'ts': ts, 'val': val})

    def post_data(self):
        """Void method to send the payload to the API.  Does not return
        anything."""
        self._validate()

        url = '{0}/{1}/{2}/{3}/base'.format(self.api_url, self._schema_root,
                                            self.metadata_key, self.event_type)

        for dpay in self._payload:
            try:
                r = requests.post(url, data=json.dumps(dpay), headers=self.headers, verify=self.ssl_verify, timeout=self.timeout)
            except ConnectionError, ex:
                self.ex('POST connection error: {0}'.format(str(ex)))

            if r.status_code != 201:
                self.ex('POST error: status_code: {0}, message: {1}'.format(
                    r.status_code, r.content))

    def ex(self, msg):
        raise EventTypePostException(msg)

    def _validate(self):
        """Method is called before a POST to do any sanity checks on the
        payload being sent."""
        # Currently unused - leaving here for future
        # for i in self._payload:
        #     pass
        pass


class EventTypeBulkPost(PostBase):
    """Client class to bulk post data.  This is used to write multiple
    event types to a single metadata."""
    wrn = EventTypePostWarning

    def __init__(self, api_url, username='', api_key='', metadata_key=None,  # pylint: disable=too-many-arguments
                 script_alias='esmond', ssl_verify=True, timeout=20):
        """
        The api_url, username and api_key args have their usual uses.  The
        event_type arg is outlined in the base class.  The metadata_key arg
        is the string for the metadata being written to.
        """
        super(EventTypeBulkPost, self).__init__(api_url, username, api_key, script_alias, ssl_verify=ssl_verify, timeout=timeout)

        self.metadata_key = metadata_key

        if not self.metadata_key:
            raise EventTypeBulkPostException('Must set metadata_key')

        self._payload = {'data': []}

    def _get_ts_payload_entry(self, ts):
        entry = False

        for i in self._payload['data']:
            if i['ts'] == ts:
                entry = i

        if not entry:
            self._payload['data'].append({'ts': ts, 'val': []})
            return self._get_ts_payload_entry(ts)

        return entry

    def add_data_point(self, event_type, ts, val):
        """Adds data points to the payload.  Adds new ts/datapoint to
        a specific event-type in the internal payload.  Will be called
        multiple times."""

        if not isinstance(ts, int):
            raise EventTypeBulkPostException('ts arg must be an integer')

        data_entry = self._get_ts_payload_entry(ts)
        data_entry['val'].append({'event-type': event_type, 'val': val})

    def post_data(self):
        """Void method to send the payload to the API.  Does not return
        anything."""
        self._validate()

        url = '{0}/{1}/{2}/'.format(self.api_url, self._schema_root,
                                    self.metadata_key)

        try:
            r = requests.put(url, data=self.json_payload(), headers=self.headers, verify=self.ssl_verify, timeout=self.timeout)
        except ConnectionError, ex:
            self.ex('POST connection error: {0}'.format(str(ex)))

        if r.status_code != 201:
            self.ex('POST error: status_code: {0}, message: {1}'.format(r.status_code, r.content))

    def ex(self, msg):
        raise EventTypeBulkPostException(msg)

    def _validate(self):
        # Currently unused - leaving here for future
        # Checking in add_data_point
        # for i in self._payload['data']:
        #     pass
        pass
