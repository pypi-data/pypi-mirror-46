import os
import logging
import struct
import enum
from io import BytesIO
import bitstruct


# Connection flags.
CLEAN_START    = 0x02
WILL_FLAG      = 0x04
WILL_QOS_1     = 0x08
WILL_QOS_2     = 0x10
WILL_RETAIN    = 0x20
PASSWORD_FLAG  = 0x40
USER_NAME_FLAG = 0x80


# Control packet types.
class ControlPacketType(enum.IntEnum):
    CONNECT     = 1
    CONNACK     = 2
    PUBLISH     = 3
    PUBACK      = 4
    PUBREC      = 5
    PUBREL      = 6
    PUBCOMP     = 7
    SUBSCRIBE   = 8
    SUBACK      = 9
    UNSUBSCRIBE = 10
    UNSUBACK    = 11
    PINGREQ     = 12
    PINGRESP    = 13
    DISCONNECT  = 14


class ConnectReasonCode(enum.IntEnum):
    SUCCESS                              = 0
    V3_1_1_UNACCEPTABLE_PROTOCOL_VERSION = 1
    V3_1_1_IDENTIFIER_REJECTED           = 2
    V3_1_1_SERVER_UNAVAILABLE            = 3
    V3_1_1_BAD_USER_NAME_OR_PASSWORD     = 4
    V3_1_1_NOT_AUTHORIZED                = 5
    UNSPECIFIED_ERROR                    = 128
    MALFORMED_PACKET                     = 129
    PROTOCOL_ERROR                       = 130
    IMPLEMENTATION_SPECIFIC_ERROR        = 131
    UNSUPPORTED_PROTOCOL_VERSION         = 132
    CLIENT_IDENTIFIER_NOT_VALID          = 133
    BAD_USER_NAME_OR_PASSWORD            = 134
    NOT_AUTHORIZED                       = 135
    SERVER_UNAVAILABLE                   = 136
    SERVER_BUSY                          = 137
    BANNED                               = 138
    BAD_AUTHENTICATION_METHOD            = 140
    TOPIC_NAME_INVALID                   = 144
    PACKET_TOO_LARGE                     = 149
    QUOTA_EXCEEDED                       = 151
    PAYLOAD_FORMAT_INVALID               = 153
    RETAIN_NOT_SUPPORTED                 = 154
    QOS_NOT_SUPPORTED                    = 155
    USE_ANOTHER_SERVER                   = 156
    SERVER_MOVED                         = 157
    CONNECTION_RATE_EXCEEDED             = 159


class DisconnectReasonCode(enum.IntEnum):
    NORMAL_DISCONNECTION                   = 0
    DISCONNECT_WITH_WILL_MESSAGE           = 4
    UNSPECIFIED_ERROR                      = 128
    MALFORMED_PACKET                       = 129
    PROTOCOL_ERROR                         = 130
    IMPLEMENTATION_SPECIFIC_ERROR          = 131
    NOT_AUTHORIZED                         = 135
    SERVER_BUSY                            = 137
    SERVER_SHUTTING_DOWN                   = 139
    KEEP_ALIVE_TIMEOUT                     = 141
    SESSION_TAKEN_OVER                     = 142
    TOPIC_FILTER_INVALID                   = 143
    TOPIC_NAME_INVALID                     = 144
    RECEIVE_MAXIMUM_EXCEEDED               = 147
    TOPIC_ALIAS_INVALID                    = 148
    PACKET_TOO_LARGE                       = 149
    MESSAGE_RATE_TOO_HIGH                  = 150
    QUOTA_EXCEEDED                         = 151
    ADMINISTRATIVE_ACTION                  = 152
    PAYLOAD_FORMAT_INVALID                 = 153
    RETAIN_NOT_SUPPORTED                   = 154
    QOS_NOT_SUPPORTED                      = 155
    USE_ANOTHER_SERVER                     = 156
    SERVER_MOVED                           = 157
    SHARED_SUBSCRIPTIONS_NOT_SUPPORTED     = 158
    CONNECTION_RATE_EXCEEDED               = 159
    MAXIMUM_CONNECT_TIME                   = 160
    SUBSCRIPTION_IDENTIFIERS_NOT_SUPPORTED = 161
    WILDCARD_SUBSCRIPTIONS_NOT_SUPPORTED   = 162


