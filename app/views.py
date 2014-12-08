#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import render_template,request
from app import app

#index page
@app.route('/')
@app.route('/index')
def index():
           return "Hello World"
