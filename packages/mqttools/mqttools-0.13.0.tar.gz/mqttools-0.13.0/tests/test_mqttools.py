import sys
import logging
import asyncio
import unittest
import threading
import binascii
import queue
import socket
from unittest.mock import patch
from io import StringIO

import mqttools
from mqttools import QoS


HOST = 'localhost'
PORT = 0


class Broker(threading.Thread):

    EXPECTED_DATA_INDEX = 0
    EXPECTED_DATA_STREAM = []
    ACTUAL_DATA_STREAM = []

    def __init__(self):
        super().__init__()
        self._listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._listener.bind((HOST, PORT))
        self._listener.listen()
        self._client_closed = queue.Queue()

    @property
    def address(self):
        return self._listener.getsockname()

    def wait_for_client_closed(self):
        self._client_closed.get(timeout=1)

    def run(self):
        while True:
            print('Broker: Listening for client...')
            self.serve_client(self._listener.accept()[0])
            self._client_closed.put(True)

    def serve_client(self, client):
        print('Broker: Serving client...')

        while self.EXPECTED_DATA_INDEX < len(self.EXPECTED_DATA_STREAM):
            _, data = self.EXPECTED_DATA_STREAM[self.EXPECTED_DATA_INDEX]
            self.EXPECTED_DATA_INDEX += 1

            size = len(data)
            data = client.recv(size)
            # print(f'Broker: Received: {data}')
            self.ACTUAL_DATA_STREAM.append(('c2s', data))

            while self.EXPECTED_DATA_INDEX < len(self.EXPECTED_DATA_STREAM):
                direction, data = self.EXPECTED_DATA_STREAM[self.EXPECTED_DATA_INDEX]

                if direction != 's2c':
                    break

                self.EXPECTED_DATA_INDEX += 1
                # print(f'Broker: Sending: {data}')
                client.send(data)
                self.ACTUAL_DATA_STREAM.append(('s2c', data))

        client.close()


