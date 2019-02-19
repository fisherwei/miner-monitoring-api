from flask import Flask
from flask_restful import Api
import luckpool
import antminer
import zennode
import requests_cache

requests_cache.install_cache('zabbix_cache', backend='memory', expire_after=60)

app = Flask(__name__)
api = Api(app)

api.add_resource(luckpool.Blocks, '/luckpool_blocks')
api.add_resource(antminer.Status, '/antminer/status/<host>')
api.add_resource(antminer.AsicStatus, '/antminer/asic_status/<host>')
api.add_resource(antminer.Conf, '/antminer/conf/<host>')
api.add_resource(antminer.Restart, '/antminer/restart/<host>')
api.add_resource(antminer.Fan, '/antminer/fan/<host>')
api.add_resource(zennode.API, '/zennode/api/<api>')

if __name__ == '__main__':
    app.run(debug=True)
