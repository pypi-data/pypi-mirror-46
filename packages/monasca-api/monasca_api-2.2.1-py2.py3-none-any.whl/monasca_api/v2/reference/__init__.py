# Copyright 2014 IBM Corp.
# Copyright 2016 FUJITSU LIMITED
# (C) Copyright 2016-2017 Hewlett Packard Enterprise Development LP
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from oslo_config import cfg
from oslo_config import types
from oslo_db import options


"""Configurations for reference implementation

I think that these configuration parameters should have been split into
small groups and be set into each implementation where they get used.

For example: kafka configuration should have been in the implementation
where kafka get used. It seems to me that the configuration for kafka gets
used in kafka_publisher, but the original settings were at the api/server.py
which I think is at the wrong place. I move these settings here for now, we
need to have a bit more re-engineering to get it right.
"""
global_opts = [cfg.StrOpt('region', help='Region that API is running in'),
               cfg.ListOpt('valid_notification_periods', default=[0, 60],
                           item_type=int,
                           help='Valid periods for notification methods')
               ]

cfg.CONF.register_opts(global_opts)

security_opts = [cfg.ListOpt('default_authorized_roles', default=['admin'],
                             help='Roles that are allowed full access to the '
                                  'API'),
                 cfg.ListOpt('agent_authorized_roles', default=['agent'],
                             help='Roles that are only allowed to POST to '
                                  'the API'),
                 cfg.ListOpt('read_only_authorized_roles', default=['monasca-read-only-user'],
                             help='Roles that are only allowed to GET from '
                                  'the API'),
                 cfg.ListOpt('delegate_authorized_roles', default=['admin'],
                             help='Roles that are allowed to POST metrics on '
                                  'behalf of another tenant')]

security_group = cfg.OptGroup(name='security', title='security')
cfg.CONF.register_group(security_group)
cfg.CONF.register_opts(security_opts, security_group)

messaging_opts = [cfg.StrOpt('driver', default='kafka',
                             help='The message queue driver to use'),
                  cfg.StrOpt('metrics_message_format', default='reference',
                             help='The type of metrics message format to '
                                  'publish to the message queue'),
                  cfg.StrOpt('events_message_format', default='reference',
                             help='The type of events message format to '
                                  'publish to the message queue')]

messaging_group = cfg.OptGroup(name='messaging', title='messaging')
cfg.CONF.register_group(messaging_group)
cfg.CONF.register_opts(messaging_opts, messaging_group)

base_sqla_path = 'monasca_api.common.repositories.sqla.'
repositories_opts = [
    cfg.StrOpt('metrics_driver',
               default='monasca_api.common.repositories.influxdb.metrics_repository:MetricsRepository',
               help='The repository driver to use for metrics'),
    cfg.StrOpt('alarm_definitions_driver',
               default=base_sqla_path + 'alarm_definitions_repository:AlarmDefinitionsRepository',
               help='The repository driver to use for alarm definitions'),
    cfg.StrOpt('alarms_driver',
               default=base_sqla_path + 'alarms_repository:AlarmsRepository',
               help='The repository driver to use for alarms'),
    cfg.StrOpt('notifications_driver',
               default=base_sqla_path + 'notifications_repository:NotificationsRepository',
               help='The repository driver to use for notifications'),
    cfg.StrOpt('notification_method_type_driver',
               default=base_sqla_path + 'notification_method_type_repository:NotificationMethodTypeRepository',
               help='The repository driver to use for notifications')]

repositories_group = cfg.OptGroup(name='repositories', title='repositories')
cfg.CONF.register_group(repositories_group)
cfg.CONF.register_opts(repositories_opts, repositories_group)


kafka_opts = [cfg.StrOpt('uri', help='Address to kafka server. For example: '
                                     'uri=192.168.1.191:9092'),
              cfg.StrOpt('metrics_topic', default='metrics',
                         help='The topic that metrics will be published too.',
                         advanced=True),
              cfg.StrOpt('events_topic', default='events',
                         help='The topic that events will be published too.',
                         advanced=True),
              cfg.StrOpt('alarm_state_transitions_topic', default='alarm-state-transitions',
                         help='The topic that alarm state will be published too.',
                         advanced=True),
              cfg.StrOpt('group', default='api',
                         help='The group name that this service belongs to.'),
              cfg.IntOpt('wait_time', default=1,
                         help='The wait time when no messages on kafka '
                              'queue.'), cfg.IntOpt('ack_time', default=20,
                                                    help='The ack time back '
                                                         'to kafka.'),
              cfg.IntOpt('max_retry', default=3,
                         help='The number of retry when there is a '
                              'connection error.'),
              cfg.BoolOpt('auto_commit', default=False,
                          help='If automatically commmit when consume '
                               'messages.'),
              cfg.BoolOpt('async', default=True, help='The type of posting.'),
              cfg.BoolOpt('compact', default=True, help=(
                  'Specify if the message received should be parsed.'
                  'If True, message will not be parsed, otherwise '
                  'messages will be parsed.')),
              cfg.MultiOpt('partitions', item_type=types.Integer(),
                           default=0,
                           help='The partitions this connection should '
                                'listen for messages on. Currently does not '
                                'support multiple partitions. '
                                'Default is to listen on partition 0.'),
              cfg.BoolOpt('drop_data', default=False, help=(
                  'Specify if received data should be simply dropped. '
                  'This parameter is only for testing purposes.')), ]

kafka_group = cfg.OptGroup(name='kafka', title='title')
cfg.CONF.register_group(kafka_group)
cfg.CONF.register_opts(kafka_opts, kafka_group)

influxdb_opts = [cfg.StrOpt('database_name'), cfg.StrOpt('ip_address'),
                 cfg.StrOpt('port'), cfg.StrOpt('user'),
                 cfg.StrOpt('password', secret=True)]

influxdb_group = cfg.OptGroup(name='influxdb', title='influxdb')
cfg.CONF.register_group(influxdb_group)
cfg.CONF.register_opts(influxdb_opts, influxdb_group)

cassandra_opts = [cfg.StrOpt('cluster_ip_addresses'), cfg.StrOpt('keyspace')]

cassandra_group = cfg.OptGroup(name='cassandra', title='cassandra')
cfg.CONF.register_group(cassandra_group)
cfg.CONF.register_opts(cassandra_opts, cassandra_group)


def register_database_opts():
    # Update the default QueuePool parameters. These can be tweaked by the
    # conf variables - max_pool_size, max_overflow and pool_timeout

    options.set_defaults(cfg.CONF, connection='sqlite://',
                         max_pool_size=10, max_overflow=20,
                         pool_timeout=10)

    # register old value
    url_opt = cfg.StrOpt(name='url',
                         default=cfg.CONF.database.connection,
                         required=False,
                         deprecated_for_removal=True,
                         deprecated_since='1.6.0',
                         deprecated_reason=(
                             'Please use database.connection option,'
                             'database.url is scheduled for removal '
                             'in Pike release')
                         )

    cfg.CONF.register_opts([url_opt], group='database')
    cfg.CONF.set_override(name='connection', group='database',
                          override=cfg.CONF.database.url)

register_database_opts()


# support URL as an option till Pike is released
# TODO(trebskit) remove in Pike release