class MQTToolsTest(unittest.TestCase):

    def setUp(self):
        Broker.EXPECTED_DATA_INDEX = 0
        Broker.EXPECTED_DATA_STREAM = []
        Broker.ACTUAL_DATA_STREAM = []
        Broker.CLOSE_AFTER_INDEX = -1
        self.broker = Broker()
        self.broker.daemon = True
        self.broker.start()
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def tearDown(self):
        self.broker.wait_for_client_closed()
        self.loop.close()
        self.assertEqual(Broker.ACTUAL_DATA_STREAM, Broker.EXPECTED_DATA_STREAM)

    def run_until_complete(self, coro):
        return self.loop.run_until_complete(coro)

    def test_start_stop(self):
        Broker.EXPECTED_DATA_STREAM = [
            # CONNECT
            ('c2s', b'\x10\x10\x00\x04MQTT\x05\x02\x00\x00\x00\x00\x03bar'),
            # CONNACK
            ('s2c', b'\x20\x03\x00\x00\x00'),
            # DISCONNECT
            ('c2s', b'\xe0\x02\x00\x00')
        ]

        client = mqttools.Client(*self.broker.address, 'bar')
        self.run_until_complete(client.start())
        self.run_until_complete(client.stop())

    def test_subscribe(self):
        Broker.EXPECTED_DATA_STREAM = [
            # CONNECT
            ('c2s', b'\x10\x10\x00\x04MQTT\x05\x02\x00\x00\x00\x00\x03bar'),
            # CONNACK
            ('s2c', b'\x20\x03\x00\x00\x00'),
            # SUBSCRIBE
            ('c2s', b'\x82\n\x00\x01\x00\x00\x04/a/b\x00'),
            # SUBACK
            ('s2c', b'\x90\x04\x00\x01\x00\x00'),
            # SUBSCRIBE
            ('c2s', b'\x82\n\x00\x02\x00\x00\x04/a/c\x00'),
            # SUBACK
            ('s2c', b'\x90\x04\x00\x02\x00\x00'),
            # PUBLISH QoS 0
            ('s2c', b'\x30\x0a\x00\x04/a/b\x00apa'),
            # DISCONNECT
            ('c2s', b'\xe0\x02\x00\x00')
        ]

        client = mqttools.Client(*self.broker.address, 'bar')
        self.run_until_complete(client.start())
        self.run_until_complete(client.subscribe('/a/b'))
        self.run_until_complete(client.subscribe('/a/c'))
        topic, message = self.run_until_complete(client.messages.get())
        self.assertEqual(topic, '/a/b')
        self.assertEqual(message, b'apa')
        self.run_until_complete(client.stop())

    def test_unsubscribe(self):
        Broker.EXPECTED_DATA_STREAM = [
            # CONNECT
            ('c2s', b'\x10\x10\x00\x04MQTT\x05\x02\x00\x00\x00\x00\x03bar'),
            # CONNACK
            ('s2c', b'\x20\x03\x00\x00\x00'),
            # SUBSCRIBE
            ('c2s', b'\x82\n\x00\x01\x00\x00\x04/a/b\x00'),
            # SUBACK
            ('s2c', b'\x90\x04\x00\x01\x00\x00'),
            # UNSUBSCRIBE
            ('c2s', b'\xa2\x09\x00\x02\x00\x00\x04/a/b'),
            # UNSUBACK
            ('s2c', b'\xb0\x04\x00\x02\x00\x00'),
            # DISCONNECT
            ('c2s', b'\xe0\x02\x00\x00')
        ]

        client = mqttools.Client(*self.broker.address, 'bar')
        self.run_until_complete(client.start())
        self.run_until_complete(client.subscribe('/a/b'))
        self.run_until_complete(client.unsubscribe('/a/b'))
        self.run_until_complete(client.stop())

    def test_publish_qos_0(self):
        Broker.EXPECTED_DATA_STREAM = [
            # CONNECT
            ('c2s', b'\x10\x10\x00\x04MQTT\x05\x02\x00\x00\x00\x00\x03bar'),
            # CONNACK
            ('s2c', b'\x20\x03\x00\x00\x00'),
            # PUBLISH
            ('c2s', b'\x30\x0a\x00\x04/a/b\x00apa'),
            # DISCONNECT
            ('c2s', b'\xe0\x02\x00\x00')
        ]

        client = mqttools.Client(*self.broker.address, 'bar')
        self.run_until_complete(client.start())
        client.publish('/a/b', b'apa')
        self.run_until_complete(client.stop())

    def test_command_line_publish_qos_0(self):
        Broker.EXPECTED_DATA_STREAM = [
            # CONNECT
            ('c2s', b'\x10\x1d\x00\x04MQTT\x05\x02\x00\x00\x00\x00\x10mqttools_publish'),
            # CONNACK
            ('s2c', b'\x20\x03\x00\x00\x00'),
            # PUBLISH
            ('c2s', b'\x30\x0a\x00\x04/a/b\x00apa'),
            # DISCONNECT
            ('c2s', b'\xe0\x02\x00\x00')
        ]

        argv = [
            'mqttools',
            'publish',
            '--host', self.broker.address[0],
            '--port', str(self.broker.address[1]),
            '--client-id', 'mqttools_publish',
            '/a/b',
            'apa'
        ]

        stdout = StringIO()

        with patch('sys.stdout', stdout):
            with patch('sys.argv', argv):
                mqttools.main()

        self.assertIn('Published 1 message(s) in', stdout.getvalue())

    def test_command_line_publish_qos_0_generate_message(self):
        Broker.EXPECTED_DATA_STREAM = [
            # CONNECT
            ('c2s', b'\x10\x1d\x00\x04MQTT\x05\x02\x00\x00\x00\x00\x10mqttools_publish'),
            # CONNACK
            ('s2c', b'\x20\x03\x00\x00\x00'),
            # PUBLISH
            ('c2s', b'\x30\x11\x00\x04/a/b\x000\xa5\xa5\xa5\xa5\xa5\xa5\xa5\xa5\xa5'),
            # DISCONNECT
            ('c2s', b'\xe0\x02\x00\x00')
        ]

        argv = [
            'mqttools',
            'publish',
            '--host', self.broker.address[0],
            '--port', str(self.broker.address[1]),
            '--client-id', 'mqttools_publish',
            '--size', '10',
            '/a/b'
        ]

        stdout = StringIO()

        with patch('sys.stdout', stdout):
            with patch('sys.argv', argv):
                mqttools.main()

        self.assertIn('Published 1 message(s) in', stdout.getvalue())

    def test_command_line_publish_qos_0_generate_short_message(self):
        Broker.EXPECTED_DATA_STREAM = [
            # CONNECT
            ('c2s', b'\x10\x1d\x00\x04MQTT\x05\x02\x00\x00\x00\x00\x10mqttools_publish'),
            # CONNACK
            ('s2c', b'\x20\x03\x00\x00\x00'),
            # PUBLISH
            ('c2s', b'\x30\x08\x00\x04/a/b\x000'),
            # PUBLISH
            ('c2s', b'\x30\x08\x00\x04/a/b\x000'),
            # PUBLISH
            ('c2s', b'\x30\x08\x00\x04/a/b\x000'),
            # PUBLISH
            ('c2s', b'\x30\x08\x00\x04/a/b\x000'),
            # PUBLISH
            ('c2s', b'\x30\x08\x00\x04/a/b\x000'),
            # PUBLISH
            ('c2s', b'\x30\x08\x00\x04/a/b\x000'),
            # PUBLISH
            ('c2s', b'\x30\x08\x00\x04/a/b\x000'),
            # PUBLISH
            ('c2s', b'\x30\x08\x00\x04/a/b\x000'),
            # PUBLISH
            ('c2s', b'\x30\x08\x00\x04/a/b\x000'),
            # PUBLISH
            ('c2s', b'\x30\x08\x00\x04/a/b\x000'),
            # PUBLISH
            ('c2s', b'\x30\x08\x00\x04/a/b\x001'),
            # DISCONNECT
            ('c2s', b'\xe0\x02\x00\x00')
        ]

        argv = [
            'mqttools',
            'publish',
            '--host', self.broker.address[0],
            '--port', str(self.broker.address[1]),
            '--client-id', 'mqttools_publish',
            '--count', '11',
            '--size', '1',
            '/a/b'
        ]

        stdout = StringIO()

        with patch('sys.stdout', stdout):
            with patch('sys.argv', argv):
                mqttools.main()

        self.assertIn('Published 11 message(s) in', stdout.getvalue())

    def test_publish_topic_alias(self):
        Broker.EXPECTED_DATA_STREAM = [
            # CONNECT
            ('c2s', b'\x10\x10\x00\x04MQTT\x05\x02\x00\x00\x00\x00\x03bar'),
            # CONNACK with topic alias 5
            ('s2c', b'\x20\x06\x00\x00\x03\x22\x00\x05'),
            # PUBLISH to set alias
            (
                'c2s',
                b'\x30\x2c\x00\x12/test/mqttools/foo\x03\x23\x00\x01'
                b'sets-alias-in-broker'
            ),
            # PUBLISH using alias
            ('c2s', b'\x30\x1a\x00\x00\x03\x23\x00\x01published-with-alias'),
            # PUBLISH without alias
            ('c2s', b'\x30\x24\x00\x12/test/mqttools/fie\x00not-using-alias'),
            # DISCONNECT
            ('c2s', b'\xe0\x02\x00\x00')
        ]

        client = mqttools.Client(*self.broker.address,
                                 'bar',
                                 topic_aliases=[
                                     '/test/mqttools/foo'
                                 ])
        self.run_until_complete(client.start())
        client.publish('/test/mqttools/foo', b'sets-alias-in-broker')
        client.publish('/test/mqttools/foo', b'published-with-alias')
        client.publish('/test/mqttools/fie', b'not-using-alias')
        self.run_until_complete(client.stop())

    def test_use_all_topic_aliases(self):
        Broker.EXPECTED_DATA_STREAM = [
            # CONNECT
            ('c2s', b'\x10\x10\x00\x04MQTT\x05\x02\x00\x00\x00\x00\x03bar'),
            # CONNACK with topic alias 1
            ('s2c', b'\x20\x06\x00\x00\x03\x22\x00\x01'),
            # PUBLISH to set alias
            ('c2s', b'\x30\x0d\x00\x04/foo\x03\x23\x00\x01apa'),
            # PUBLISH, no alias available
            ('c2s', b'\x30\x0a\x00\x04/bar\x00cat'),
            # DISCONNECT
            ('c2s', b'\xe0\x02\x00\x00')
        ]

        client = mqttools.Client(*self.broker.address,
                                 'bar',
                                 topic_aliases=[
                                     '/foo'
                                 ])
        self.run_until_complete(client.start())
        client.publish('/foo', b'apa')
        client.publish('/bar', b'cat')
        self.run_until_complete(client.stop())

    def test_connack_unspecified_error(self):
        Broker.EXPECTED_DATA_STREAM = [
            # CONNECT
            ('c2s', b'\x10\x10\x00\x04MQTT\x05\x02\x00\x00\x00\x00\x03bar'),
            # CONNACK with unspecified error
            ('s2c', b'\x20\x03\x00\x80\x00')
        ]

        client = mqttools.Client(*self.broker.address, 'bar')

        with self.assertRaises(mqttools.ConnectError) as cm:
            self.run_until_complete(client.start())

        self.assertEqual(str(cm.exception), 'UNSPECIFIED_ERROR(128)')

    def test_receive_topic_alias(self):
        Broker.EXPECTED_DATA_STREAM = [
            # CONNECT with topic alias 5
            (
                'c2s',
                b'\x10\x13\x00\x04MQTT\x05\x02\x00\x00\x03\x22\x00\x05\x00\x03bar'
            ),
            # CONNACK
            ('s2c', b'\x20\x03\x00\x00\x00'),
            # SUBSCRIBE
            ('c2s', b'\x82\x18\x00\x01\x00\x00\x12/test/mqttools/foo\x00'),
            # SUBACK
            ('s2c', b'\x90\x04\x00\x01\x00\x00'),
            # PUBLISH to set alias
            (
                's2c',
                b'\x30\x2c\x00\x12/test/mqttools/foo\x03\x23\x00\x01'
                b'sets-alias-in-client'
            ),
            # PUBLISH using alias
            ('s2c', b'\x30\x1a\x00\x00\x03\x23\x00\x01published-with-alias'),
            # DISCONNECT
            ('c2s', b'\xe0\x02\x00\x00')
        ]

        client = mqttools.Client(*self.broker.address,
                                 'bar',
                                 topic_alias_maximum=5)
        self.run_until_complete(client.start())
        self.run_until_complete(client.subscribe('/test/mqttools/foo'))
        topic, message = self.run_until_complete(client.messages.get())
        self.assertEqual(topic, '/test/mqttools/foo')
        self.assertEqual(message, b'sets-alias-in-client')
        topic, message = self.run_until_complete(client.messages.get())
        self.assertEqual(topic, '/test/mqttools/foo')
        self.assertEqual(message, b'published-with-alias')
        self.run_until_complete(client.stop())


logging.basicConfig(level=logging.DEBUG)


if __name__ == '__main__':
    unittest.main()
