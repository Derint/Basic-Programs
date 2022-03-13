#!/usr/bin/env python
# coding: utf-8


from PIL import Image
from PIL.ExifTags import TAGS
import os
import argparse


def arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-path', '--p', dest='path',
                        help='Enter Directory Path')
    return parser.parse_args()


def noOfFiles(path):
    c = 0
    for i in os.listdir(path):
        if i.split('.')[-1].lower() in ['jpg', 'mp4', 'jpeg', 'png']:
            c += 1
    return c


path = arguments().path

fold_name = 'Images'
slash = '\\' if os.name in ['nt', 'dos'] else '/'

if path is None:
    path = os.getcwd()

if not os.path.isdir(path):
    print("\r \t[!] Invalid Path..")
    exit()

go = False
tf = noOfFiles(path)

if tf and fold_name not in os.listdir(path):
    os.mkdir(path + slash + fold_name)

c = 1
for i in os.listdir(path):
    ext = i.split('.')[-1]
    if ext in ['jpg', 'png', 'JPEG', 'mp4']:
        imagename = i
        image = Image.open(path + slash + imagename)
        exifdata = image.getexif()

        for tag_id in exifdata:
            tag = TAGS.get(tag_id, tag_id)
            data = exifdata.get(tag_id)

            if isinstance(data, bytes):
                data = data.decode()

            if tag == 'DateTime':
                date = data[:10].split(":")
                date = date[-1] + '_' + date[1] + '_' + date[0]
                print(f'\r  Current Image: {data} ({c} of {tf})', end='')

                if date not in os.listdir(path + slash + fold_name):
                    os.makedirs(f'{path}{slash}{fold_name}{slash}{date}')

                image.save(f'{path}{slash}{fold_name}{slash}' +
                           date + slash + data.replace(':', '_')+'.'+ext, exif=exifdata)
                go = True
                c += 1

if go:
    print("\r\t[+]  All Your Images have been save to their respective Folders")
else:
    print("\r\t[-]  No Meta-Data was found in the given Directory.")
