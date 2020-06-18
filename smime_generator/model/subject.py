from typing import Dict

class SSLSubject:

    def __init__(self, country: str, state: str, city: str, organisation: str, name: str, email: str, organisation_unit: str = None):
        self.country = country
        self.state = state
        self.city = city
        self.organisation = organisation
        self.organisation_unit = organisation_unit
        self.name = name
        self.email = email

    def copy_with_dict(self, data: Dict[str, str]):
        country = self.country
        if "country" in data.keys():
            country = data["country"]

        state = self.state
        if "state" in data.keys():
            state = data["state"]

        city = self.city
        if "city" in data.keys():
            city = data["city"]

        organisation = self.organisation
        if "organisation" in data.keys():
            organisation = data["organisation"]

        name = self.name
        if "name" in data.keys():
            name = data["name"]

        email = self.email
        if "email" in data.keys():
            email = data["email"]

        organisation_unit = self.organisation_unit
        if "unit" in data.keys():
            organisation_unit = data["unit"]

        return SSLSubject(country, state, city, organisation, name, email, organisation_unit=organisation_unit)

    def to_openssl_string(self)->str:
        subject = f"/C={self.country}"
        subject += f"/ST={self.state}"
        subject += f"/L={self.city}"
        subject += f"/O={self.organisation}"
        if self.organisation_unit is not None:
            subject += f"/OU={self.organisation_unit}"
        subject += f"/CN={self.name}"
        subject += f"/emailAddress={self.email}"
        return subject

def of_dict(data: Dict[str, str])->SSLSubject:
    return SSLSubject(data["country"], data["state"], data["city"], data["organisation"], data["name"], data["email"], organisation_unit=data.get("unit"))

