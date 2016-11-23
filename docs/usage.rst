=====
Usage
=====

To use JWT APNs Client in a project::

    import jwt_apns_client


To create a dummy certificate suitable for use in test cases or could which does not interract with the APNs servers::

    1. generate elliptic curve key:
        openssl ecparam -name secp256k1 -genkey -noout -out secp256k1-key.pem
    2. convert to unencrypted pkcs#8 pem
        openssl pkcs8 -topk8 -in secp256k1-key.pem -out key.p8 -nocrypt
