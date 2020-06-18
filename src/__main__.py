from service import AppConfig, CertificateGenerator

import argparse

parser = argparse.ArgumentParser(description='Manages SMIME Certificates')
parser.add_argument("mode", choices=["update-ca", "update-user", "list"])
args = parser.parse_args()

config = AppConfig()
generator = CertificateGenerator(config)

if args.mode == "update-ca":
    generator.generate_ca()
elif args.mode == "update-user":
    generator.generate_certs()
elif args.mode == "list":
    generator.list_certs()
