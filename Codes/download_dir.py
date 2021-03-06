import requests, re, os, collections
import urllib.parse as urlparse
import argparse
from time import sleep



def extract_links_from(url):
    global l
    try:
        response = requests.get(url)
        files = re.findall('(?:href=")(.*?)"', response.content.decode(errors='ignore'))
        
        ret_files = []
        for i in files:
            ret_files.append(i.replace('%2F', '/'))
        
        return ret_files
    except:
        print("[-] I Think the url is not a vaild one OR maybe you are not connected to the Server ..")
        exit()


def crawl(url):
    global l
    href_links = extract_links_from(url)
    print("\r\tGetting all the links (Found " + str(len(target_links)) + " Links) " + '.'*l, end='')

    for link in href_links:
        
        link = urlparse.urljoin(url, link)
        
        if '#' in link:
            link = link.split('#')[0]

        if file_url in link and link not in target_links:
            target_links.append(link)
            crawl(link)

        l+=1
        if l>n:
            print("\r\tGetting all the links (Found " + str(len(target_links)) + " Links)" + ' ' *(n+1) , end='')
            l=1
 
            
def check_sentence(sentence):
    words = sentence.split('/')
    word_counts = collections.Counter(words)
    for word, count in sorted(word_counts.items()):
        if count>1:
            return sentence.replace(word+'/','', 1)
        
    return sentence


def saveFile(url, path, remain, chuckSize=1024, char='#'):
    res = requests.get(url, stream=True)
    byte_length = int(res.headers['Content-length'])

    totalDataLength = 0
    if byte_length > 1e6: size = f", size: {round(byte_length/1048576, 2)} Mb."
    else: size = f", size: {round(byte_length/1024, 2)} kb."

    try:
        with open(path, 'wb') as file:
            for data in res.iter_content(chuckSize):
                cal = round(round(totalDataLength / byte_length, 2)*100)
                
                print(f'\r  [{char * int(cal / 2)}{"." * (50 - int(cal / 2))}] |({cal}%){size}, ({remain[0]} of {remain[1]})', end='') 
                file.write(data)
                totalDataLength += len(data)
        print(f'\r{" " * 100}',end='')
        

    except KeyboardInterrupt:
        print("\nInterrupted By User")
        os.remove(path)


def isEmpty(path): # From stackoverflow
    if os.path.exists(path) and not os.path.isfile(path):
        if not os.listdir(path):
            print("\r\tPurging : " + path, end='')
            os.rmdir(path)
            sleep(0.5)
        else:pass
    else:
        print("The path is either for a file or not valid")
        print('---'*20)


def getPlainText(text):
    switch_elts = {'+':' ', '%0A':''}
    
    for i in switch_elts.keys():
        if i in text:
            text = text.replace(i, switch_elts[i])
            
    return text


def decode_link(url):
    return urlparse.unquote(url)


def plain_text(text):
    return decode_link(getPlainText(text))


def getArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', '-u', dest='url', help='URL of File to be downloaded.')
    return parser.parse_args()


ext = ['html', 'json', 'py', 'java', 'c', 'dat', 'dat', 'dir', 
 'exe', 'apk', 'docx', 'pptx', 'txt', 'pdf', 'jpg', 'png', 'JPEG'
 'doc', 'bak', 'mp3', 'mp4', 'wav', 'html', 'css', 'zip', 'ipynb'
 'deb', 'xz', 'csv', 'xlsx', 'xls', 'db', 'jiff', '7z', 'rar', 
 'webp', 'sql', 'djvu', 'TXT', 'opus']


args = getArguments()
file_url = args.url

if file_url is None:
    file_url = input("Enter the URL: ").strip()

if 'http://' not in file_url:
    file_url = 'http://' + file_url

if not file_url.endswith('/') and file_url.split('.')[-1] not in ext:
    file_url += '/'

l = 0
n = 6 
target_links = []
crawl(file_url)

t = []
uk_ext = []

for i in target_links:
    if i.split('.')[-1] in ext:
        t.append(i)
    else:
        if i.split('.')[-1] not in uk_ext: 
            uk_ext.append(i.split('.')[-1])


s = set()
for i in t:
    f_name = i.replace(file_url, '')
    
    check_dir = len(f_name.split('/')) > 1
    fold_name = check_sentence("/".join(f_name.split('/')[:-1]))
    file_name = f_name.split('/')[-1].split('.')
    file_ext = file_name[-1]
    
    if check_dir:
        if file_ext not in ext:
            fold_name = check_sentence("/".join(f_name.split('/')))
                                                
        s.add(plain_text(fold_name))
        


if 'Downloaded_Files' not in os.listdir(os.getcwd()):
    os.mkdir('Downloaded_Files')

for i in s:
    if not os.path.isdir('Downloaded_Files/' + i):
        os.makedirs('Downloaded_Files/' + i)


go = False
j = 1
for i in t:
    subF = i.replace(file_url, '')
    if subF:
        temp_url = file_url+check_sentence(subF)

        try:
            fname = plain_text(check_sentence(subF))
    
            if len(fname) > 180:
                ext = fname.split('.')[-1]
                print(f"\r\nThe File Name is to Big.\nPlease rename this file.\n  Current File Name: {fname}")
                fname = input("New File Name: ")
                
            if len(fname)>180 or fname=='':
                fname = fname[:160] + '.' + ext
                
            saveFile(temp_url, "Downloaded_Files/"+fname, [j, len(t)])
            go = True
            j+=1

        except Exception as e:
            print('---'*20)
            print("Something went wrog", e)
            print('---'*20)
  
  
if file_url.split('.')[-1] in ext:
    saveFile(file_url, os.getcwd()+'/Downloaded_Files/'+file_url.split('/')[-1])
    go = True

for i, j, k in os.walk('./Downloaded_Files'):
    isEmpty(i)

if go:
    print("\r\t[+] Download Complete...")

else:
    print("\r  [-] No Files where there in the given link..      ")

if uk_ext:
    print("\n\t[!] Found these unknown Extension : " + ", ".join(uk_ext))