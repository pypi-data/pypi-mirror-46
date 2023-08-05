import arrow
import google.protobuf.pyext._message
import google.protobuf.timestamp_pb2
import google.protobuf.wrappers_pb2
from interface_meta import override

from ..wrapper import GRPCMessageWrapper


class ProtobufWrapper(GRPCMessageWrapper):

    @override
    def _update_from_pyobj(self, value):
        self._message.value = value

    @override
    def _as_pyobj(self):
        return self._message.value


class ProtobufDoubleWrapper(ProtobufWrapper):

    _MESSAGE_TYPE = google.protobuf.wrappers_pb2.DoubleValue


class ProtobufFloatWrapper(ProtobufWrapper):

    _MESSAGE_TYPE = google.protobuf.wrappers_pb2.FloatValue


class ProtobufInt64Wrapper(ProtobufWrapper):

    _MESSAGE_TYPE = google.protobuf.wrappers_pb2.Int64Value


class ProtobufUInt64Wrapper(ProtobufWrapper):

    _MESSAGE_TYPE = google.protobuf.wrappers_pb2.UInt64Value


class ProtobufInt32Wrapper(ProtobufWrapper):

    _MESSAGE_TYPE = google.protobuf.wrappers_pb2.Int32Value


class ProtobufUInt32Wrapper(ProtobufWrapper):

    _MESSAGE_TYPE = google.protobuf.wrappers_pb2.UInt32Value


class ProtobufBytesWrapper(ProtobufWrapper):

    _MESSAGE_TYPE = google.protobuf.wrappers_pb2.BytesValue


class ProtobufStringWrapper(ProtobufWrapper):

    _MESSAGE_TYPE = google.protobuf.wrappers_pb2.StringValue


class ProtobufBoolWrapper(ProtobufWrapper):

    _MESSAGE_TYPE = google.protobuf.wrappers_pb2.BoolValue


class ProtobufTimestampWrapper(GRPCMessageWrapper):

    _MESSAGE_TYPE = google.protobuf.timestamp_pb2.Timestamp

    @override
    def _update_from_pyobj(self, value):
        self._message.FromDatetime(arrow.get(value))

    @override
    def _as_pyobj(self):
        return self._message.ToDatetime() if self._message.seconds > 0 or self._message.nanos > 0 else None
