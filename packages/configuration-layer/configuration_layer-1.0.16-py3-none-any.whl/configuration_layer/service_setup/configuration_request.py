import os
import threading
import logging
import sys
import time
from configuration_layer.classes.ConfigurationConsumer import ConfigurationConsumer
from configuration_layer.classes.ConfigurationProducer import ConfigurationProducer
from messaging_middleware.utils.logger import Logger



class ConfigurationSeeker(threading.Thread):
    def __init__(self, **kwargs):
        logging.basicConfig(
            format='%(asctime)s.%(msecs)s:%(name)s:%(thread)d:%(levelname)s:%(process)d:%(message)s',
            level=logging.INFO
        )
        logging.getLogger('urllib3.connectionpool').setLevel(logging.ERROR)
        threading.Thread.__init__(self, name='the_seeker')
        self.logger = Logger(ssl=os.environ.get('security_protocol', 0))
        self.message = kwargs.get('message', None)
        self.consumer_ready_eh = threading.Event()
        self.initial_conf_set_eh = threading.Event()
        self.configuration_already_set = kwargs.get('set',0)
        self.get_configuration_and_exit = kwargs.get('breakable',1)
        self.service_name = kwargs.get('service_name', None)

        self.configuration_product = ConfigurationProducer(
            bootstrap_servers=kwargs.get('bootstrap_servers', None),
            producer_topic=kwargs.get('producer_topic', None),
            security_protocol=kwargs.get('security_protocol', 'plaintext'),
            schema_registry=os.environ.get('schema_registry',
                                           'http://edc2rdwdocker01.eu.trendnet.org:8081'),
        )

        self.configuration_consumer = ConfigurationConsumer(
            bootstrap_servers=kwargs.get('bootstrap_servers', None),
            consumer_topic=kwargs.get('consumer_topic', None),
            consumer_ready_eh=self.consumer_ready_eh,
            breakable=self.get_configuration_and_exit,
            initial_conf_set_eh=self.initial_conf_set_eh,
            service_name=self.service_name,
            security_protocol=kwargs.get('security_protocol', 'plaintext')

        )

    def run(self):
        try:
            self.configuration_consumer.start()
            while True:
                if self.consumer_ready_eh.is_set():
                    if not self.configuration_already_set:
                            if self.initial_conf_set_eh.is_set() and self.get_configuration_and_exit:
                                break
                            else:
                                self.logger.logmsg('debyg','Requesting my configuration..')
                                self.configuration_product.request_service_configuration(message_to_send=self.message,
                                                                                     service_name=self.service_name)
                                time.sleep(5.0)
                                continue
                    else:
                        break



        except KeyboardInterrupt:
            sys.stderr.write('%% Aborted by user\n')