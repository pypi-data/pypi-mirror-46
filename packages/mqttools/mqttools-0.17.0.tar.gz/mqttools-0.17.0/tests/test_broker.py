import logging
import asyncio
import unittest

import mqttools


class BrokerTest(unittest.TestCase):

    def test_multiple_subscribers(self):
        asyncio.run(self.multiple_subscribers())

    async def multiple_subscribers(self):
        broker = mqttools.Broker('localhost', 0)

        async def broker_wrapper():
            with self.assertRaises(asyncio.CancelledError):
                await broker.serve_forever()

        broker_task = asyncio.create_task(broker_wrapper())

        async def tester():
            address = await broker.getsockname()

            # Setup subscriber 1.
            reader_1, writer_1 = await asyncio.open_connection(*address)
            connect = b'\x10\x10\x00\x04MQTT\x05\x02\x00\x00\x00\x00\x03su1'
            writer_1.write(connect)
            connack = await reader_1.readexactly(7)
            self.assertEqual(connack, b'\x20\x05\x00\x00\x02\x24\x00')
            subscribe = b'\x82\x0a\x00\x01\x00\x00\x04/a/b\x00'
            writer_1.write(subscribe)
            suback = await reader_1.readexactly(6)
            self.assertEqual(suback, b'\x90\x04\x00\x01\x00\x00')

            # Setup subscriber 2.
            reader_2, writer_2 = await asyncio.open_connection(*address)
            connect = b'\x10\x10\x00\x04MQTT\x05\x02\x00\x00\x00\x00\x03su2'
            writer_2.write(connect)
            connack = await reader_2.readexactly(7)
            self.assertEqual(connack, b'\x20\x05\x00\x00\x02\x24\x00')
            subscribe = b'\x82\x0a\x00\x01\x00\x00\x04/a/b\x00'
            writer_2.write(subscribe)
            suback = await reader_2.readexactly(6)
            self.assertEqual(suback, b'\x90\x04\x00\x01\x00\x00')

            # Setup a publisher.
            reader_3, writer_3 = await asyncio.open_connection(*address)
            connect = b'\x10\x10\x00\x04MQTT\x05\x02\x00\x00\x00\x00\x03pub'
            writer_3.write(connect)
            connack = await reader_3.readexactly(7)
            self.assertEqual(connack, b'\x20\x05\x00\x00\x02\x24\x00')

            # Publish a topic.
            publish = b'\x30\x0a\x00\x04/a/b\x00apa'
            writer_3.write(publish)

            # Receive the publish in both subscribers.
            publish = await reader_1.readexactly(12)
            self.assertEqual(publish, b'\x30\x0a\x00\x04/a/b\x00apa')
            publish = await reader_2.readexactly(12)
            self.assertEqual(publish, b'\x30\x0a\x00\x04/a/b\x00apa')

            # Cleanly disconnect subscriber 1.
            disconnect = b'\xe0\x02\x00\x00'
            writer_1.write(disconnect)
            writer_1.close()

            # Publish another topic, now only to subscriber 2.
            publish = b'\x30\x0a\x00\x04/a/b\x00boo'
            writer_3.write(publish)

            # Receive the publish in subscriber 2.
            publish = await reader_2.readexactly(12)
            self.assertEqual(publish, b'\x30\x0a\x00\x04/a/b\x00boo')

            # Subscribe to /+/b is an invalid topic in the current
            # implementation.
            subscribe = b'\x82\x0a\x00\x01\x00\x00\x04/+/b\x00'
            writer_2.write(subscribe)
            suback = await reader_2.readexactly(6)
            self.assertEqual(suback, b'\x90\x04\x00\x01\x00\xa2')

            writer_2.close()
            writer_3.close()
            broker_task.cancel()

        await asyncio.wait_for(asyncio.gather(broker_task, tester()), 1)

    def test_unsubscribe(self):
        asyncio.run(self.unsubscribe())

    async def unsubscribe(self):
        broker = mqttools.Broker('localhost', 0)

        async def broker_wrapper():
            with self.assertRaises(asyncio.CancelledError):
                await broker.serve_forever()

        broker_task = asyncio.create_task(broker_wrapper())

        async def tester():
            address = await broker.getsockname()

            # Setup the subscriber. Subscribe to /a/a, /a/b, /a/c and /a/d.
            reader_1, writer_1 = await asyncio.open_connection(*address)
            connect = b'\x10\x10\x00\x04MQTT\x05\x02\x00\x00\x00\x00\x03su1'
            writer_1.write(connect)
            connack = await reader_1.readexactly(7)
            self.assertEqual(connack, b'\x20\x05\x00\x00\x02\x24\x00')
            subscribe = (
                b'\x82\x1f\x00\x01\x00\x00\x04/a/a\x00\x00\x04/a/b\x00\x00\x04'
                b'/a/c\x00\x00\x04/a/d\x00')
            writer_1.write(subscribe)
            suback = await reader_1.readexactly(9)
            self.assertEqual(suback, b'\x90\x07\x00\x01\x00\x00\x00\x00\x00')

            # Setup a publisher.
            reader_2, writer_2 = await asyncio.open_connection(*address)
            connect = b'\x10\x10\x00\x04MQTT\x05\x02\x00\x00\x00\x00\x03pub'
            writer_2.write(connect)
            connack = await reader_2.readexactly(7)
            self.assertEqual(connack, b'\x20\x05\x00\x00\x02\x24\x00')

            # Publish /a/a and /a/c.
            publish = b'\x30\x0a\x00\x04/a/a\x00apa'
            writer_2.write(publish)
            publish = b'\x30\x0a\x00\x04/a/c\x00cow'
            writer_2.write(publish)

            # Receive /a/a and /a/c in the subscriber.
            publish = await reader_1.readexactly(12)
            self.assertEqual(publish, b'\x30\x0a\x00\x04/a/a\x00apa')
            publish = await reader_1.readexactly(12)
            self.assertEqual(publish, b'\x30\x0a\x00\x04/a/c\x00cow')

            # Unsubscribe from /a/a and /a/c.
            unsubscribe = b'\xa2\x0f\x00\x02\x00\x00\x04/a/a\x00\x04/a/c'
            writer_1.write(unsubscribe)
            unsuback = await reader_1.readexactly(7)
            self.assertEqual(unsuback, b'\xb0\x05\x00\x02\x00\x00\x00')

            # Publish /a/a, /a/c and then /a/b, /a/a should not be
            # received by the subscriber.
            publish = b'\x30\x0a\x00\x04/a/a\x00apa'
            writer_2.write(publish)
            publish = b'\x30\x0a\x00\x04/a/c\x00cow'
            writer_2.write(publish)
            publish = b'\x30\x0a\x00\x04/a/b\x00mas'
            writer_2.write(publish)

            # Receive /a/b in the subscriber.
            publish = await reader_1.readexactly(12)
            self.assertEqual(publish, b'\x30\x0a\x00\x04/a/b\x00mas')

            # Unsubscribe from /a/b.
            unsubscribe = b'\xa2\x09\x00\x02\x00\x00\x04/a/b'
            writer_1.write(unsubscribe)
            unsuback = await reader_1.readexactly(6)
            self.assertEqual(unsuback, b'\xb0\x04\x00\x02\x00\x00')

            # Unsubscribe from /a/b again should fail.
            unsubscribe = b'\xa2\x09\x00\x02\x00\x00\x04/a/b'
            writer_1.write(unsubscribe)
            unsuback = await reader_1.readexactly(6)
            self.assertEqual(unsuback, b'\xb0\x04\x00\x02\x00\x11')

            # Unsubscribe from /a/# is an invalid topic in the current
            # implementation.
            unsubscribe = b'\xa2\x09\x00\x02\x00\x00\x04/a/#'
            writer_1.write(unsubscribe)
            unsuback = await reader_1.readexactly(6)
            self.assertEqual(unsuback, b'\xb0\x04\x00\x02\x00\x11')

            # Publish /a/b and then /a/d, /a/b should not be received
            # by the subscriber.
            publish = b'\x30\x0a\x00\x04/a/b\x00apa'
            writer_2.write(publish)
            publish = b'\x30\x0a\x00\x04/a/d\x00mas'
            writer_2.write(publish)

            # Receive /a/d in the subscriber.
            publish = await reader_1.readexactly(12)
            self.assertEqual(publish, b'\x30\x0a\x00\x04/a/d\x00mas')

            writer_1.close()
            writer_2.close()
            broker_task.cancel()

        await asyncio.wait_for(asyncio.gather(broker_task, tester()), 1)

    def test_resume_session(self):
        asyncio.run(self.resume_session())

    async def resume_session(self):
        broker = mqttools.Broker('localhost', 0)

        async def broker_wrapper():
            with self.assertRaises(asyncio.CancelledError):
                await broker.serve_forever()

        broker_task = asyncio.create_task(broker_wrapper())

        async def tester():
            address = await broker.getsockname()

            # Try to resume a session that does not exist.
            reader_1, writer_1 = await asyncio.open_connection(*address)
            connect = b'\x10\x10\x00\x04MQTT\x05\x00\x00\x00\x00\x00\x03res'
            writer_1.write(connect)
            connack = await reader_1.readexactly(7)
            self.assertEqual(connack, b'\x20\x05\x00\x00\x02\x24\x00')
            subscribe = b'\x82\x0a\x00\x01\x00\x00\x04/a/b\x00'
            writer_1.write(subscribe)
            suback = await reader_1.readexactly(6)
            self.assertEqual(suback, b'\x90\x04\x00\x01\x00\x00')
            writer_1.close()

            # Resume the session.
            reader_1, writer_1 = await asyncio.open_connection(*address)
            connect = b'\x10\x10\x00\x04MQTT\x05\x00\x00\x00\x00\x00\x03res'
            writer_1.write(connect)
            connack = await reader_1.readexactly(7)
            self.assertEqual(connack, b'\x20\x05\x01\x00\x02\x24\x00')

            # Setup a publisher.
            reader_2, writer_2 = await asyncio.open_connection(*address)
            connect = b'\x10\x10\x00\x04MQTT\x05\x02\x00\x00\x00\x00\x03pub'
            writer_2.write(connect)
            connack = await reader_2.readexactly(7)
            self.assertEqual(connack, b'\x20\x05\x00\x00\x02\x24\x00')

            # Publish /a/b.
            publish = b'\x30\x0a\x00\x04/a/b\x00apa'
            writer_2.write(publish)

            # Receive /a/b in the subscriber.
            publish = await reader_1.readexactly(12)
            self.assertEqual(publish, b'\x30\x0a\x00\x04/a/b\x00apa')

            # Perform a clean start and subscribe to /a/c.
            writer_1.close()
            reader_1, writer_1 = await asyncio.open_connection(*address)
            connect = b'\x10\x10\x00\x04MQTT\x05\x02\x00\x00\x00\x00\x03res'
            writer_1.write(connect)
            connack = await reader_1.readexactly(7)
            self.assertEqual(connack, b'\x20\x05\x00\x00\x02\x24\x00')
            subscribe = b'\x82\x0a\x00\x01\x00\x00\x04/a/c\x00'
            writer_1.write(subscribe)
            suback = await reader_1.readexactly(6)
            self.assertEqual(suback, b'\x90\x04\x00\x01\x00\x00')

            # Publish /a/b and then /a/c.
            publish = b'\x30\x0a\x00\x04/a/b\x00apa'
            writer_2.write(publish)
            publish = b'\x30\x0a\x00\x04/a/c\x00apa'
            writer_2.write(publish)

            # Receive /a/c in the subscriber.
            publish = await reader_1.readexactly(12)
            self.assertEqual(publish, b'\x30\x0a\x00\x04/a/c\x00apa')

            writer_1.close()
            writer_2.close()
            broker_task.cancel()

        await asyncio.wait_for(asyncio.gather(broker_task, tester()), 1)

    def test_ping(self):
        asyncio.run(self.ping())

    async def ping(self):
        broker = mqttools.Broker('localhost', 0)

        async def broker_wrapper():
            with self.assertRaises(asyncio.CancelledError):
                await broker.serve_forever()

        broker_task = asyncio.create_task(broker_wrapper())

        async def tester():
            address = await broker.getsockname()

            # Setup the pinger.
            reader_1, writer_1 = await asyncio.open_connection(*address)
            connect = b'\x10\x10\x00\x04MQTT\x05\x02\x00\x00\x00\x00\x03su1'
            writer_1.write(connect)
            connack = await reader_1.readexactly(7)
            self.assertEqual(connack, b'\x20\x05\x00\x00\x02\x24\x00')
            pingreq = b'\xc0\x00'
            writer_1.write(pingreq)
            pingresp = await reader_1.readexactly(2)
            self.assertEqual(pingresp, b'\xd0\x00')

            writer_1.close()
            broker_task.cancel()

        await asyncio.wait_for(asyncio.gather(broker_task, tester()), 1)


logging.basicConfig(level=logging.DEBUG)


if __name__ == '__main__':
    unittest.main()
