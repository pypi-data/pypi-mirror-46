# Created by Antonio Di Mariano (antonio_dimariano@trendmicro.com) at 2019-05-17

from confluent_kafka import Consumer
from messaging_middleware.utils.logger import Logger
import configuration_layer.helpers.producer_messages as message
from confluent_kafka import TopicPartition, KafkaException, KafkaError, OFFSET_END
from concurrent.futures import ThreadPoolExecutor
import threading
import logging
import sys
import time
import datetime
import os
import json
import uuid

logger = Logger(ssl=os.environ.get('security_protocol', 0))


def delivery_callback(err, msg):
    if err:
        sys.stderr.write('%% Message failed delivery: %s\n' % err)
    else:
        sys.stderr.write('%% Message delivered to %s [%d] @ %o\n' %
                         (msg.topic(), msg.partition(), msg.offset()))



class ConfigurationConsumer(threading.Thread):

    def __init__(self, **kwargs):
        self.group_id = 'configuration_seeker_' + str(uuid.uuid1())
        self.service_name = kwargs.get('service_name', None)
        self.bootstrap_servers = kwargs.get('bootstrap_servers', None)
        self.security_protocol = kwargs.get('security_protocol', 'plaintext')
        self.consumer_topic = kwargs.get('consumer_topic', None)
        self.initial_conf_set_eh = kwargs.get('initial_conf_set_eh')
        self.consumer_ready_eh = kwargs.get('consumer_ready_eh')
        self.consumer = Consumer({'bootstrap.servers': self.bootstrap_servers,
                                  'group.id': self.group_id,
                                  'session.timeout.ms': 6000,
                                  'enable.auto.commit': 'true',
                                  'log.connection.close': 'false',
                                  'default.topic.config': {'auto.offset.reset': 'latest'},
                                  'security.protocol': self.security_protocol,
                                  'ssl.ca.location': "./configuration/cacert.pem",

                                  })

        self.consumer.subscribe([self.consumer_topic], on_assign=self.do_assign)
        self.initial_configuration_set = kwargs.get('set', 0)
        self.breakable = kwargs.get('breakable', 1)
        self.configuration_directory = kwargs.get('service_configuration_directory', 'configuration')
        threading.Thread.__init__(self, name='the_seeker')

        self.executor = ThreadPoolExecutor(
            max_workers=5)  # this thread pool will only have 5 concurrent threads that can process any jobs that I submit to
        if self.security_protocol == 'ssl':
            self.logger = Logger(ssl=1)
        else:
            self.logger = Logger()

    def do_assign(self,consumer, partitions):
        for tp in partitions:
            lo, hi = consumer.get_watermark_offsets(tp)
            if hi <= 0:
                logger.logmsg('info', "No previous offset (empty partition): skip to end", consumer)
                # No previous offset (empty partition): skip to end
                tp.offset = OFFSET_END
            else:
                tp.offset = hi
        logger.logmsg('info', 'Partitions available:', partitions)
        consumer.assign(partitions)
        self.consumer_ready_eh.set()
        self.logger.logmsg('debug', 'Configuration consumer ready.')

    def stop(self):
        self.consumer.close()

    def run(self):
        self.logger.logmsg('info', "Configuration Request Version 1.2")
        try:
            while True:
                m = self.consumer.poll(1)
                "'if no messages are coming and if I haven't received a configuration, a message will be sent every 10 seconds in order to request the service configuration'"
                if m is None:
                   continue

                if m.error() is None:

                    # HEre I got a message

                    self.logger.logmsg('info', 'Received message', m.value(), m.offset())
                    message_payload = m.value()
                    data_json = json.loads(message_payload.decode('ascii'))
                    "'If the receiver of the message is the same of the service name, the configuration will be saved as a JSON file. The consumer will stay active in case of updates"
                    if data_json['service_name'] == self.service_name:

                        self.executor.submit(
                            self.update_my_service_configuration(configuration_to_update=message_payload))
                        if self.breakable:
                            break
                else:
                    self.logger.logmsg('error', "Error in the configuration consumer")
                    continue

        except KeyboardInterrupt:
            sys.stderr.write('%% Aborted by user\n')
            self.consumer.close()

    def update_my_service_configuration(self, configuration_to_update):
        try:
            self.logger.logmsg('info', "Service Configuration Received.")

            with open(self.configuration_directory + '/service_configuration.json', 'w') as outfile:
                outfile.write(configuration_to_update.decode('utf8'))
                outfile.close()
                message_to_produce = message.operation_result(service_name=self.service_name,
                                                              last_operation='setconf',
                                                              timestamp=datetime.datetime.now(
                                                                  datetime.timezone.utc).strftime(
                                                                  '%Y-%m-%dT%H:%M:%S%z'),
                                                              operation_result=message.const_values()[
                                                                  'SUCCESS']
                                                              )
        except ValueError as e:
            message_to_produce = message.operation_result(service_name=self.service_name,
                                                          last_operation='setconf',
                                                          timestamp=datetime.datetime.now(
                                                              datetime.timezone.utc).strftime(
                                                              '%Y-%m-%dT%H:%M:%S%z'),
                                                          operation_result=message.const_values()[
                                                              'FAIL'],
                                                          error_description=e)

        "'notify I've just got the configuration!'"
        self.logger.produce_msg(message_to_produce)

        if self.breakable:
            self.logger.logmsg('info', 'Initial Configuration received successfully. Exit now')
            self.initial_conf_set_eh.set()

        else:
            self.logger.logmsg('info', 'Service Configuration updated successfully')

        self.initial_configuration_set = 1
