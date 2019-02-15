# coding=utf-8
import json
import os
import sys
import shutil
from PIL import Image
from os import walk

# read finder url
dirName = sys.argv[1]

# read all files
f = []
for (dirpath, dirnames, filenames) in walk(dirName):
    f.extend(filenames)
    break

print f

# filter atlas files
for filename in f:
    [name, type] = filename.split('.')
    if type == 'atlas':
        print '\n'
        atlas = open(dirName + '/' + filename, 'r')
        data = json.loads(atlas.read())
        image_name = 'atlas/' + data['meta']['image']
        path = 'dist/' + data['meta']['prefix']
        print image_name
        print path

        # 删除文件夹
        if os.path.exists(path):
            shutil.rmtree(path)

        # 创建文件夹
        os.makedirs(path)

        # 加载图片
        im = Image.open(image_name)
        frames = data['frames']

        for frame in frames:
            frame_info = frames[frame]
            x = frame_info['frame']['x']
            y = frame_info['frame']['y']
            w = frame_info['frame']['w']
            h = frame_info['frame']['h']
            print frame, x, y, w, h
            box = (x, y, x + w, y + h)
            region = im.crop(box)
            region.save(path + frame)
