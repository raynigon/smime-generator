# SMIME Certificate Generator

Easy SMIME Certificate Handling

## Installation

1. Install Python3.6
2. Install OpenSSL
3. `pip install raynigon-smime-generator`

## Usage

### Generate Config File

```yaml
generation:
    general:
        key:
            size: 4096
        retention: 365 # one years in days
        subject:
            country: "DE"
            state: "north rhine westphalia"
            city: "Bonn"
            organisation: "TKK AG"
            unit: "Dummy Unit"
            name: "TKK AG"
            email: "ca@tkk-ag.de"
    ca:
        filename: "ca"
        key:
            size: 4096
            password: "****"
        subject:
            country: "DE"
            state: "north rhine westphalia"
            city: "Bonn"
            organisation: "TKK AG"
            unit: "Dummy Unit"
            name: "TKK CA"
            email: "ca@tkk-ag.de"
        retention: 3650 # ten years in days
    user:
        - name: "Max Mustermann"
          email: "m.mustermann@tkk-ag.de"
          password: "test123"
        - name: "Lina Musterfrau"
          email: "l.musterfrau@tkk-ag.de"
          password: "test123"
          unit: "Marketing"
```

### Generate CA

`cert_generator.py update-ca`

### Generate User Certificates

`cert_generator.py update-user`

### List all certificates

`cert_generator.py list`