class PubackReasonCode(enum.IntEnum):
    SUCCESS                       = 0
    NO_MATCHING_SUBSCRIBERS       = 16
    UNSPECIFIED_ERROR             = 128
    IMPLEMENTATION_SPECIFIC_ERROR = 131
    NOT_AUTHORIZED                = 135
    TOPIC_NAME_INVALID            = 144
    PACKET_IDENTIFIER_IN_USE      = 145
    QUOTA_EXCEEDED                = 151
    PAYLOAD_FORMAT_INVALID        = 153


class PubrecReasonCode(enum.IntEnum):
    SUCCESS                       = 0
    NO_MATCHING_SUBSCRIBERS       = 16
    UNSPECIFIED_ERROR             = 128
    IMPLEMENTATION_SPECIFIC_ERROR = 131
    NOT_AUTHORIZED                = 135
    TOPIC_NAME_INVALID            = 144
    PACKET_IDENTIFIER_IN_USE      = 145
    QUOTA_EXCEEDED                = 151
    PAYLOAD_FORMAT_INVALID        = 153


class PubrelReasonCode(enum.IntEnum):
    SUCCESS = 0
    PACKET_IDENTIFIER_NOT_FOUND = 146


class PubcompReasonCode(enum.IntEnum):
    SUCCESS = 0
    PACKET_IDENTIFIER_NOT_FOUND = 146


class PropertyIds(enum.IntEnum):
    PAYLOAD_FORMAT_INDICATOR          = 1
    MESSAGE_EXPIRY_INTERVAL           = 2
    CONTENT_TYPE                      = 3
    RESPONSE_TOPIC                    = 8
    CORRELATION_DATA                  = 9
    SUBSCRIPTION_IDENTIFIER           = 11
    SESSION_EXPIRY_INTERVAL           = 17
    ASSIGNED_CLIENT_IDENTIFIER        = 18
    SERVER_KEEP_ALIVE                 = 19
    AUTHENTICATION_METHOD             = 21
    AUTHENTICATION_DATA               = 22
    REQUEST_PROBLEM_INFORMATION       = 23
    WILL_DELAY_INTERVAL               = 24
    REQUEST_RESPONSE_INFORMATION      = 25
    RESPONSE_INFORMATION              = 26
    SERVER_REFERENCE                  = 28
    REASON_STRING                     = 31
    RECEIVE_MAXIMUM                   = 33
    TOPIC_ALIAS_MAXIMUM               = 34
    TOPIC_ALIAS                       = 35
    MAXIMUM_QOS                       = 36
    RETAIN_AVAILABLE                  = 37
    USER_PROPERTY                     = 38
    MAXIMUM_PACKET_SIZE               = 39
    WILDCARD_SUBSCRIPTION_AVAILABLE   = 40
    SUBSCRIPTION_IDENTIFIER_AVAILABLE = 41
    SHARED_SUBSCRIPTION_AVAILABLE     = 42


class QoS(enum.IntEnum):
    """Quality of service levels.

    """

    AT_MOST_ONCE  = 0
    "At most once (QoS 0)."

    AT_LEAST_ONCE = 1
    "At least once (QoS 1)."

    EXACTLY_ONCE  = 2
    "Exactly once (QoS 2)."


# MQTT 5.0
PROTOCOL_VERSION = 5

LOGGER = logging.getLogger(__name__)


class Error(Exception):
    pass


class MalformedPacketError(Error):
    pass


class PayloadReader(BytesIO):

    def read(self, size):
        data = super().read(size)

        if len(data) != size:
            raise MalformedPacketError('Payload too short.')

        return data

    def read_all(self):
        return super().read()

    def is_data_available(self):
        pos = self.tell()
        self.seek(0, os.SEEK_END)
        at_end = (pos < self.tell())
        self.seek(pos)

        return at_end


def control_packet_type_to_string(control_packet_type):
    try:
        name = ControlPacketType(control_packet_type).name
    except ValueError:
        name = 'UNKNOWN'

    return f'{name}({control_packet_type})'


