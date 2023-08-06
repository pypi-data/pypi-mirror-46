import os

import requests

from glassfrog import exceptions


class GlassFrogClient:
    _URL = 'https://api.glassfrog.com'
    _TOKEN = os.environ.get('GLASSFROG_API_TOKEN')

    @classmethod
    def get(cls, resource, id=None, from_resource=None):
        if from_resource:
            if not id:
                raise Exception()
            url = f'{cls._URL}/{from_resource}/{id}/{resource}'
        elif id:
            url = f'{cls._URL}/{resource}/{id}'
        else:
            url = f'{cls._URL}/{resource}'

        if not cls._TOKEN:
            raise exceptions.TokenUndefinedException()

        response = requests.get(
            url=url,
            headers={
                "X-Auth-Token": cls._TOKEN,
                "Content-Type": "application/json",
            }
        )
        response.raise_for_status()
        return response.json()
