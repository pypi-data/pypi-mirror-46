# Copyright 2014 - Mirantis, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import functools

from oslo_config import cfg
from oslo_log import log
from oslo_utils import importutils

from keystoneclient.auth import identity
from keystoneclient import httpclient

from mistral.actions.openstack import base
from mistral.utils import inspect_utils
from mistral.utils.openstack import keystone as keystone_utils


LOG = log.getLogger(__name__)

CONF = cfg.CONF


IRONIC_API_VERSION = '1.22'
"""The default microversion to pass to Ironic API.

1.22 corresponds to Newton final.
"""


def _try_import(module_name):
    try:
        return importutils.try_import(module_name)
    except Exception as e:
        msg = 'Unable to load module "%s". %s' % (module_name, str(e))
        LOG.error(msg)
        return None


aodhclient = _try_import('aodhclient.v2.client')
barbicanclient = _try_import('barbicanclient.client')
ceilometerclient = _try_import('ceilometerclient.v2.client')
cinderclient = _try_import('cinderclient.v2.client')
designateclient = _try_import('designateclient.v1')
glanceclient = _try_import('glanceclient.v2.client')
glareclient = _try_import('glareclient.v1.client')
gnocchiclient = _try_import('gnocchiclient.v1.client')
heatclient = _try_import('heatclient.v1.client')
ironic_inspector_client = _try_import('ironic_inspector_client.v1')
ironicclient = _try_import('ironicclient.v1.client')
keystoneclient = _try_import('keystoneclient.v3.client')
magnumclient = _try_import('magnumclient.v1.client')
mistralclient = _try_import('mistralclient.api.v2.client')
muranoclient = _try_import('muranoclient.v1.client')
neutronclient = _try_import('neutronclient.v2_0.client')
novaclient = _try_import('novaclient.client')
senlinclient = _try_import('senlinclient.v1.client')
swift_client = _try_import('swiftclient.client')
tackerclient = _try_import('tackerclient.v1_0.client')
troveclient = _try_import('troveclient.v1.client')
zaqarclient = _try_import('zaqarclient.queues.v2.client')


class NovaAction(base.OpenStackAction):
    _service_type = 'compute'

    @classmethod
    def _get_client_class(cls):
        return novaclient.Client

    def _create_client(self, context):
        LOG.debug("Nova action security context: %s", context)

        return novaclient.Client(2, **self.get_session_and_auth(context))

    @classmethod
    def _get_fake_client(cls):
        return cls._get_client_class()(2)


class GlanceAction(base.OpenStackAction):
    _service_type = 'image'

    @classmethod
    def _get_client_class(cls):
        return glanceclient.Client

    def _create_client(self, context):

        LOG.debug("Glance action security context: %s", context)

        glance_endpoint = self.get_service_endpoint()

        return self._get_client_class()(
            glance_endpoint.url,
            region_name=glance_endpoint.region,
            **self.get_session_and_auth(context)
        )

    @classmethod
    def _get_fake_client(cls):
        return cls._get_client_class()("fake_endpoint")


class KeystoneAction(base.OpenStackAction):

    _service_type = 'identity'

    @classmethod
    def _get_client_class(cls):
        return keystoneclient.Client

    def _create_client(self, context):

        LOG.debug("Keystone action security context: %s", context)

        kwargs = self.get_session_and_auth(context)

        # NOTE(akovi): the endpoint in the token messes up
        # keystone. The auth parameter should not be provided for
        # these operations.
        kwargs.pop('auth')

        client = self._get_client_class()(**kwargs)

        return client

    @classmethod
    def _get_fake_client(cls):
        # Here we need to replace httpclient authenticate method temporarily
        authenticate = httpclient.HTTPClient.authenticate

        httpclient.HTTPClient.authenticate = lambda x: True
        fake_client = cls._get_client_class()()

        # Once we get fake client, return back authenticate method
        httpclient.HTTPClient.authenticate = authenticate

        return fake_client


class CeilometerAction(base.OpenStackAction):
    _service_type = 'metering'

    @classmethod
    def _get_client_class(cls):
        return ceilometerclient.Client

    def _create_client(self, context):

        LOG.debug("Ceilometer action security context: %s", context)

        ceilometer_endpoint = self.get_service_endpoint()

        endpoint_url = keystone_utils.format_url(
            ceilometer_endpoint.url,
            {'tenant_id': context.project_id}
        )

        return self._get_client_class()(
            endpoint_url,
            region_name=ceilometer_endpoint.region,
            token=context.auth_token,
            username=context.user_name,
            insecure=context.insecure
        )

    @classmethod
    def _get_fake_client(cls):
        return cls._get_client_class()("")


