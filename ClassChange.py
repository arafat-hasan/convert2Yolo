# -*-coding:utf-8-*-

import sys
import os
import csv

import xml.etree.ElementTree as Et
from xml.etree.ElementTree import Element, ElementTree
from PIL import Image
import cv2

import json

from xml.etree.ElementTree import dump


class ClassChange:

    def __init__(self, change_cls_list_path):
        tmpdict = {}
        with open(change_cls_list_path, mode='r') as infile:
            reader = csv.reader(infile)
            tmpdict = {rows[0]: rows[1] for rows in reader}
        self.changelist = tmpdict

    
    def trim(self, data, img_path, img_ext):
        for key in data:
            imgsize = data[key]["size"]
            if imgsize["width"] == None or imgsize["height"] == None or imgsize["depth"] == None or int(imgsize["width"]) == 0 or int(imgsize["height"]) == 0 or int(imgsize["depth"]) == 0:
                print(f'Invalid image size in `{key+".xml"}`, no worry, fixing...')
                file = key + img_ext
                im = cv2.imread(os.path.join(img_path, file))
                h, w, d = im.shape
                print("Image sizes: ", h, w, d)
                imgsize["width"] = str(w)
                imgsize["height"] = str(h)
                imgsize["depth"] = str(d)
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


