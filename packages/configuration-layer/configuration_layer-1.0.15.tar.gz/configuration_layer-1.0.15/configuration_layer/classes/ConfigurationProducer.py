# Created by Antonio Di Mariano (antonio_dimariano@trendmicro.com) at 2019-05-17

import configuration_layer.helpers.producer_messages as message
import datetime
from messaging_middleware.utils.logger import Logger
from messaging_middleware.avro_communication_layer.Producer import Producer

default_schema = key_schema={"service_name": "tc-labs-availability-watcher"}

class ConfigurationProducer:

    def __init__(self, **kwargs):
        self.producer_topic = kwargs.get('producer_topic', None)
        self.schema_registry = kwargs.get('schema_registry', None)
        self.bootstrap_servers = kwargs.get('bootstrap_servers', None)
        self.security_protocol = kwargs.get('security_protocol', 'plaintext')
        self.producer = Producer(
            bootstrap_servers=self.bootstrap_servers,
            schema_reqistry_url=self.schema_registry,
            topic=self.producer_topic,
            security_protocol=self.security_protocol)
        if self.security_protocol == 'ssl':
            self.logger = Logger(ssl=1)
        else:
            self.logger = Logger()

    def request_service_configuration(self,**kwargs):
        message_to_send = kwargs.get('message_to_send',{})
        service_name = kwargs.get('service_name')
        ret = self.producer.produce_message(value=message_to_send, key=default_schema)
        self.logger.logmsg('debug', 'Requesting my configuration..', ret)
        message_to_produce = message.operation_result(service_name=service_name,
                                                      last_operation='getconf',
                                                      timestamp=datetime.datetime.now(
                                                          datetime.timezone.utc).strftime(
                                                          '%Y-%m-%dT%H:%M:%S%z'),
                                                      operation_result=message.const_values()[
                                                          'PENDING'])
        self.logger.produce_msg(message_to_produce)
