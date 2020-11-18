# -*-coding:utf-8-*-

import os
import xml.etree.ElementTree as ET
import json
import pprint
import copy
import csv
import argparse
from tqdm import tqdm
import glob
import cv2
import pathlib
from io import BytesIO

parser = argparse.ArgumentParser(description='label Converting example.')

parser.add_argument('--img_path', type=str, help='directory of image folder')
parser.add_argument('--label', type=str,
                    help='directory of label folder or label file path')
parser.add_argument('--img_type', type=str, help='type of image')
parser.add_argument('--convert_output_path', type=str,
                    help='directory of label folder')
parser.add_argument('--change_cls_list_file', type=str,
                    help='directory of change *.names file')


args = parser.parse_args()


def get_classes(change_cls_list_path):
    tmpdict = {}
    with open(change_cls_list_path, mode='r') as infile:
        reader = csv.reader(infile)
        tmpdict = {rows[0]: rows[1] for rows in reader}
    return tmpdict


def main(config):

    class_names = get_classes(config["change_cls_list"])

    xml_dir = config["label"]
    store_dir = config["output_path"]
    img_dir = config["img_path"]
    img_type = config["img_type"]

    print("Globbing started")
    filenames = glob.glob(xml_dir + '/**/*.xml', recursive=True)
    print("Total files: ", len(filenames))

    for filename in tqdm(filenames):
        #print(filename)
        basename = os.path.basename(filename)
        name_with_path = os.path.relpath(os.path.splitext(filename)[0], xml_dir)
        tree = ET.parse(filename)
        
        root = tree.getroot()
        root.find("filename").text = basename
        size = root.find("size")
        if size.find("width").text == None or size.find("height").text == None or size.find("depth").text == None or size.find("width").text == "0" or size.find("height").text == "0" or size.find("depth").text == "0":
            print(f'\nInvalid image size in `{basename}`, no worry, fixing...')
            im = cv2.imread(os.path.join(img_dir, name_with_path+img_type))
            h, w, d = im.shape
            print(f'Scanned image size: h, w, d = {h}, {w}, {d}')
            size.find("width").text = str(w)
            size.find("height").text = str(h)
            size.find("depth").text = str(d)

        for obj in root.findall('object'):  
            obj.find("name").text = class_names[obj.find("name").text]
            if obj.find("name").text == "DELETE":
                root.remove(obj)
        
        et = ET.ElementTree(root)

        savefilename = os.path.abspath(os.path.join(store_dir, "".join([name_with_path, ".xml"])))
        savedirectory = os.path.dirname(savefilename)
        pathlib.Path(savedirectory).mkdir(parents=True, exist_ok=True)

        f = BytesIO()
        et.write(f, encoding='utf-8', xml_declaration=True) 

        with open(savefilename, "wb") as xml_write:
            xml_write.write(f.getvalue()) 
    
    



if __name__ == '__main__':

    config = {
        "img_path": args.img_path,
        "label": args.label,
        "img_type": args.img_type,
        "output_path": args.convert_output_path,
        "change_cls_list": args.change_cls_list_file,
    }

    main(config)