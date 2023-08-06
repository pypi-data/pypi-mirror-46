#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pika
import functools

__name__ = "puanchen"
__version__ = '0.0.3'
__author__ = 'ClaireHuang'
__author_email__ = 'clairehf@163.com'


class HeraldMQ(object):
    def __init__(self, host, port, vhost, user, password, heartbeat=0):
        credentials = pika.PlainCredentials(user, password)
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host, port, vhost, credentials, heartbeat=heartbeat
        ))
        self.channel = self.connection.channel()

    def declare_queue(self, queue_name):
        self.channel.queue_declare(queue=queue_name, durable=True)

    def declare_delay_queue(self, queue_name, ttl):
        delay_queue_name = queue_name + "_delay"
        self.channel.queue_declare(queue=queue_name, durable=True)
        self.channel.queue_bind(exchange='amq.direct', queue=queue_name,
                                routing_key=queue_name)
        self.channel.queue_declare(queue=delay_queue_name, durable=True,
                            arguments={
                                'x-message-ttl': ttl,
                                'x-dead-letter-exchange': 'amq.direct',
                                'x-dead-letter-routing-key': queue_name
                            })

    def send_message(self, queue_name, body):
        self.channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            body=body,
            properties=pika.BasicProperties(delivery_mode=2)
        )

    def send_delay_message(self, queue_name, body):
        delay_queue_name = queue_name + "_delay"
        self.send_message(delay_queue_name, body)

    def close_connection(self):
        self.connection.close()

    def _on_message(self, chan, method_frame, _header_frame, body,
                   consume_func=None):
        """Called when a message is received."""
        result = consume_func(body)
        if result == "complete":
            chan.basic_ack(delivery_tag=method_frame.delivery_tag)
        elif result == "requeue":
            chan.basic_reject(delivery_tag=method_frame.delivery_tag)

    def worker(self, queue_name, func):
        self.channel.basic_qos(prefetch_count=1)
        on_message_callback = functools.partial(self._on_message,
                                                consume_func=func)
        self.channel.basic_consume(queue_name, on_message_callback)
        self.channel.start_consuming()
