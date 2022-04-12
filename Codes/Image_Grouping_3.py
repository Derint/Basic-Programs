
#!/usr/bin/env python
# coding: utf-8


import os
import re
import shutil
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from tokenize import Number


def image(image_file, path):
    global c, go
    temp = re.search(r'(\d{8,})', image_file)

    if temp:
        if len(temp.group(1)) > 8:
            dt = datetime.fromtimestamp(int(temp.group(1))/1000)
            fold_name = dt.strftime("%d-%m-%Y")
        else:
            t = temp.group(1)
            fold_name = f'{t[6:]}-{t[4:6]}-{t[:4]}'

        if not os.path.isdir(output_folder+M_fold_name+slash+fold_name):
            os.makedirs(output_folder+M_fold_name+slash+fold_name)

        if not os.path.isfile(output_folder + M_fold_name+slash+fold_name+slash+image_file):

            shutil.copy2(path+slash+image_file, output_folder +
                         M_fold_name+slash+fold_name+slash+image_file)
            print(
                f'\r    [*]  Processed :: {str(round(c/len(os.listdir(path))*100, 2 )).center(7)} % ', end='')
            go = True
            c += 1


def getArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p", "--path", help="Path to Image Directory", dest="path")
    parser.add_argument("-fn", "--folder_name",
                        help="Folder Name In which you want to save all the files", dest="M_fold_name")
    parser.add_argument('-t', '--thread_no', dest='n',
                        help="Number of threads you want to use.")

    parser.add_argument('-o', '--output_folder', dest="output_folder",
                        help="Path Where you want to save this file.")
    return parser.parse_args()


def secSearch(text):
    temp = re.search(r'(\d{8,})', text)
    if temp:
        if len(temp.group(1)) > 8:
            dt = datetime.fromtimestamp(int(temp.group(1))/1000)
            fileName = dt.strftime(
                "%d-%m-%Y %H_%M_%S")+f"_{int(dt.microsecond/1000)}"+'.'+text.split('.')[-1]
            return True, fileName
    return False, text


def NumberOfFiles(dir):
    c = 0
    for i, j, k in os.walk(dir):
        c += len(k)
    return c


print('\n')
slash = "\\" if os.name in ['nt', 'dos'] else '/'
args = getArguments()
path = args.path
n = args.n
output_folder = args.output_folder

if not output_folder:
    output_folder = os.getcwd()+slash
else:
    if not os.path.isdir(output_folder):
        print('   [X]  Invalid output Folder Path  ')
        exit()

    if not output_folder.endswith(slash):
        output_folder += slash
pre_cnt = NumberOfFiles(output_folder)

if not n:
    n = len(os.listdir(path))
n = int(n)


if not path:
    path = input("    [>]  Enter Image Directory Path : ")
    if path == '':
        path = os.getcwd()

if not os.path.isdir(path):
    print("    [X]  Folder not Found ")
    exit()


M_fold_name = args.M_fold_name
if not M_fold_name:
    M_fold_name = "Group_Images"


imageList = os.listdir(path)


c = 0
go = False


for i in imageList:
    temp = re.search(r'(\d{8,})', i)
    uc = False
    if temp:
        if len(temp.group(1)) > 8:
            uc1 = input(
                "    [>]  File Name is given in seconds format Do you want to change it (Y/n) : ")
            if uc1.lower() == 'y':
                uc = True
            break


for _ in range(3):
    with ThreadPoolExecutor(max_workers=n) as executor:
        for img in imageList:
            executor.submit(image, img, path)


if uc:
    l = 1
    for i, j, k in os.walk(output_folder+M_fold_name+slash):
        for file in k:
            con, fileName = secSearch(file)
            if con:
                print(f"\r    [*]  Renaming all the images {'.'*l} ", end='')
                temp = i+slash+secSearch(file)[1]
                if not os.path.isfile(temp):
                    os.rename(i+slash+file, temp)

                if l > 7:
                    print(
                        f"\r    [*]  Renaming all the images {' '*l} ", end='')
                    l = 1
                l += 1


print(f'\r  {" "*50}', end='')
z = abs(NumberOfFiles(output_folder) - pre_cnt)
# print(f'\r\n   C : {c}, pre_cnt : {pre_cnt}, current_cnt : {NumberOfFiles(output_folder)},  z : {z}, go : {go}', end='\n\n')

if z == 0:
    print(
        f'\r    [+]  All files were already arranged in : {output_folder+M_fold_name}{slash}')
    exit()

if go:
    print(f"\r    [+]  Grouping Completed....")

    import winsound
    duration = 500  # milliseconds
    freq = 410  # Hz
    for i in range(3):
        winsound.Beep(freq, duration)
else:
    try:
        os.rmdir(output_folder + M_fold_name)
    except:
        pass
    print("\r    [!]  No Images Were found the Directory..... ")
