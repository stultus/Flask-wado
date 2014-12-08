#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim: sw=4:expandtab
#
# copyright 2014 Hrishikesh K B <hrishi.kb@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.



from flask import render_template,request
from app import app
import accessdata

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
    if kwargs['contentType'] == "application/dicom":
        format = "dicom"
    else:
        #image/png -> png, image/jpeg -> jpeg
        format = kwargs['contentType'].replace('image/','')

    #getting DICOM image from accessdata
    image = accessdata.get(studyUID = kwargs['studyUID'],
                           seriesUID = kwargs['seriesUID'],
                           objectUID = kwargs['objectUID'],
                           format=format)
    if kwargs['contentType'] == "application/dicom":
        return image.raw()
    if 'windowWidth' in kwargs:
        image.brightness(kwargs['windowWidth'])

    if 'windowCenter' in kwargs:
        left, upper, right, lower = [float(val) for val in kwargs['region'].split(",")]
        #coordinates normalization
        width, height = image.img.size
        #1 : width = left : x
        image.crop(width * left, height * upper,
                   width * right, height * lower)
    if 'rows' in kwargs or 'columns' in kwargs:
        image.resize(kwargs['rows'], kwargs['columns'])
    img = image.dump()
    return img, 200, {'Content-Type':kwargs['contentType'],'Pragma':'cache'}


    return str(kwargs)
