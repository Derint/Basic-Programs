from PIL import Image
from PIL.ExifTags import TAGS
import os

go = False
for i in os.listdir():
    ext = i.split('.')[-1]
    if ext in ['.jpg', '.png', '.JPEG', '.mp4']:
    # if i.endswith('.jpg') or i.endswith('.png') or i.endswith:
        imagename = i
        image = Image.open(imagename)
        exifdata = image.getexif()
        
        for tag_id in exifdata:
            tag = TAGS.get(tag_id, tag_id)
            data = exifdata.get(tag_id)
            
            if isinstance(data, bytes):
                data = data.decode()

            if tag == 'DateTime':
                date = data[:10].replace(':','_')
                print('\r Current Image: ' + data + ', saving in ' + 'Date '+date+' folder.', end='')

                if f'Date {date}' not in os.listdir():
                    os.mkdir(os.getcwd()+'\\Date '+date+'\\')
                
                image.save(os.getcwd()+'\\Date '+date+'\\'+data.replace(':','_')+'.jpg')
                go = True


if go:
    print("\rAll Your Images have been save to their respective Folders")

else:
    print("\rNo Meta-Data was found in current Directory.")

