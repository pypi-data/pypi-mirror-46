# -*- coding: utf-8 -*-
"""
     Module for Json parameter file procedures
"""

import os
import codecs
import simplejson as json
from collections import OrderedDict

class JsonParams(object):
    """Json parameter reading support class"""
    def __init__(self, Tool, ConfigFolder, ConfigFile):
        """Class initialization procedure

        Args:
            self: The reserved object 'self'
            Tool: GEOPython tool (optional)
            ConfigFolder: Configuration file storing directory
            ConfigFile: Name of the configuration file (without extension)
        """
        self.Tool = Tool
        self.ConfigFolder = ConfigFolder
        self.ConfigFile = ConfigFile
        if not Tool == None:
            self.ConfigPath = os.path.join(self.Tool.ExecutePatch, ConfigFolder, ConfigFile)
        else:
            if not ConfigFolder == None:
                self.ConfigPath = os.path.join(ConfigFolder, ConfigFile)
            else:
                self.ConfigPath = ConfigFile
        if not self.ConfigPath.lower()[-4:] == "json":
            self.ConfigPath = self.ConfigPath + '.json'
        self.Params = []

    def GetParams(self):
        """Get parameters from the parameter file

        Args:
            self: The reserved object 'self'
        """
        f = codecs.open(self.ConfigPath, 'r', 'utf-8')
        JsonString = f.read()
        f.close()
        J = json.loads(JsonString, object_pairs_hook=OrderedDict)
        self.Params = J
        return self.Params

    def WriteParams(self):
        """Save parameters in the parameter file

        Args:
            self: The reserved object 'self'
        """
        JsonString = json.dumps(self.Params, sort_keys=True, indent=4 * ' ')
        f = codecs.open(self.ConfigPath, 'w', 'utf-8')
        f.write(JsonString)
        f.close()

    def UpdateValueByPath(self, path, Value, valueIsStringJson = False):
        elem = self.Params

        if valueIsStringJson:
            Value = json.loads(Value, object_pairs_hook=OrderedDict)

        pathList = path.strip("\\").split("\\")
        for x in pathList[:-1]:
                elem = elem[x]
        LastKey = pathList[-1:][0]

        elem[LastKey] = Value


    def GetValueByPath(self, path):
        elem = self.Params
        pathList = path.strip("\\").split("\\")
        for x in pathList:
                elem = elem[x]

        return elem