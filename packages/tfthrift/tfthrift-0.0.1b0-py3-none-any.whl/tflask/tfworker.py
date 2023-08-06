# -*- coding: utf-8 -*

from .tfroutes import route_map
from .tfflask import tfsession
from pprint import pprint
import json

class RpcParamsException(Exception):
    pass

class Worker(object):
    def __init__(self, logger):
        self.logger = logger
        pass
    
    def get_error(self, error_message="", error_code=40001):
        return {
            "code": error_code,
            "msg": error_message,
        }
    
    def call(self, body):
        self.logger.info("incomming:{}".format(body))
        try:
            resp = self.process(body)
        except RpcParamsException as ex:
            self.logger.error(str(ex))
            resp = self.get_error(str(ex))
        except Exception as ex:
            self.logger.error(str(ex))
            resp = self.get_error(str(ex)) 
        return json.dumps(resp)
            
    
    def process(self, body):
        tfsession.request_data = body
        resp = {}

        try:
            jbody = json.loads(body)
        except json.decoder.JSONDecodeError:
            raise RpcParamsException("参数错误:{}:{}".format(body, "json格式错误"))
        
        jauth = jbody.get('auth')
        if jauth is None:
            raise RpcParamsException("参数错误:{}:{}".format(body, "缺少auth信息"))
        
        jdata = jbody.get('request_data')
        if jdata is None:
            raise RpcParamsException("参数错误:{}:{}".format(body, "缺少request_data信息"))


        path = jdata.get('url')
        params = jdata.get('params')

        if path is None:
            raise RpcParamsException("参数错误:{}:{}".format(body, "缺少path"))
        
        if params is None:
            raise RpcParamsException("参数错误:{}:{}".format(body, "缺少params"))

        pprint(route_map)
        if path in route_map:
            route_map[path](**params)
        else:
            raise RpcParamsException("参数错误:{}:{}".format(body, "path 不存在"))

        return json.dumps(resp)

