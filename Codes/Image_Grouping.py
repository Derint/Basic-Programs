#!/usr/bin/env python
# coding: utf-8


from concurrent.futures import ThreadPoolExecutor, as_completed
import os
from PIL import Image
from PIL.ExifTags import TAGS
import argparse


def image(img_file_path, fold_name):
    global c
    ext = img_file_path.split('.')[-1]
    image = Image.open(img_file_path)  # <---- path here
    exifdata = image.getexif()

    for tag_id in exifdata:
        tag = TAGS.get(tag_id, tag_id)
        data = exifdata.get(tag_id)

        if isinstance(data, bytes):
            data = data.decode()

        if tag == 'DateTime':
            date = data[:10].split(":")
            date = date[-1] + '_' + date[1] + '_' + date[0]
            print(f'\r  [*]  Processed {round(c/tf * 100)} % ', end='')
            if date not in os.listdir(fold_name):
                os.makedirs(f'{fold_name}{slash}{date}')

            fn = f'{fold_name}{slash}' + date + \
                slash + data.replace(':', '_')+'.'+ext
            if not os.path.isfile(fn):
                image.save(fn, exif=exifdata)
                c += 1


def getArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p", "--path", help="Image Directory Path", dest="path")
    return parser.parse_args()


slash = '\\' if os.name in ['nt', 'dos'] else '/'
m_fold_name = "Images"
path = getArguments().path

if path is None:
    path = input("  [>]  Enter Path : ")

if path == '':
    os.getcwd()

if not os.path.isdir(path):
    print("\r \t[!] Invalid Path..")
    exit()

if not path.endswith(slash):
    path += slash

if m_fold_name not in os.listdir(path):
    os.mkdir(path + m_fold_name)

print('\n')
imgList = []
for i in os.listdir(path):
    if i.split('.')[-1] in ['jpg', 'png', 'JPEG', 'mp4']:
        imgList.append(path + i)


n, c, tf = 20, 1, len(imgList)

for i in range(2):
    with ThreadPoolExecutor(max_workers=n) as executor:
        for img in imgList:
            executor.submit(image, img, path + m_fold_name)

print(f'\r {" "*20}', end='')
print("\r  [+]  All the images are sorted in their respective folder. ")
