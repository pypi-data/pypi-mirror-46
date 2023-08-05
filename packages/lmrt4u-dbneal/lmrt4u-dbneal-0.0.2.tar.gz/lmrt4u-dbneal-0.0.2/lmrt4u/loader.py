# -*- coding unix -*-

import yaml
import json
import os 

def loadDocument():
    """Load Lmrt4uFile from current directory"""
    yamlFile = True
    jsonFile = False
    with open('Lmrt4uFile') as input_file:
        try:
            contents = yaml.safe_load(input_file)
        except:
            yamlFile = False

        if not yamlFile:
            try:
                contents = json.loads(input_file)
            except: 
                jsonFile = False
    if yamlFile or jsonFile:
        return contents
