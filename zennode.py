#!/usr/bin/env python
from flask_restful import reqparse, abort, Api, Resource
import requests


class API(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('key', type=str)

    def get(self, host):
        data = self.parser.parse_args()
        key = data.get('key')

        try:
            response = requests.get('https://securenodes2.na.zensystem.io{api}?key={key}'.format(api=api, key=key))
            return response.text
        except Exception as p:
            return p

