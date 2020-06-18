import yaml
from typing import List

from ..model import SSLSubject
from ..model.subject import of_dict as subject_of_dict

class GeneralConfig:

    def __init__(self, key_size, subject: SSLSubject, retention: int):
        self.key_size = key_size
        self.subject = subject
        self.retention = retention

class CAKey:

    def __init__(self, password):
        self.password = password

class CAConfig:

    def __init__(self, filename, key_size, key_password, subject: SSLSubject, retention: int):
        self.filename = filename
        self.key_size = key_size
        self.key = CAKey(key_password)
        self.subject = subject
        self.retention = retention

class UserConfig:

    def __init__(self, subject, password):
        self.subject = subject
        self.password = password

    @property
    def email(self):
        return self.subject.email

    @property
    def name(self):
        return self.subject.name

class AppConfig:

    def __init__(self, path="config.yml"):
        with open(path) as file:
            self.__data = yaml.safe_load(file)
    
    @property
    def general(self)->GeneralConfig:
        base_section = self.__data["generation"]["general"]
        subject = subject_of_dict(base_section["subject"])
        return GeneralConfig(base_section["key"]["size"], subject, base_section["retention"])

    @property
    def ca(self)->CAConfig:
        base_ca = self.__data["generation"]["ca"]
        key_size = self.general.key_size
        if "size" in base_ca["key"].keys():
            key_size = base_ca["key"]["size"]
        subject = self.general.subject.copy_with_dict(base_ca["subject"])
        return CAConfig(base_ca["filename"], key_size, base_ca["key"]["password"], subject, base_ca["retention"])

    @property
    def user(self)->List[UserConfig]:
        base_section = self.__data["generation"]["user"]
        user = []
        for item in base_section:
            subject = self.general.subject.copy_with_dict(item)
            password = item["password"]
            user.append(UserConfig(subject, password))
        return user