class HeatAction(base.OpenStackAction):
    _service_type = 'orchestration'

    @classmethod
    def _get_client_class(cls):
        return heatclient.Client

    def _create_client(self, context):

        LOG.debug("Heat action security context: %s", context)

        heat_endpoint = self.get_service_endpoint()

        endpoint_url = keystone_utils.format_url(
            heat_endpoint.url,
            {
                'tenant_id': context.project_id,
                'project_id': context.project_id
            }
        )

        return self._get_client_class()(
            endpoint_url,
            region_name=heat_endpoint.region,
            **self.get_session_and_auth(context)
        )

    @classmethod
    def _get_fake_client(cls):
        return cls._get_client_class()("")


class NeutronAction(base.OpenStackAction):
    _service_type = 'network'

    @classmethod
    def _get_client_class(cls):
        return neutronclient.Client

    def _create_client(self, context):

        LOG.debug("Neutron action security context: %s", context)

        neutron_endpoint = self.get_service_endpoint()

        return self._get_client_class()(
            endpoint_url=neutron_endpoint.url,
            region_name=neutron_endpoint.region,
            token=context.auth_token,
            auth_url=context.auth_uri,
            insecure=context.insecure
        )


class CinderAction(base.OpenStackAction):
    _service_type = 'volumev2'

    @classmethod
    def _get_client_class(cls):
        return cinderclient.Client

    def _create_client(self, context):

        LOG.debug("Cinder action security context: %s", context)

        cinder_endpoint = self.get_service_endpoint()

        cinder_url = keystone_utils.format_url(
            cinder_endpoint.url,
            {
                'tenant_id': context.project_id,
                'project_id': context.project_id
            }
        )

        client = self._get_client_class()(
            context.user_name,
            context.auth_token,
            project_id=context.project_id,
            auth_url=cinder_url,
            region_name=cinder_endpoint.region,
            insecure=context.insecure
        )

        client.client.auth_token = context.auth_token
        client.client.management_url = cinder_url

        return client

    @classmethod
    def _get_fake_client(cls):
        return cls._get_client_class()()


class MistralAction(base.OpenStackAction):
    _service_type = 'workflowv2'

    @classmethod
    def _get_client_class(cls):
        return mistralclient.Client

    def _create_client(self, context):

        LOG.debug("Mistral action security context: %s", context)

        if CONF.pecan.auth_enable:
            session_and_auth = self.get_session_and_auth(context)

            return self._get_client_class()(
                mistral_url=session_and_auth['auth'].endpoint,
                **session_and_auth)
        else:
            mistral_url = 'http://{}:{}/v2'.format(CONF.api.host,
                                                   CONF.api.port)
            return self._get_client_class()(mistral_url=mistral_url)

    @classmethod
    def _get_fake_client(cls):
        return cls._get_client_class()()


class TroveAction(base.OpenStackAction):
    _service_type = 'database'

    @classmethod
    def _get_client_class(cls):
        return troveclient.Client

    def _create_client(self, context):

        LOG.debug("Trove action security context: %s", context)

        trove_endpoint = self.get_service_endpoint()

        trove_url = keystone_utils.format_url(
            trove_endpoint.url,
            {'tenant_id': context.project_id}
        )

        client = self._get_client_class()(
            context.user_name,
            context.auth_token,
            project_id=context.project_id,
            auth_url=trove_url,
            region_name=trove_endpoint.region,
            insecure=context.insecure
        )

        client.client.auth_token = context.auth_token
        client.client.management_url = trove_url

        return client

    @classmethod
    def _get_fake_client(cls):
        return cls._get_client_class()("fake_user", "fake_passwd")


class IronicAction(base.OpenStackAction):
    _service_name = 'ironic'

    @classmethod
    def _get_client_class(cls):
        return ironicclient.Client

    def _create_client(self, context):

        LOG.debug("Ironic action security context: %s", context)

        ironic_endpoint = self.get_service_endpoint()

        return self._get_client_class()(
            ironic_endpoint.url,
            token=context.auth_token,
            region_name=ironic_endpoint.region,
            os_ironic_api_version=IRONIC_API_VERSION,
            insecure=context.insecure
        )

    @classmethod
    def _get_fake_client(cls):
        return cls._get_client_class()("http://127.0.0.1:6385/")


