# Original author: 
from OpenSSL import crypto, SSL

from time import gmtime, mktime

import socket
import os
import datetime
import collections


Subject = collections.namedtuple('Subject', (
    'country',
    'state',
    'organization',
    'organization_unit',
    'common_name',
))


def self_signed_cert(cert_name, key_name, expiry_timedelta = datetime.timedelta(days = 30 * 18), key_size = 2048, subject_data = None):
    if not os.path.exists(cert_name) or not os.path.exists(key_name):
        # create a key pair
        k = crypto.PKey()
        k.generate_key(crypto.TYPE_RSA, key_size)

        # create a self-signed cert
        if subject_data is None:
            my_hostname = socket.gethostname()

            subject_data = Subject(
                country = '  ',
                state = 'Unknown',
                organization = 'Unknown',
                organization_unit = 'Unknown',
                common_name = my_hostname
            )

        cert = crypto.X509()
        cert.get_subject().C = subject_data.country
        cert.get_subject().ST = subject_data.state
        cert.get_subject().O = subject_data.organization
        cert.get_subject().OU = subject_data.organization_unit
        cert.get_subject().CN = subject_data.common_name
        cert.set_serial_number(1000)
        cert.gmtime_adj_notBefore(0)
        cert.gmtime_adj_notAfter(expiry_timedelta.seconds)
        cert.set_issuer(cert.get_subject())
        cert.set_pubkey(k)
        cert.sign(k, 'sha512')
        
        # save cert, then save key
        with open(cert_name, "wb") as fp1:
            fp1.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))

        with open(key_name, "wb") as fp2:
            fp2.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k))