def pack_string(data):
    data = data.encode('utf-8')
    packed = struct.pack('>H', len(data))
    packed += data

    return packed


def unpack_string(payload):
    size = unpack_u16(payload)

    try:
        return payload.read(size).decode('utf-8')
    except UnicodeDecodeError:
        raise MalformedPacketError('String not UTF-8 encoded.')


def pack_u32(value):
    return struct.pack('>I', value)


def unpack_u32(payload):
    return struct.unpack('>I', payload.read(4))[0]


def pack_u16(value):
    return struct.pack('>H', value)


def unpack_u16(payload):
    return struct.unpack('>H', payload.read(2))[0]


def pack_u8(value):
    return struct.pack('B', value)


def unpack_u8(payload):
    return payload.read(1)[0]


def pack_property(property_id, value):
    return struct.pack('B', property_id) + {
        PropertyIds.PAYLOAD_FORMAT_INDICATOR: pack_u8,
        PropertyIds.MESSAGE_EXPIRY_INTERVAL: pack_u32,
        PropertyIds.CONTENT_TYPE: pack_string,
        PropertyIds.RESPONSE_TOPIC: pack_string,
        PropertyIds.CORRELATION_DATA: pack_binary,
        PropertyIds.SUBSCRIPTION_IDENTIFIER: pack_variable_integer,
        PropertyIds.SESSION_EXPIRY_INTERVAL: pack_u32,
        PropertyIds.ASSIGNED_CLIENT_IDENTIFIER: pack_string,
        PropertyIds.SERVER_KEEP_ALIVE: pack_u16,
        PropertyIds.AUTHENTICATION_METHOD: pack_string,
        PropertyIds.AUTHENTICATION_DATA: pack_binary,
        PropertyIds.REQUEST_PROBLEM_INFORMATION: pack_u8,
        PropertyIds.WILL_DELAY_INTERVAL: pack_u32,
        PropertyIds.REQUEST_RESPONSE_INFORMATION: pack_u8,
        PropertyIds.RESPONSE_INFORMATION: pack_string,
        PropertyIds.SERVER_REFERENCE: pack_string,
        PropertyIds.REASON_STRING: pack_string,
        PropertyIds.RECEIVE_MAXIMUM: pack_u16,
        PropertyIds.TOPIC_ALIAS_MAXIMUM: pack_u16,
        PropertyIds.TOPIC_ALIAS: pack_u16,
        PropertyIds.MAXIMUM_QOS: pack_u8,
        PropertyIds.RETAIN_AVAILABLE: pack_u8,
        PropertyIds.USER_PROPERTY: pack_string,
        PropertyIds.MAXIMUM_PACKET_SIZE: pack_u32,
        PropertyIds.WILDCARD_SUBSCRIPTION_AVAILABLE: pack_u8,
        PropertyIds.SUBSCRIPTION_IDENTIFIER_AVAILABLE: pack_u8,
        PropertyIds.SHARED_SUBSCRIPTION_AVAILABLE: pack_u8
    }[property_id](value)


def log_properties(packet_name, properties):
    if LOGGER.isEnabledFor(logging.DEBUG):
        LOGGER.debug('%s properties:', packet_name)

        for identifier, value in properties.items():
            LOGGER.debug('  %s(%d): %s',
                         identifier.name,
                         identifier.value,
                         value)


def pack_properties(packet_name, properties):
    log_properties(packet_name, properties)
    packed = b''

    for property_id, value in properties.items():
        packed += pack_property(property_id, value)

    return pack_variable_integer(len(packed)) + packed


