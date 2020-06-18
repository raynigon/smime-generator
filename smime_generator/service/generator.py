from .config import AppConfig, UserConfig
from .openssl import OpenSSL
from os import path, makedirs, walk
from cryptography import x509
from cryptography.hazmat.backends import default_backend

import base64
import datetime


class CertificateGenerator():

    def __init__(self, config: AppConfig):
        self.__config = config
        self.__open_ssl = OpenSSL()

    def generate_ca(self):
        ca_config = self.__config.ca
        ca_key_file_name = f"{ca_config.filename}.key"
        ca_cert_file_name = f"{ca_config.filename}.crt"
        if not path.exists(ca_key_file_name):
            self.__open_ssl.generate_rsa_key(
                ca_config.key.password, ca_config.key_size, ca_key_file_name)
        if not path.exists(ca_cert_file_name):
            self.__open_ssl.generate_certificate(
                ca_key_file_name, ca_config.key.password, ca_config.retention, ca_config.subject, ca_cert_file_name)

    def generate_certs(self):
        ca_config = self.__config.ca
        ca_key_file_name = f"{ca_config.filename}.key"
        ca_cert_file_name = f"{ca_config.filename}.crt"
        if not path.exists(ca_key_file_name) or not path.exists(ca_cert_file_name):
            raise Exception("Unable to generate User certificates without a Certificate Authority")
        for user in self.__config.user:
            self.__create_user_keypair(user)

    def list_certs(self):
        certs = self.__find_certs()
        row_format = "{:70} | {:35}"
        print(row_format.format("Certificate", "Invalid after"))
        print("-" * 108)
        for row in certs:
            diff = (row[1] - datetime.datetime.now()).total_seconds()
            marker = ""
            if diff < 2592000: # 30 days
                marker = " < soon invalid"
            items = [row[0], str(row[1])+marker]
            print(row_format.format(*items))

    def __find_certs(self):
        certs = []
        for parent, _, files in walk("."):
            for filename in files:
                if not filename.endswith(".crt") and not filename.endswith(".pem"):
                    continue
                file_path = path.join(parent, filename)
                with open(file_path, "rb") as fp:
                    data = fp.read()
                try:
                    cert = x509.load_pem_x509_certificate(
                        data, default_backend())
                    certs.append([file_path, cert.not_valid_after])
                except:
                    pass
        return certs

    def __create_user_keypair(self, user: UserConfig):
        folder = user.email.replace(".", "_").replace("@", "_at_")
        if path.exists(folder):
            return
        makedirs(folder)
        # Generate Key
        self.__open_ssl.generate_rsa_key(
            user.password, self.__config.general.key_size, f"{folder}/private.key")
        # Generate Signing Request
        self.__open_ssl.generate_signing_request(
            f"{folder}/private.key", user.password, user.subject, f"{folder}/cert_sign_req.csr")
        # Sign Certificate
        ca_config = self.__config.ca
        ca_key_file_name = f"{ca_config.filename}.key"
        ca_cert_file_name = f"{ca_config.filename}.crt"
        self.__open_ssl.sign_smime_request(
            ca_cert_file_name,
            ca_key_file_name,
            ca_config.key.password,
            f"{folder}/cert_sign_req.csr",
            self.__config.general.retention,
            f"{folder}/certificate.crt"
        )
        # Convert Result
        self.__open_ssl.convert_to_x509_pem(
            f"{folder}/certificate.crt", f"{folder}/{folder}.pem")
        self.__open_ssl.convert_to_pkcs12(
            f"{folder}/certificate.crt", f"{folder}/private.key", user.password, user.password, f"{folder}/{folder}.p12")
