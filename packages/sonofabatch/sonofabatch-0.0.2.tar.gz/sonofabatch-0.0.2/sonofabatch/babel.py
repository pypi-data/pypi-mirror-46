import struct
from faker import Faker


async def read_string_from_reader(reader, max_size_bytes=262144):
    str_size = await read_int_from_reader(reader)
    if str_size <= 0 or str_size > max_size_bytes:
        return None

    str_data = await reader.read(str_size)
    return str_data.decode()


async def write_string_to_writer(writer, string):
    string = string.encode()
    str_len = len(string)
    packed_str_len = struct.pack('i', str_len)
    writer.write(packed_str_len)
    writer.write(string)
    await writer.drain()


async def read_float_from_reader(reader):
    data = await reader.read(4)
    unpacked, = struct.unpack('f', data)
    return unpacked


async def write_float_to_writer(writer, num):
    data = struct.pack('f', float(num))
    writer.write(data)
    await writer.drain()


async def read_bool_from_reader(reader):
    data = await reader.read(1)
    unpacked, = struct.unpack('?', data)
    return unpacked


async def write_bool_to_writer(writer, boolean):
    data = struct.pack('?', boolean)
    writer.write(data)
    await writer.drain()


async def read_int_from_reader(reader):
    data = await reader.read(4)
    unpacked, = struct.unpack('i', data)
    return unpacked


async def write_int_to_writer(writer, num):
    data = struct.pack('i', int(num))
    writer.write(data)
    await writer.drain()


def generate_random_node_name():
    _fake = Faker()
    return _fake.name()