def unpack_property(property_id, payload):
    return {
        PropertyIds.PAYLOAD_FORMAT_INDICATOR: unpack_u8,
        PropertyIds.MESSAGE_EXPIRY_INTERVAL: unpack_u32,
        PropertyIds.CONTENT_TYPE: unpack_string,
        PropertyIds.RESPONSE_TOPIC: unpack_string,
        PropertyIds.CORRELATION_DATA: unpack_binary,
        PropertyIds.SUBSCRIPTION_IDENTIFIER: unpack_variable_integer,
        PropertyIds.SESSION_EXPIRY_INTERVAL: unpack_u32,
        PropertyIds.ASSIGNED_CLIENT_IDENTIFIER: unpack_string,
        PropertyIds.SERVER_KEEP_ALIVE: unpack_u16,
        PropertyIds.AUTHENTICATION_METHOD: unpack_string,
        PropertyIds.AUTHENTICATION_DATA: unpack_binary,
        PropertyIds.REQUEST_PROBLEM_INFORMATION: unpack_u8,
        PropertyIds.WILL_DELAY_INTERVAL: unpack_u32,
        PropertyIds.REQUEST_RESPONSE_INFORMATION: unpack_u8,
        PropertyIds.RESPONSE_INFORMATION: unpack_string,
        PropertyIds.SERVER_REFERENCE: unpack_string,
        PropertyIds.REASON_STRING: unpack_string,
        PropertyIds.RECEIVE_MAXIMUM: unpack_u16,
        PropertyIds.TOPIC_ALIAS_MAXIMUM: unpack_u16,
        PropertyIds.TOPIC_ALIAS: unpack_u16,
        PropertyIds.MAXIMUM_QOS: unpack_u8,
        PropertyIds.RETAIN_AVAILABLE: unpack_u8,
        PropertyIds.USER_PROPERTY: unpack_string,
        PropertyIds.MAXIMUM_PACKET_SIZE: unpack_u32,
        PropertyIds.WILDCARD_SUBSCRIPTION_AVAILABLE: unpack_u8,
        PropertyIds.SUBSCRIPTION_IDENTIFIER_AVAILABLE: unpack_u8,
        PropertyIds.SHARED_SUBSCRIPTION_AVAILABLE: unpack_u8
    }[property_id](payload)


def unpack_properties(packet_name,
                      allowed_property_ids,
                      payload):
    """Return a dictionary of unpacked properties.

    """

    end_pos = unpack_variable_integer(payload)
    end_pos += payload.tell()
    properties = {}

    while payload.tell() < end_pos:
        property_id = payload.read(1)[0]

        if property_id not in allowed_property_ids:
            raise MalformedPacketError(
                f'Invalid property identifier {property_id}.')

        property_id = PropertyIds(property_id)
        properties[property_id] = unpack_property(property_id, payload)

    log_properties(packet_name, properties)

    return properties


def pack_binary(data):
    packed = struct.pack('>H', len(data))
    packed += data

    return packed


def unpack_binary(payload):
    size = unpack_u16(payload)

    return payload.read(size)


def pack_variable_integer(value):
    if value == 0:
        packed = b'\x00'
    else:
        packed = b''

        while value > 0:
            encoded_byte = (value & 0x7f)
            value >>= 7

            if value > 0:
                encoded_byte |= 0x80

            packed += struct.pack('B', encoded_byte)

    return packed


def unpack_variable_integer(payload):
    value = 0
    multiplier = 1
    byte = 0x80

    while (byte & 0x80) == 0x80:
        byte = unpack_u8(payload)
        value += ((byte & 0x7f) * multiplier)
        multiplier <<= 7

    return value


def pack_fixed_header(message_type, flags, size):
    packed = bitstruct.pack('u4u4', message_type, flags)
    packed += pack_variable_integer(size)

    return packed


def unpack_packet_type(payload):
    packet_type = bitstruct.unpack('u4', payload)[0]

    try:
        packet_type = ControlPacketType(packet_type)
    except ValueError:
        pass

    return packet_type


