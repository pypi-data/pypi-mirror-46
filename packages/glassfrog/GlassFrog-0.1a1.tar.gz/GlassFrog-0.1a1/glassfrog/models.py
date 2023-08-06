from datetime import datetime

from glassfrog import exceptions
from glassfrog.client import GlassFrogClient


class BaseModel:
    _RESOURCE_NAME = None

    def __init__(self, data):
        self._data = data

    @property
    def id(self):
        return self._get('id')

    def _get(self, value):
        try:
            return self._data[value]
        except KeyError:
            pass

    @classmethod
    def get(cls, id):
        data = GlassFrogClient.get(resource=cls._RESOURCE_NAME, id=id)
        return cls(data=data[cls._RESOURCE_NAME])

    @classmethod
    def list(cls):
        data = GlassFrogClient.get(resource=cls._RESOURCE_NAME, id=id)
        for item in data[cls._RESOURCE_NAME]:
            yield cls(data=item)

    def _detail(self, resource_class):
        data = GlassFrogClient.get(
            resource=resource_class._RESOURCE_NAME,
            id=self.id,
            from_resource=self._RESOURCE_NAME,
        )
        for item in data[resource_class._RESOURCE_NAME]:
            yield resource_class(data=item)


class UnsupportedModelMixin:
    @classmethod
    def get(cls, id):
        return cls(data={'id': id})

    @classmethod
    def list(cls):
        raise exceptions.UnsupportedModelException()

    def _detail(self, resource_class):
        raise exceptions.UnsupportedModelException()


class Circle(BaseModel):
    _RESOURCE_NAME = 'circles'

    @property
    def name(self):
        return self._get('name')

    @property
    def short_name(self):
        return self._get('short_name')

    @property
    def strategy(self):
        return self._get('strategy')

    @property
    def organization(self):
        organization_id = self._get('organization_id')
        return Organization.get(id=organization_id)

    @property
    def roles(self):
        links = self._get('links')
        for role_id in links['roles']:
            yield Role.get(id=role_id)

    @property
    def policies(self):
        links = self._get('links')
        for policy_id in links['policies']:
            yield Policy.get(id=policy_id)

    @property
    def domains(self):
        links = self._get('links')
        for domain_id in links['domains']:
            yield Domain.get(id=domain_id)

    @property
    def supported_role(self):
        links = self._get('links')
        role_id = links['supported_role']
        return Role.get(id=role_id)


class Person(BaseModel):
    _RESOURCE_NAME = 'people'

    @property
    def name(self):
        return self._get('name')

    @property
    def email(self):
        return self._get('email')


class Organization(UnsupportedModelMixin, BaseModel):
    pass


class Domain(UnsupportedModelMixin, BaseModel):
    pass


class Policy(UnsupportedModelMixin, BaseModel):
    pass


class Role(BaseModel):
    _RESOURCE_NAME = 'roles'

    @property
    def is_core(self):
        return self._get('is_core')

    @property
    def purpose(self):
        return self._get('purpose')

    @property
    def circle(self):
        links = self._get('links')
        circle_id = links['circle']
        return Circle.get(id=circle_id)

    @property
    def supported_role(self):
        links = self._get('links')
        role_id = links['supported_role']
        return Role.get(id=role_id)

    @property
    def domains(self):
        links = self._get('links')
        for domain_id in links['domains']:
            yield Domain.get(id=domain_id)

    @property
    def accountabilities(self):
        links = self._get('links')
        for accountability_id in links['accountabilities']:
            yield Accountability.get(id=accountability_id)

    @property
    def people(self):
        links = self._get('links')
        for person_id in links['people']:
            yield Person.get(id=person_id)

    @property
    def organization(self):
        organization_id = self._get('organization_id')
        return Organization.get(id=organization_id)
    
    @property
    def elected_until(self):
        try:
            date_str = self._get('elected_until')
            return datetime.strptime(date_str, '%Y-%M-%d').date()
        except:
            return None


class Accountability(UnsupportedModelMixin, BaseModel):
    pass


class Project(UnsupportedModelMixin, BaseModel):
    pass
