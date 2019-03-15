#!/usr/bin/env python
from flask_restful import reqparse, abort, Api, Resource
from requests.auth import HTTPDigestAuth
import requests
import urllib.parse

port = 80
username = 'root'
password = 'root'


def get_value(data, item):
    keys = item.split('.')
    if len(keys) == 2:
        return data[keys[0]][keys[1]]
    elif len(keys) == 3:
        return data[keys[0]][int(keys[1])][keys[2]]
    elif len(keys) == 4:
        values = {}
        for i in data[keys[0]][int(keys[1])][keys[2]].split(','):
            j = i.split('=')
            if len(j) != 2:
                continue
            if j[1][-1:] == '|':
                j[1] = j[1][:-1]
            values[j[0]] = j[1]
        return values[keys[3]]
    else:
        return 'error'


class Status(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('item', type=str)

    def get(self, host):
        data = self.parser.parse_args()
        item = data.get('item')

        try:
            # requests_cache.install_cache('zabbix_cache', backend='redis', expire_after=30)
            response = requests.get('http://{host}:{port}/cgi-bin/get_miner_status.cgi'.format(host=host, port=port),
                                    auth=HTTPDigestAuth(username, password))
            data = response.json()
        except Exception as p:
            return p

        return get_value(data, item)


class AsicStatus(Resource):
    def get(self, host):
        try:
            response = requests.get('http://{host}:{port}/cgi-bin/get_miner_status.cgi'.format(host=host, port=port),
                                    auth=HTTPDigestAuth(username, password))
            data = response.json()
        except Exception as p:
            return p

        asic = ''
        asic += get_value(data, 'devs.0.freq.chain_acs1')
        asic += get_value(data, 'devs.0.freq.chain_acs2')
        asic += get_value(data, 'devs.0.freq.chain_acs3')

        return asic.strip()


class Conf(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('item', type=str)

    def get(self, host):
        data = self.parser.parse_args()
        item = data.get('item')

        try:
            # requests_cache.install_cache('zabbix_cache', backend='redis', expire_after=30)
            response = requests.get('http://{host}:{port}/cgi-bin/get_miner_conf.cgi'.format(host=host, port=port),
                                    auth=HTTPDigestAuth(username, password))
            data = response.json()
        except Exception as p:
            return p

        return get_value(data, item)


class Restart(Resource):
    def __init__(self):
        pass

    def get(self, host):
        try:
            response = requests.get('http://{host}:{port}/cgi-bin/kill_cgminer.cgi'.format(host=host, port=port),
                                    auth=HTTPDigestAuth(username, password))
            data = response.text
        except Exception as p:
            return 0

        return data


class Fan(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('fanpwm', type=str)

    def get(self, host):
        data = self.parser.parse_args()
        fanpwm = data.get('fanpwm')

        try:
            response = requests.get('http://{host}:{port}/cgi-bin/get_miner_conf.cgi'.format(host=host, port=port),
                                    auth=HTTPDigestAuth(username, password))
            data = response.json()
        except Exception as p:
            return 10

        d = ''
        d += urllib.parse.urlencode({'_ant_pool1url': data['pools'][0]['url']}) + '&'
        d += urllib.parse.urlencode({'_ant_pool1user': data['pools'][0]['user']}) + '&'
        d += urllib.parse.urlencode({'_ant_pool1pw': data['pools'][0]['pass']}) + '&'
        d += urllib.parse.urlencode({'_ant_pool2url': data['pools'][1]['url']}) + '&'
        d += urllib.parse.urlencode({'_ant_pool2user': data['pools'][1]['user']}) + '&'
        d += urllib.parse.urlencode({'_ant_pool2pw': data['pools'][1]['pass']}) + '&'
        d += urllib.parse.urlencode({'_ant_pool3url': data['pools'][2]['url']}) + '&'
        d += urllib.parse.urlencode({'_ant_pool3user': data['pools'][2]['user']}) + '&'
        d += urllib.parse.urlencode({'_ant_pool3pw': data['pools'][2]['pass']}) + '&'
        d += urllib.parse.urlencode({'_ant_nobeeper': 'false'}) + '&'
        d += urllib.parse.urlencode({'_ant_notempoverctrl': 'false'}) + '&'
        d += urllib.parse.urlencode({'_ant_fan_customize_switch': 'true'}) + '&'
        d += urllib.parse.urlencode({'_ant_fan_customize_value': fanpwm}) + '&'
        d += urllib.parse.urlencode({'_ant_freq': data['bitmain-freq']})

        try:
            response = requests.post('http://{host}:{port}/cgi-bin/set_miner_conf.cgi'.format(host=host, port=port),
                                     auth=HTTPDigestAuth(username, password), data=d)
            return response.status_code
        except Exception as p:
            return 20


class Pool(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('p1', type=str)
        self.parser.add_argument('p1u', type=str)
        self.parser.add_argument('p2', type=str)
        self.parser.add_argument('p2u', type=str)
        self.parser.add_argument('p3', type=str)
        self.parser.add_argument('p3u', type=str)

    def get(self, host):
        data = self.parser.parse_args()
        p1 = data.get('p1')
        print(host.split('.'))
        p1u = data.get('p1u') + '.' + host.split('.')[-1]
        p2 = data.get('p2')
        p2u = data.get('p2u') + '.' + host.split('.')[-1]
        p3 = data.get('p3')
        p3u = data.get('p3u') + '.' + host.split('.')[-1]

        try:
            response = requests.get('http://{host}:{port}/cgi-bin/get_miner_conf.cgi'.format(host=host, port=port),
                                    auth=HTTPDigestAuth(username, password))
            data = response.json()
        except Exception as p:
            return 10

        d = ''
        d += urllib.parse.urlencode({'_ant_pool1url': p1}) + '&'
        d += urllib.parse.urlencode({'_ant_pool1user': p1u}) + '&'
        d += urllib.parse.urlencode({'_ant_pool1pw': data['pools'][0]['pass']}) + '&'
        d += urllib.parse.urlencode({'_ant_pool2url': p2}) + '&'
        d += urllib.parse.urlencode({'_ant_pool2user': p2u}) + '&'
        d += urllib.parse.urlencode({'_ant_pool2pw': data['pools'][1]['pass']}) + '&'
        d += urllib.parse.urlencode({'_ant_pool3url': p3}) + '&'
        d += urllib.parse.urlencode({'_ant_pool3user': p3u}) + '&'
        d += urllib.parse.urlencode({'_ant_pool3pw': data['pools'][2]['pass']}) + '&'
        d += urllib.parse.urlencode({'_ant_nobeeper': 'false'}) + '&'
        d += urllib.parse.urlencode({'_ant_notempoverctrl': 'false'}) + '&'
        d += urllib.parse.urlencode({'_ant_fan_customize_switch': 'false'}) + '&'
        d += urllib.parse.urlencode({'_ant_fan_customize_value': ''}) + '&'
        d += urllib.parse.urlencode({'_ant_freq': data['bitmain-freq']})

        try:
            response = requests.post('http://{host}:{port}/cgi-bin/set_miner_conf.cgi'.format(host=host, port=port),
                                     auth=HTTPDigestAuth(username, password), data=d)
            return response.status_code
        except Exception as p:
            return 20