def pack_connect(client_id,
                 clean_start,
                 will_topic,
                 will_message,
                 will_qos,
                 keep_alive_s,
                 properties):
    flags = 0

    if clean_start:
        flags |= CLEAN_START

    payload_length = len(client_id) + 2

    if will_topic and will_message:
        flags |= WILL_FLAG

        if will_qos == 1:
            flags |= WILL_QOS_1
        elif will_qos == 2:
            flags |= WILL_QOS_2

        payload_length += 1
        packed_will_topic = pack_string(will_topic)
        payload_length += len(packed_will_topic)
        payload_length += len(will_message) + 2

    properties = pack_properties('CONNECT', properties)
    packed = pack_fixed_header(ControlPacketType.CONNECT,
                               0,
                               10 + payload_length + len(properties))
    packed += struct.pack('>H', 4)
    packed += b'MQTT'
    packed += struct.pack('>BBH',
                          PROTOCOL_VERSION,
                          flags,
                          keep_alive_s)
    packed += properties
    packed += pack_string(client_id)

    if flags & WILL_FLAG:
        packed += pack_variable_integer(0)
        packed += packed_will_topic
        packed += pack_binary(will_message)

    return packed


def unpack_connect(payload):
    unpack_u16(payload)

    if payload.read(4) != b'MQTT':
        raise MalformedPacketError('Invalid MQTT magic string.')

    if unpack_u8(payload) != PROTOCOL_VERSION:
        raise MalformedPacketError('Wrong protocol version.')

    flags = unpack_u8(payload)
    clean_start = bool(flags & CLEAN_START)
    keep_alive_s = unpack_u16(payload)
    properties = unpack_properties(
        'CONNECT',
        [
            PropertyIds.SESSION_EXPIRY_INTERVAL,
            PropertyIds.AUTHENTICATION_METHOD,
            PropertyIds.AUTHENTICATION_DATA,
            PropertyIds.REQUEST_PROBLEM_INFORMATION,
            PropertyIds.REQUEST_RESPONSE_INFORMATION,
            PropertyIds.RECEIVE_MAXIMUM,
            PropertyIds.TOPIC_ALIAS_MAXIMUM,
            PropertyIds.USER_PROPERTY,
            PropertyIds.MAXIMUM_PACKET_SIZE
        ],
        payload)
    client_id = unpack_string(payload)

    if flags & WILL_FLAG:
        raise MalformedPacketError()

    return client_id, clean_start, keep_alive_s, properties


def pack_connack(session_present,
                 reason,
                 properties):
    properties = pack_properties('CONNACK', properties)
    packed = pack_fixed_header(ControlPacketType.CONNACK,
                               0,
                               2 + len(properties))
    packed += pack_u8(int(session_present))
    packed += pack_u8(reason)
    packed += properties

    return packed


def unpack_connack(payload):
    flags = unpack_u8(payload)
    session_present = bool(flags & 1)
    reason = unpack_u8(payload)

    try:
        reason = ConnectReasonCode(reason)
    except ValueError:
        raise MalformedPacketError(f'Invalid CONNACK reason {reason}')

    properties = unpack_properties(
        'CONNACK',
        [
            PropertyIds.SESSION_EXPIRY_INTERVAL,
            PropertyIds.ASSIGNED_CLIENT_IDENTIFIER,
            PropertyIds.SERVER_KEEP_ALIVE,
            PropertyIds.AUTHENTICATION_METHOD,
            PropertyIds.AUTHENTICATION_DATA,
            PropertyIds.RESPONSE_INFORMATION,
            PropertyIds.SERVER_REFERENCE,
            PropertyIds.REASON_STRING,
            PropertyIds.RECEIVE_MAXIMUM,
            PropertyIds.TOPIC_ALIAS_MAXIMUM,
            PropertyIds.MAXIMUM_QOS,
            PropertyIds.RETAIN_AVAILABLE,
            PropertyIds.USER_PROPERTY,
            PropertyIds.MAXIMUM_PACKET_SIZE,
            PropertyIds.WILDCARD_SUBSCRIPTION_AVAILABLE,
            PropertyIds.SUBSCRIPTION_IDENTIFIER_AVAILABLE,
            PropertyIds.SHARED_SUBSCRIPTION_AVAILABLE
        ],
        payload)

    return session_present, reason, properties


def pack_disconnect(reason):
    packed = pack_fixed_header(ControlPacketType.DISCONNECT, 0, 2)
    packed += struct.pack('B', reason)
    packed += pack_variable_integer(0)

    return packed


