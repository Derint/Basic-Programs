#!/usr/bin/env python
# coding: utf-8


from operator import index
from tabnanny import check
import requests
import re
import os
import bs4
import urllib.parse as urlparse
import argparse
from time import sleep, time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor


def saveFile(url, path, remain, chuckSize=10240, char1='#', char2='.'):
    global c, go, reagain_download
    res = requests.get(url, headers={"User-Agent": "XY"}, stream=True)
    byte_length = len(res.content)  # int(res.headers['content-length'])

    totalDataLength = 0
    if byte_length > 1e6:
        chuckSize *= 100000

    try:
        with open(path, 'wb') as file:
            for data in res.iter_content(chuckSize):
                if remain[1] == 1:
                    cal = round(totalDataLength / byte_length*100, 2)
                    print(
                        f'\r  [{char1 * int(cal / 2)}{char2 * (50 - int(cal / 2))}] |({str(cal).center(7)}%)', end='')
                file.write(data)
                totalDataLength += len(data)

        if remain[1] != 1:
            per = round(c/noOfFiles * 100, 2)
            print(
                f'\r  [{char1*int(per/2)}{char2*(50-(int(per/2)))}] ({str(per).center(7)}%) ({c} of {remain[1]}) ', end='')
            go = True
            c += 1
    except:
        reagain_download.append((url, '\\\\?\\'+path))
        os.remove(path)


def Crawl(url):
    global links, l
    print("\r\tGetting all the links " + '.'*l, end='')

    try:
        req = requests.get(url)
    except:
        pass

    soup = bs4.BeautifulSoup(req.content, features='html.parser')
    for i in soup.find_all({'a': 'href'}):
        if str(i.text).endswith('/'):
            Crawl(url + '/' + i.text)
            l += 1
        if l > n:
            print("\r\tGetting all the links " + ' ' * (n+1), end='')
            l = 1
        else:
            if i.text not in links and i.text != '..':
                links.append(url + '/' + i.text)


def check_url(url):
    msg = "\r  [-]  Invalid URL or Server not active"
    try:
        rq = requests.get(url)
        if rq.status_code in [200, 406]:
            pass
    except:
        print(msg)
        exit()


def fileName(link, check_file=False):
    path = plain_text(link.replace(url, '')).split('/')
    filename = path[-1]
    if len(filename) > 78:
        blink("  [*]  Changing File Name ...  (#ToLarge)", 1)
        filename = filename[:76] + '.' + filename.split('.')[-1]
        print('\r', ' '*100, end='')

    t = ''
    if not check_file:
        t = os.getcwd() + slash + m_fold_name + slash + fold_name
    return t + f"{slash}".join(path[:-1]) + slash + filename


def getPlainText(text):
    switch_elts = {'+': ' ', '%0A': '', '//': '/', '\n': '', '\t': ''}

    for i in switch_elts.keys():
        if i in text:
            text = text.replace(i, switch_elts[i])

    return text


def decode_link(url):
    return urlparse.unquote(url)


def plain_text(text):
    return decode_link(getPlainText(text))


def blink(text, times=3):
    for i in range(times):
        print(f'\r{text}', end='')
        sleep(0.7)
        print(f'\r{" "*(len(text)+3)}', end='')
        sleep(0.3)


def ifHasExt(url):
    if not url:
        return False
    return not url.endswith('/')


def getFolderNames(url, links):
    folder_names = set()
    for i in links:
        file_path = plain_text(i.replace(url, '')).split('/')
        folder_names.add("/".join(file_path[:-1]))
    return folder_names


def noOfFolders(path):
    s = 0
    for i, j, k in os.walk(path):
        s += len(j)
    return s


def Download_files(links_2_be_downloaded):
    with ThreadPoolExecutor(max_workers=nt) as executor:
        for i in range(len(links_2_be_downloaded)):
            executor.submit(
                saveFile, links_2_be_downloaded[i][0], links_2_be_downloaded[i][1], [c, noOfFiles])


def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%d:%02d:%02d" % (hour, minutes, seconds)


def getArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', '-u', dest='url',
                        help='URL of File to be downloaded.')
    parser.add_argument('--thread', '-t', dest='thread', help='No of Threads.')
    parser.add_argument('--Fold_name', '-Fn', dest='folder_name',
                        help="Folder Name In which you want to save all the downloaded files.")

    return parser.parse_args()


