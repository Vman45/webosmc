# coding: utf-8
from __future__ import unicode_literals
from flask import Flask
import os
import time
app = Flask(__name__)


def ReadPath(path):
    try:
        exists = os.path.exists(path)
    except UnicodeDecodeError:
        exists = os.path.exists(path.decode('utf-8'))
        path = path.decode('utf-8')
    except UnicodeEncodeError:
        exists = os.path.exists(path.encode('utf-8'))
        path = path.encode('utf-8')
    if not exists:
        print("Doesnt exist.")
        return None
    try:
        files=[]
        folders=[]
        lst = os.listdir(path)
        for name in lst:
            try:
                fn = os.path.join(path, name)
            except UnicodeDecodeError:
                fn = os.path.join(path.encode('utf-8'), name)
            try:
                isDir = os.path.isdir(fn)
            except UnicodeEncodeError:
                isDir = os.path.isdir(fn.encode('utf-8'))
            if isDir == False:
                files.append(name.decode('utf-8',errors='ignore')) 
            else:
                folders.append(name.decode('utf-8',errors='ignore'))
        return folders,files
    except StopIteration:
        print("empty.")
        return 0

def IsFile(path):
    try:
        exists = os.path.isdir(path)
    except UnicodeDecodeError:
        exists = os.path.isdir(path.decode('utf-8'))
    except UnicodeEncodeError:
        exists = os.path.isdir(path.encode('utf-8'))
    if exists:
        return False
    else:
        return True

def RemoveHiddenObjects(_list):
    _list2=list() # List that contains only visible,
                  # non-hidden objects.
    for element in _list:
        if element[0]!=".":
            _list2.append(element)

    return _list2


def log(message, file="log.txt"):
    """A barebones function that logs messages."""
    line="[{} >>> {}]\n\t{}\n\n".format(time.strftime("%d/%m/%Y"), time.strftime("%H:%M:%S"),message)
    file=open(file, "a")
    file.write(line)
    file.close()




