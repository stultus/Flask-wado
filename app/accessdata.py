#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim: sw=4:expandtab
#
# copyright 2014 Hrishikesh K B <hrishi.kb@gmail.com>
# Copyright 2008 Emanuele Rocca <ema@galliera.it>
# Copyright 2008 Marco De Benedetto <debe@galliera.it>
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

"""
DICOM data access layer.

Write your own __getfile function to suit your needs.
"""

from lib import *
import images

def __getfile(studyUID, seriesUID, objectUID):
    # search the dicom file based on the parametrs and return the filename
    # implement your own function here, for now it just returns a hard-coded
    # value
    objectfile = "sample.dcm"
    return objectfile

def get(studyUID, seriesUID, objectUID, format='jpeg'):
    """Function called by the main program to get an image."""
    objectfile = __getfile(studyUID, seriesUID, objectUID)
    return images.Dicom(objectfile, format)

if __name__ == "__main__":
    print get(studyUID="1.3.76.13.10010.0.5.74.3996.1224256625.4053",
        seriesUID="1.3.12.2.1107.5.4.4.1053.30000008100608242373400002493",
        objectUID="1.3.12.2.1107.5.4.4.1053.30000008100608324685900001822")
