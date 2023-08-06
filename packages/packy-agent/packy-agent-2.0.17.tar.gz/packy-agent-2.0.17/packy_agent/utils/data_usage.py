import psutil


def get_network_usage():
    snetio = psutil.net_io_counters(pernic=True, nowrap=True)
    snetio.pop('lo', None)

    bytes_sent = bytes_received = 0
    for value in snetio.values():
        bytes_sent += value.bytes_sent
        bytes_received += value.bytes_recv

    return bytes_sent, bytes_received
