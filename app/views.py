#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import render_template,request
from app import app

REQUIRED = ('requestType', 'studyUID', 'seriesUID', 'objectUID')
OPTIONAL = ('contentType', 'charset', 'anonymize', 'annotation',
            'rows', 'columns', 'region',
            'windowWidth', 'windowCenter', 'frameNumber', 'imageQuality',
            'presentationUID', 'presentationSeriesUID', 'transferSyntax' )
INVALID_DICOM = ('annotation', 'rows', 'columns', 'region',
                 'windowWidth', 'windowCenter')
INVALID_NONDICOM = ('anonymize',)

def err(msg):
    raise Exception, msg

def check_params(kwargs):
    """Validate and sanitize requests"""
    #TODO: implement every check
    valid = REQUIRED + OPTIONAL
    curparams = kwargs.keys()

    #WADO is the only requestType currently accepted by the standard
    assert kwargs['requestType'] == "WADO"

    #checking unknown parameters
    for par in curparams:
        if par not in valid:
            err("Unknown parameter: " + par)

    #checking missing parameters
    for par in REQUIRED:
        if par not in curparams:
            err("Missing parameter:" +par)

    #default content type is image/jpeg
    kwargs['contentType'] = kwargs.get('contentType', 'image/jpeg')

    if kwargs['contentType'] == 'application/dicom':
        for par in INVALID_DICOM:
            if par in curparams:
                err(par + " is not valid if contentType is application/dicom")

        #validation finished
        return

    #checking values for contentType != application/dicom
    for par in INVALID_NONDICOM:
        if par in curparams:
            err(par + " is valid only if contentType is application/dicom")

    if 'annotation' in curparams:
        assert kwargs['annotation'] in ('patient', 'technique')

    if 'windowWidth' in curparams:
        assert 'windowCenter' in curparams
    if 'windowCenter' in curparams:
        assert 'windowWidth' in curparams
    if 'region' in curparams:
        region = kwargs['region'].split(',')
        assert len(region) == 4
        for val in region:
            assert 0.0 <= float(val) <= 1.0




#index page
@app.route('/')
@app.route('/index')
def index():
    kwargs = {rows.split('=')[0]:rows.split('=')[1] for rows in \
              request.query_string.split('&')}
    check_params(kwargs)
    return str(kwargs)