args = getArguments()
url = args.url
nt = args.thread
m_fold_name = args.folder_name


if m_fold_name is None:
    m_fold_name = 'Downloaded_Files'

if nt is None:
    nt = 5
nt = int(nt)


slash = '\\' if os.name in ['nt', 'dos'] else '/'

l, z, c, n = 1, 0, 0, 8

if url is None:
    url = input("\n  [>]  Enter URL: ").strip()
    print('\n')

if not url.startswith('http://') and not url.startswith('https://'):
    uc = input("Which Request you want Http or Https : ")
    if uc == '':
        uc = 'http'
    url = uc+'://' + url

try:
    index_link = re.search(r'http[s]{,1}://.*?/', url).group(0)
except:
    print('\r  [-]  No Files/Folders were found ')
    exit()


print("\r  [*]  Checking url ... ", end='')
check_url(url)
print("\r", ' '*100, end='')

if m_fold_name not in os.listdir(os.getcwd()):
    os.mkdir(m_fold_name)

loc = os.getcwd() + slash + m_fold_name + slash


go = False

if len(url.replace(index_link, '').split('.')[-1]) == 2:
    fname = plain_text(url.replace(index_link, '').split('/')[-1])
    if len(fname.split(".")) > 1:
        fname = fname.split("/")[-1]
    if not os.path.isfile(loc + fname):
        saveFile(url, loc + fname, [1, 1], 20, char1='$', char2='.')
        print('\r', ' '*100, end='')
        print("\r  [+]  Download Complete")
    else:
        print("\r  [o]  File Already Downloaded ")
        exit()

else:
    if not url.endswith('/'):
        url += '/'
    fold_name = plain_text(url.replace(index_link, '').replace('/', slash))
    pre_num = noOfFolders(m_fold_name+slash+fold_name)
    s_time = time()
    links = []
    Crawl(url)

    for i in range(len(links)):
        if '//' in links[i][len(index_link):]:
            links[i] = index_link + \
                links[i][len(index_link):].replace('//', '/')

    # If there is no is no folder name i.e Default folder name
    if not fold_name or fold_name is None:
        now = datetime.now()
        fold_name = 'F - ' + str(now.strftime("%d-%m-%y %H_%M_%S"))

    fold_name = fold_name.replace('/', slash)

    # Getting all the folder names to create directories
    folder_names = getFolderNames(url, links)

    # Creating Directories
    for i in list(folder_names):
        tmp_fold = m_fold_name + slash + \
            fold_name + slash + i.replace('/', slash)
        if not os.path.isdir(tmp_fold):
            os.makedirs(getPlainText(tmp_fold))

    # Keeping those links which are to be downloaded (i.e removing all the folder links)
    links = [i for i in links if not i.endswith('/')]

    # Checking if the file is already present in folder or not
    links_2_be_downloaded = []
    for i in range(len(links)):
        fn = fileName(links[i])
        tem_a, tem_b = os.path.isfile(fn), os.path.isfile('\\\\?\\'+fn)
        if not tem_a and not tem_b:
            if tem_b:
                fn = '\\\\?\\'+fn
            links_2_be_downloaded.append((links[i], fn))

    if len(links) != len(links_2_be_downloaded):
        print("\n  [$]  Some Files Were Already Downloaded.")
        uc = input('  [>]  Do you want to download them again (Y/n) : ')
        if uc.lower() == 'y':
            links_2_be_downloaded = []
            for i in range(len(links)):
                links_2_be_downloaded.append((links[i], fileName(links[i])))

    reagain_download = []
    noOfFiles = len(links_2_be_downloaded)

    Download_files(links_2_be_downloaded)
    if len(reagain_download):
        Download_files(reagain_download)

    print('\r', ' '*100, end='')

    if not links_2_be_downloaded:
        print(
            f"\r  [+]  All files Already Downloaded : {os.getcwd() + slash + m_fold_name + slash + fold_name}")
        exit()

    if go:
        af_num = noOfFolders(m_fold_name+slash+fold_name)
        print(
            f'\r  [INFO]  Downloaded {c} Files, {abs(pre_num-af_num)} Folders ')
        print("  [INFO]  Download Time : ", convert(time() - s_time))
        print("\r  [+]\t  Download Complete")
    else:
        print("\r  [-]  No Files where there in the given link... ")
