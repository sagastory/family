#!/usr/bin/env Python
# coding=utf-8

from url import url

import tornado.web
import os

settings = dict(
    template_path = os.path.join(os.path.dirname(__file__), "templates"),
    static_path = os.path.join(os.path.dirname(__file__), "statics"),
    cookie_secret="61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
    login_url="/login",
    autoreload=True,
    debug=True,
    dbhost='127.0.0.1',
    dbpasswd='jbgsn',
    dbuser='root',
    dbname='family'
    )

application = tornado.web.Application(
    handlers = url,
    **settings
    )