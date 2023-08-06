from collections import namedtuple

ProbeResult = namedtuple('ProbeResult', ('hop_number', 'reply_hop_number', 'probe_number',
                                         'hop_ip_address', 'rtt_seconds', 'is_last_hop',
                                         'probe'))
SentProbe = namedtuple('SentProbe', ('ttl', 'probe_number', 'sent_time', 'payload', 'key'))
