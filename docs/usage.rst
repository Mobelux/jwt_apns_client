=====
Usage
=====

To use JWT APNs Client in a project::

    from jwt_apns_client.jwt_apns_client import APNSConnection, APNSEnvironments
    client = APNSConnection(
        topic='com.example.application',
        team_id='apns_team_id',
        apns_key_id='apns_key_id',
        apns_key_path='/path/to/apns/key.pem',
        environment=APNSEnvironments.DEV)

    response = client.send_notification(
        device_registration_id='registration_id',
        alert='Example APNS Message',
        badge=1
    )


To create a dummy certificate suitable for use in test cases or which does not interract with the APNs servers::

    1. generate elliptic curve key:
        openssl ecparam -name secp256k1 -genkey -noout -out secp256k1-key.pem
    2. convert to unencrypted pkcs#8 pem
        openssl pkcs8 -topk8 -in secp256k1-key.pem -out key.p8 -nocrypt