class BaremetalIntrospectionAction(base.OpenStackAction):

    @classmethod
    def _get_client_class(cls):
        return ironic_inspector_client.ClientV1

    @classmethod
    def _get_fake_client(cls):
        try:
            # ironic-inspector client tries to get and validate it's own
            # version when created. This might require checking the keystone
            # catalog if the ironic-inspector server is not listening on the
            # localhost IP address. Thus, we get a session for this case.
            sess = keystone_utils.get_admin_session()

            return cls._get_client_class()(session=sess)
        except Exception as e:
            LOG.warning("There was an error trying to create the "
                        "ironic-inspector client using a session: %s", str(e))
            # If it's not possible to establish a keystone session, attempt to
            # create a client without it. This should fall back to where the
            # ironic-inspector client tries to get it's own version on the
            # default IP address.
            LOG.debug("Attempting to create the ironic-inspector client "
                      "without a session.")

            return cls._get_client_class()()

    def _create_client(self, context):

        LOG.debug(
            "Baremetal introspection action security context: %s", context)

        inspector_endpoint = keystone_utils.get_endpoint_for_project(
            service_type='baremetal-introspection'
        )

        return self._get_client_class()(
            api_version=1,
            inspector_url=inspector_endpoint.url,
            auth_token=context.auth_token,
        )


class SwiftAction(base.OpenStackAction):

    @classmethod
    def _get_client_class(cls):
        return swift_client.Connection

    def _create_client(self, context):

        LOG.debug("Swift action security context: %s", context)

        swift_endpoint = keystone_utils.get_endpoint_for_project('swift')

        kwargs = {
            'preauthurl': swift_endpoint.url % {
                'tenant_id': context.project_id
            },
            'preauthtoken': context.auth_token,
            'insecure': context.insecure
        }

        return self._get_client_class()(**kwargs)


class ZaqarAction(base.OpenStackAction):

    @classmethod
    def _get_client_class(cls):
        return zaqarclient.Client

    def _create_client(self, context):

        LOG.debug("Zaqar action security context: %s", context)

        zaqar_endpoint = keystone_utils.get_endpoint_for_project(
            service_type='messaging')
        keystone_endpoint = keystone_utils.get_keystone_endpoint_v2()

        opts = {
            'os_auth_token': context.auth_token,
            'os_auth_url': keystone_endpoint.url,
            'os_project_id': context.project_id,
            'insecure': context.insecure,
        }
        auth_opts = {'backend': 'keystone', 'options': opts}
        conf = {'auth_opts': auth_opts}

        return self._get_client_class()(zaqar_endpoint.url, conf=conf)

    @classmethod
    def _get_fake_client(cls):
        return cls._get_client_class()("")

    @classmethod
    def _get_client_method(cls, client):
        method = getattr(cls, cls.client_method_name)

        # We can't use partial as it's not supported by getargspec
        @functools.wraps(method)
        def wrap(*args, **kwargs):
            return method(client, *args, **kwargs)

        arguments = inspect_utils.get_arg_list_as_str(method)
        # Remove client
        wrap.__arguments__ = arguments.split(', ', 1)[1]

        return wrap

    @staticmethod
    def queue_messages(client, queue_name, **params):
        """Gets a list of messages from the queue.

        :param client: the Zaqar client
        :type client: zaqarclient.queues.client

        :param queue_name: Name of the target queue.
        :type queue_name: `six.string_type`

        :param params: Filters to use for getting messages.
        :type params: **kwargs dict

        :returns: List of messages.
        :rtype: `list`
        """
        queue = client.queue(queue_name)

        return queue.messages(**params)

    @staticmethod
    def queue_post(client, queue_name, messages):
        """Posts one or more messages to a queue.

        :param client: the Zaqar client
        :type client: zaqarclient.queues.client

        :param queue_name: Name of the target queue.
        :type queue_name: `six.string_type`

        :param messages: One or more messages to post.
        :type messages: `list` or `dict`

        :returns: A dict with the result of this operation.
        :rtype: `dict`
        """
        queue = client.queue(queue_name)

        return queue.post(messages)

    @staticmethod
    def queue_pop(client, queue_name, count=1):
        """Pop `count` messages from the queue.

        :param client: the Zaqar client
        :type client: zaqarclient.queues.client

        :param queue_name: Name of the target queue.
        :type queue_name: `six.string_type`

        :param count: Number of messages to pop.
        :type count: int

        :returns: List of messages.
        :rtype: `list`
        """
        queue = client.queue(queue_name)

        return queue.pop(count)


