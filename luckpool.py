#!/usr/bin/env python
from flask_restful import reqparse, abort, Api, Resource
import requests


class Blocks(Resource):
    def get(self):
        try:
            response = requests.get('https://luckpool.net/zen/stats')
            data = response.json()
        except Exception as p:
            return p

        blocks0 = data['poolStats']['pendingBlocks']
        blocks24 = data['poolStats']['blocksLast24']
        blocks48 = data['poolStats']['blocksLast48']

        return {'0': blocks0, '24': blocks24, '48': blocks48}
