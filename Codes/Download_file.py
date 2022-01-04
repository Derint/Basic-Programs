import requests, os
import argparse


def saveFile(url, path, chuckSize=1024, char='#'):
    res = requests.get(url, stream=True)
    byte_length = int(res.headers['Content-length'])

    totalDataLength = 0
    if byte_length > 1e6: size = f", size: {round(byte_length/1048576, 2)} Mb."
    else: size = f", size: {round(byte_length/1024, 2)} kb."

    try:
        with open(path, 'wb') as file:
            for data in res.iter_content(chuckSize):
                cal = round(round(totalDataLength / byte_length, 2)*100)
                
                print(f'\r[*]   [{char * int(cal / 2)}{"." * (50 - int(cal / 2))}] |({cal}%){size}', end='') 
                file.write(data)
                totalDataLength += len(data)
        print(f'\r{" " * 150}',end='')
        print('\r',end='')

    except KeyboardInterrupt:
        print("\nInterrupted By User")
        os.remove(path)


def getArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', '-u', dest='url', help='URL of File to be downloaded.')
    parser.add_argument('--path', '-p', dest='path', help='Path to save the file')

    return parser.parse_args()



check_encoding = {'%20':' ', '%2F':'/'}

args = getArguments()

url = args.url
path = args.path


if url is None:
    url = input('[-] Enter the URL: ').strip()

if path is None:
    path = input('[-] Enter the Path: ').strip()


for i in check_encoding.keys():
    if i in url:
        url = url.replace(i, check_encoding[i])

if '%' in url:
    t = url.index('%')
    print(f"Found encoding {url[t: t+3]}")
    print("Exiting Now")
    exit()


if not path:
    path = os.getcwd() + '\\'

if not (path.endswith('/') or path.endswith('\\')):
    path += '\\'

file_name = url.split('/')[-1].replace(' ', '_')

print(f'\nFile: {file_name}. \nURL: {url}')

saveFile(url, path+file_name)