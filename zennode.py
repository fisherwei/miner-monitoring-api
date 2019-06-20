#!/usr/bin/env python
from flask_restful import reqparse, abort, Api, Resource
import requests
import os


class API(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('api', type=str)

    def get(self, host):
        data = self.parser.parse_args()
        api = data.get('api')
        key = os.environ['ZEN_KEY']

        try:
            response = requests.get('https://securenodes2.na.zensystem.io{api}?key={key}'.format(api=api, key=key))
            return response.text
        except Exception as p:
            return p

