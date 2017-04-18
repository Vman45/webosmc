# coding: utf-8

def readConfig(f):
    with open (f,"r") as fic:
        return fic.read()

def writeConfig(f,c):
    with open (f,"w") as fic:
        fic.write(c)
    return "ok"
