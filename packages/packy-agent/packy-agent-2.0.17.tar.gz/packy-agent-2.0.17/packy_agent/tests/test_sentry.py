import logging

import sentry_sdk


logger = logging.getLogger(__name__)


def test_message_is_sent_to_sentry_when_message_is_sent_explicitly(sentry_server_mock):
    events = sentry_server_mock
    events.clear()
    sentry_sdk.capture_message('Test message')
    assert len(events) == 1
    first_event = events[0]
    assert first_event['message'] == 'Test message'


def test_message_is_sent_to_sentry_when_error_is_logged(sentry_server_mock):
    events = sentry_server_mock
    events.clear()
    logger.error('Test error')
    assert len(events) == 1
    first_event = events[0]
    assert first_event['logentry']['message'] == 'Test error'
