import json

import pytest
import requests


def pytest_addoption(parser):
    group = parser.getgroup('slack')
    group.addoption(
        '--slack_channel',
        action='store',
        dest='slack_channel',
        default=None,
        help='Set the channel name to report'
    )
    group.addoption(
        '--slack_hook',
        action='store',
        dest='slack_hook',
        default=None,
        help='Used for reporting to slack'
    )

    group.addoption(
        '--slack_report_link',
        action='store',
        dest='slack_report_link',
        default=None,
        help='Set the report link'
    )

    group.addoption(
        '--slack_username',
        action='store',
        dest='slack_username',
        default=None,
        help='Set the reporter name'
    )

    group.addoption(
        '--slack_timeout',
        action='store',
        dest='slack_timeout',
        default=10,
        help='Set the report send timeout'
    )

    group.addoption(
        '--slack_success_icon',
        action='store',
        dest='slack_success_icon',
        default=':thumbsup:',
        help='Set icon for a successful run'
    )

    group.addoption(
        '--slack_failed_icon',
        action='store',
        dest='slack_failed_icon',
        default=':thumbsdown:',
        help='Set icon for a failed run'
    )


@pytest.hookimpl(hookwrapper=True)
def pytest_terminal_summary(terminalreporter, exitstatus, config):
    yield

    if not config.option.slack_hook or not config.option.slack_channel:
        return
    timeout = config.option.slack_timeout
    failed = len(terminalreporter.stats.get('failed', []))
    passed = len(terminalreporter.stats.get('passed', []))
    skipped = len(terminalreporter.stats.get('skipped', []))
    error = len(terminalreporter.stats.get('error', []))

    report_link = config.option.slack_report_link
    slack_hook = config.option.slack_hook
    channel = config.option.slack_channel

    slack_username = config.option.slack_username if config.option.slack_username else 'Regression testing results'

    if int(exitstatus) == 0:
        color = "#56a64f"
        emoji = config.option.slack_success_icon
    else:
        color = '#ff0000'
        emoji = config.option.slack_failed_icon

    final_results = 'Passed=%s Failed=%s Skipped=%s Error=%s' % (passed, failed, skipped, error)
    if report_link:
        final_results = '<%s|%s>' % (report_link, final_results)

    results_pattern = {
        "color": color,
        "text": final_results,
        "mrkdwn_in": [
            "text",
            "pretext"
        ]
    }

    payload = {"channel": channel,
               "username": slack_username,
               "attachments": [results_pattern],
               "icon_emoji": emoji}

    requests.post(slack_hook, data=json.dumps(payload), timeout=timeout)
