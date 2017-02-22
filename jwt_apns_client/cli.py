# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import, print_function, division

import click

from jwt_apns_client.jwt_apns_client import APNSConnection, APNSEnvironments

click.disable_unicode_literals_warning = True


@click.command()
def main(args=None):
    """Console script for jwt_apns_client"""
    click.echo("Replace this message by putting your code into "
               "jwt_apns_client.cli.main")
    click.echo("See click documentation at http://click.pocoo.org/")


@click.command()
@click.option('--message', default="testing!", help='A message to send in an alert')
@click.option('--device', help='A device registration id')
@click.option('--environment', default=APNSEnvironments.DEV, help='Development or production environment')
@click.option('--key_path', help='Path to the .p8 file')
@click.option('--key_id', help='APNs Key Id')
@click.option('--team_id', help='APNs Team Id')
@click.option('--topic', help='APNs Topic')
def send(message, device, environment, key_path, key_id, team_id, topic, *args, **kwargs):
    conn = APNSConnection(environment=environment, apns_key_path=key_path, team_id=team_id,
                          apns_key_id=key_id, topic=topic)

    notification_response = conn.send_notification(device_registration_id=device, alert=message)
    print('Status: ', notification_response.status)
    if notification_response.reason:
        print('Reason: ', notification_response.reason)
    # print(notification_response.__dict__)


if __name__ == "__main__":
    send()
