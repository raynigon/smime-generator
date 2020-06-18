from subprocess import call
from ..model import SSLSubject

from os import path

SMIME_CNF_FILE = """
[req]
distinguished_name = req_distinguished_name

[req_distinguished_name]
countryName = Country Name (2 letter code)
countryName_default = DE
countryName_min = 2
countryName_max = 2
stateOrProvinceName = State or Province Name (full name)
stateOrProvinceName_default = State
localityName = Locality Name (eg, city)
0.organizationName = Organization Name (eg, company)
0.organizationName_default = Company
organizationalUnitName = Organizational Unit Name (eg, section)
commonName = Common Name (e.g. server FQDN or YOUR name)
commonName_max = 64
emailAddress = Email Address
emailAddress_max = 40

[smime]
basicConstraints = CA:FALSE
keyUsage = nonRepudiation, digitalSignature, keyEncipherment
subjectKeyIdentifier = hash
authorityKeyIdentifier = keyid,issuer
subjectAltName = email:copy
extendedKeyUsage = emailProtection
"""


class OpenSSL:

    def __init__(self):
        pass

    def generate_rsa_key(self, key_password: str, key_size: int, output_path: str):
        call([
            "openssl",
            "genrsa",
            "-aes256",
            "-passout",
            f"pass:{key_password}",
            "-out", output_path,
            str(key_size)
        ])

    def generate_certificate(self, key_path: str, key_password: str, retention_time: int, subject: SSLSubject, output_path: str):
        call([
            "openssl", 
            "req", 
            "-new", 
            "-x509", 
            "-key", key_path, 
            "-passin", f"pass:{key_password}",
            "-days", str(retention_time), 
            "-out", output_path,
            "-subj", subject.to_openssl_string()
        ])

    def generate_signing_request(self, key_path: str, key_password: str, subject: SSLSubject, output_path: str):
        call([
            "openssl", 
            "req", 
            "-new", 
            "-subj", subject.to_openssl_string(),
            "-key", key_path, 
            "-passin", f"pass:{key_password}",
            "-out", output_path,
        ])

    def sign_smime_request(self, ca_cert_path: str, ca_key_path: str, ca_key_password: str, request_path: str, retention_time: int, output_path: str):
        if not path.exists("smime.cnf"):
            with open("smime.cnf", "w") as file:
                file.write(SMIME_CNF_FILE)
        call([
            "openssl",
            "x509",
            "-req",
            "-days", str(retention_time),
            "-in", request_path,
            "-passin", f"pass:{ca_key_password}",
            "-CA", ca_cert_path,
            "-CAkey", ca_key_path,
            "-set_serial", "1",
            "-out", output_path,
            "-addtrust", "emailProtection",
            "-addreject", "clientAuth",
            "-addreject", "serverAuth",
            "-trustout",
            "-extfile", "smime.cnf",
            "-extensions", "smime"
        ])

    def convert_to_x509_pem(self, input_path: str, output_path: str):
        call([
            "openssl", 
            "x509", 
            "-in", input_path,
            "-out", output_path
        ])

    def convert_to_pkcs12(self, certificate_path: str, key_path: str, key_password: str, pkcs_password: str, output_path: str):
        call([
            "openssl", 
            "pkcs12", 
            "-export", 
            "-passin", f"pass:{key_password}",
            "-passout", f"pass:{pkcs_password}",
            "-in", certificate_path,
            "-inkey", key_path,
            "-out", output_path
        ])