class BarbicanAction(base.OpenStackAction):

    @classmethod
    def _get_client_class(cls):
        return barbicanclient.Client

    def _create_client(self, context):

        LOG.debug("Barbican action security context: %s", context)

        barbican_endpoint = keystone_utils.get_endpoint_for_project('barbican')
        keystone_endpoint = keystone_utils.get_keystone_endpoint_v2()

        auth = identity.v2.Token(
            auth_url=keystone_endpoint.url,
            tenant_name=context.user_name,
            token=context.auth_token,
            tenant_id=context.project_id
        )

        return self._get_client_class()(
            project_id=context.project_id,
            endpoint=barbican_endpoint.url,
            auth=auth,
            insecure=context.insecure
        )

    @classmethod
    def _get_fake_client(cls):
        return cls._get_client_class()(
            project_id="1",
            endpoint="http://127.0.0.1:9311"
        )

    @classmethod
    def _get_client_method(cls, client):
        if cls.client_method_name != "secrets_store":
            return super(BarbicanAction, cls)._get_client_method(client)

        method = getattr(cls, cls.client_method_name)

        @functools.wraps(method)
        def wrap(*args, **kwargs):
            return method(client, *args, **kwargs)

        arguments = inspect_utils.get_arg_list_as_str(method)

        # Remove client.
        wrap.__arguments__ = arguments.split(', ', 1)[1]

        return wrap

    @staticmethod
    def secrets_store(client,
                      name=None,
                      payload=None,
                      algorithm=None,
                      bit_length=None,
                      secret_type=None,
                      mode=None, expiration=None):
        """Create and Store a secret in Barbican.

        :param client: the Zaqar client
        :type client: zaqarclient.queues.client

        :param name: A friendly name for the Secret
        :type name: string

        :param payload: The unencrypted secret data
        :type payload: string

        :param algorithm: The algorithm associated with this secret key
        :type algorithm: string

        :param bit_length: The bit length of this secret key
        :type bit_length: int

        :param secret_type: The secret type for this secret key
        :type secret_type: string

         :param mode: The algorithm mode used with this secret keybit_length:
        :type mode: string

        :param expiration: The expiration time of the secret in ISO 8601 format
        :type expiration: string

        :returns: A new Secret object
        :rtype: class:`barbicanclient.secrets.Secret'
        """

        entity = client.secrets.create(
            name,
            payload,
            algorithm,
            bit_length,
            secret_type,
            mode,
            expiration
        )

        entity.store()

        return entity._get_formatted_entity()


class DesignateAction(base.OpenStackAction):
    _service_type = 'dns'

    @classmethod
    def _get_client_class(cls):
        return designateclient.Client

    def _create_client(self, context):

        LOG.debug("Designate action security context: %s", context)

        designate_endpoint = self.get_service_endpoint()

        designate_url = keystone_utils.format_url(
            designate_endpoint.url,
            {'tenant_id': context.project_id}
        )

        client = self._get_client_class()(
            endpoint=designate_url,
            tenant_id=context.project_id,
            auth_url=context.auth_uri,
            region_name=designate_endpoint.region,
            service_type='dns',
            insecure=context.insecure
        )

        client.client.auth_token = context.auth_token
        client.client.management_url = designate_url

        return client

    @classmethod
    def _get_fake_client(cls):
        return cls._get_client_class()()


class MagnumAction(base.OpenStackAction):

    @classmethod
    def _get_client_class(cls):
        return magnumclient.Client

    def _create_client(self, context):

        LOG.debug("Magnum action security context: %s", context)

        keystone_endpoint = keystone_utils.get_keystone_endpoint_v2()
        auth_url = keystone_endpoint.url
        magnum_url = keystone_utils.get_endpoint_for_project('magnum').url

        return self._get_client_class()(
            magnum_url=magnum_url,
            auth_token=context.auth_token,
            project_id=context.project_id,
            user_id=context.user_id,
            auth_url=auth_url,
            insecure=context.insecure
        )

    @classmethod
    def _get_fake_client(cls):
        return cls._get_client_class()(auth_url='X', magnum_url='X')