def unpack_disconnect(payload):
    if payload.is_data_available():
        reason = payload.read(1)[0]
    else:
        reason = 0

    try:
        reason = DisconnectReasonCode(reason)
    except ValueError:
        pass

    if payload.is_data_available():
        properties = unpack_properties(
            'DISCONNECT',
            [
                PropertyIds.SESSION_EXPIRY_INTERVAL,
                PropertyIds.SERVER_REFERENCE,
                PropertyIds.REASON_STRING,
                PropertyIds.USER_PROPERTY
            ],
            payload)
    else:
        properties = {}

    return reason, properties


def pack_subscribe(topic, packet_identifier):
    packed_topic = pack_string(topic)
    packed = pack_fixed_header(ControlPacketType.SUBSCRIBE,
                               2,
                               len(packed_topic) + 4)
    packed += struct.pack('>HB', packet_identifier, 0)
    packed += packed_topic
    packed += struct.pack('B', 0)

    return packed


def unpack_subscribe(payload):
    packet_identifier = unpack_u16(payload)
    unpack_u8(payload)
    topics = []

    while payload.is_data_available():
        topics.append(unpack_string(payload))
        unpack_u8(payload)

    return topics, packet_identifier


def pack_suback(packet_identifier):
    properties = pack_properties('SUBACK', {})
    packed = pack_fixed_header(ControlPacketType.SUBACK,
                               0,
                               2 + len(properties))
    packed += pack_u16(packet_identifier)
    packed += properties

    return packed


def unpack_suback(payload):
    packet_identifier = unpack_u16(payload)
    properties = unpack_properties('SUBACK',
                                   [
                                       PropertyIds.REASON_STRING,
                                       PropertyIds.USER_PROPERTY
                                   ],
                                   payload)

    return packet_identifier, properties


def pack_unsubscribe(topic, packet_identifier):
    packed_topic = pack_string(topic)
    packed = pack_fixed_header(ControlPacketType.UNSUBSCRIBE,
                               2,
                               len(packed_topic) + 3)
    packed += struct.pack('>HB', packet_identifier, 0)
    packed += packed_topic

    return packed


def unpack_unsubscribe(payload):
    packet_identifier = unpack_u16(payload)
    unpack_u8(payload)
    topic = unpack_string(payload)

    return packet_identifier, topic


def pack_unsuback(packet_identifier):
    packed = pack_fixed_header(ControlPacketType.UNSUBACK, 0, 3)
    packed += pack_u16(packet_identifier)
    packed += pack_properties('UNSUBACK', {})

    return packed


def unpack_unsuback(payload):
    packet_identifier = unpack_u16(payload)
    properties = unpack_properties('UNSUBACK',
                                   [
                                       PropertyIds.REASON_STRING,
                                       PropertyIds.USER_PROPERTY
                                   ],
                                   payload)

    return packet_identifier, properties


def pack_publish(topic, message, alias):
    if alias is None:
        properties = b'\x00'
    else:
        properties = pack_properties('PUBLISH',
                                     {PropertyIds.TOPIC_ALIAS: alias})

    packed_topic = pack_string(topic)
    size = len(packed_topic) + len(message) + len(properties)
    packed = pack_fixed_header(ControlPacketType.PUBLISH, 0, size)
    packed += packed_topic
    packed += properties
    packed += message

    return packed


def unpack_publish(payload, qos):
    topic = unpack_string(payload)

    if qos > 0:
        raise MalformedPacketError('Only QoS 0 is supported.')

    properties = unpack_properties(
        'PUBLISH',
        [
            PropertyIds.PAYLOAD_FORMAT_INDICATOR,
            PropertyIds.MESSAGE_EXPIRY_INTERVAL,
            PropertyIds.CONTENT_TYPE,
            PropertyIds.RESPONSE_TOPIC,
            PropertyIds.CORRELATION_DATA,
            PropertyIds.SUBSCRIPTION_IDENTIFIER,
            PropertyIds.TOPIC_ALIAS,
            PropertyIds.USER_PROPERTY
        ],
        payload)

    message = payload.read_all()

    return topic, message, properties


def pack_pingreq():
    return pack_fixed_header(ControlPacketType.PINGREQ, 0, 0)


def pack_pingresp():
    return pack_fixed_header(ControlPacketType.PINGRESP, 0, 0)
