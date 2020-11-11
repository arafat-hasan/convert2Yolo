# -*-coding:utf-8-*-

import sys
import os
import csv

import xml.etree.ElementTree as Et
from xml.etree.ElementTree import Element, ElementTree
from PIL import Image

import json

from xml.etree.ElementTree import dump


class ClassChange:

    def __init__(self, change_cls_list_path):
        tmpdict = {}
        with open(change_cls_list_path, mode='r') as infile:
            reader = csv.reader(infile)
            tmpdict = {rows[0]: rows[1] for rows in reader}
        self.changelist = tmpdict
    
    def trim(self, data):
        for key in data:
            numobjects = data[key]["objects"]["num_obj"]
            objects  = data[key]["objects"]
            for idx in range(numobjects):
                objects[str(idx)]['name'] = self.changelist[objects[str(idx)]['name']]
                if objects[str(idx)]['name'] == "DELETE":
                    del objects[str(idx)]
            data[key]["objects"]["num_obj"] = len(data[key]["objects"]) - 1
            numobjects = data[key]["objects"]["num_obj"]
            newdict = {}
            idx = 0
            for k in objects:
                if k == "num_obj":
                    newdict["num_obj"] = objects[k]
                    idx = idx - 1
                else:
                    newdict[str(idx)] = objects[k]
                idx = idx + 1
            del data[key]["objects"]
            data[key]["objects"] = newdict
            del newdict
            del objects
        return data