class MuranoAction(base.OpenStackAction):
    _service_name = 'murano'

    @classmethod
    def _get_client_class(cls):
        return muranoclient.Client

    def _create_client(self, context):

        LOG.debug("Murano action security context: %s", context)

        keystone_endpoint = keystone_utils.get_keystone_endpoint_v2()
        murano_endpoint = self.get_service_endpoint()

        return self._get_client_class()(
            endpoint=murano_endpoint.url,
            token=context.auth_token,
            tenant=context.project_id,
            region_name=murano_endpoint.region,
            auth_url=keystone_endpoint.url,
            insecure=context.insecure
        )

    @classmethod
    def _get_fake_client(cls):
        return cls._get_client_class()("http://127.0.0.1:8082/")


class TackerAction(base.OpenStackAction):
    _service_name = 'tacker'

    @classmethod
    def _get_client_class(cls):
        return tackerclient.Client

    def _create_client(self, context):

        LOG.debug("Tacker action security context: %s", context)

        keystone_endpoint = keystone_utils.get_keystone_endpoint_v2()
        tacker_endpoint = self.get_service_endpoint()

        return self._get_client_class()(
            endpoint_url=tacker_endpoint.url,
            token=context.auth_token,
            tenant_id=context.project_id,
            region_name=tacker_endpoint.region,
            auth_url=keystone_endpoint.url,
            insecure=context.insecure
        )

    @classmethod
    def _get_fake_client(cls):
        return cls._get_client_class()()


class SenlinAction(base.OpenStackAction):
    _service_name = 'senlin'

    @classmethod
    def _get_client_class(cls):
        return senlinclient.Client

    def _create_client(self, context):

        LOG.debug("Senlin action security context: %s", context)

        keystone_endpoint = keystone_utils.get_keystone_endpoint_v2()
        senlin_endpoint = self.get_service_endpoint()

        return self._get_client_class()(
            endpoint_url=senlin_endpoint.url,
            token=context.auth_token,
            tenant_id=context.project_id,
            region_name=senlin_endpoint.region,
            auth_url=keystone_endpoint.url,
            insecure=context.insecure
        )

    @classmethod
    def _get_fake_client(cls):
        return cls._get_client_class()("http://127.0.0.1:8778")


class AodhAction(base.OpenStackAction):
    _service_type = 'alarming'

    @classmethod
    def _get_client_class(cls):
        return aodhclient.Client

    def _create_client(self, context):

        LOG.debug("Aodh action security context: %s", context)

        aodh_endpoint = self.get_service_endpoint()

        endpoint_url = keystone_utils.format_url(
            aodh_endpoint.url,
            {'tenant_id': context.project_id}
        )

        return self._get_client_class()(
            endpoint_url,
            region_name=aodh_endpoint.region,
            token=context.auth_token,
            username=context.user_name,
            insecure=context.insecure
        )

    @classmethod
    def _get_fake_client(cls):
        return cls._get_client_class()()


class GnocchiAction(base.OpenStackAction):
    _service_type = 'metric'

    @classmethod
    def _get_client_class(cls):
        return gnocchiclient.Client

    def _create_client(self, context):

        LOG.debug("Gnocchi action security context: %s", context)

        gnocchi_endpoint = self.get_service_endpoint()

        endpoint_url = keystone_utils.format_url(
            gnocchi_endpoint.url,
            {'tenant_id': context.project_id}
        )

        return self._get_client_class()(
            endpoint_url,
            region_name=gnocchi_endpoint.region,
            token=context.auth_token,
            username=context.user_name
        )

    @classmethod
    def _get_fake_client(cls):
        return cls._get_client_class()()


class GlareAction(base.OpenStackAction):
    _service_name = 'glare'

    @classmethod
    def _get_client_class(cls):
        return glareclient.Client

    def _create_client(self, context):

        LOG.debug("Glare action security context: %s", context)

        glare_endpoint = self.get_service_endpoint()

        endpoint_url = keystone_utils.format_url(
            glare_endpoint.url,
            {'tenant_id': context.project_id}
        )

        return self._get_client_class()(
            endpoint_url,
            **self.get_session_and_auth(context)
        )

    @classmethod
    def _get_fake_client(cls):
        return cls._get_client_class()("http://127.0.0.1:9494/")
