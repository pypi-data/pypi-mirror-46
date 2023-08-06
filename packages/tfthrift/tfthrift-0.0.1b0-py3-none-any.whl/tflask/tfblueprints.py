# -*- coding: utf-8 -*

from flask import Blueprint
from .tfroutes import route_map

class TBluePrint(Blueprint):

    def __init__(self, name, import_name, static_folder=None,
                 static_url_path=None, template_folder=None,
                 url_prefix=None, subdomain=None, url_defaults=None,
                 root_path=None):
                 super().__init__(name, import_name, static_folder, static_url_path,
                 template_folder, url_prefix, subdomain, url_defaults, root_path)
                 

    def add_url_rule(self, rule, endpoint=None, view_func=None, **options):
        super().add_url_rule(rule, endpoint, view_func, **options)
        route_map['/'] = view_func


