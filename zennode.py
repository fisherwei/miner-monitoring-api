#!/usr/bin/env python
from flask_restful import reqparse, abort, Api, Resource
import requests
import os


class NodeDetail(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('nodeid', type=str)

    def get(self, host):
        data = self.parser.parse_args()
        nodeid = data.get('nodeid')
        key = os.environ['ZEN_KEY']

        try:
            response = requests.get('https://securenodes2.na.zensystem.io/api/{nodeid}/detail?key={key}'.format(nodeid=nodeid, key=key))
            return response.text
        except Exception as p:
            return p

