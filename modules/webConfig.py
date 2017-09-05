# coding: utf-8
# Permet de gérer des fonctions pour le fihcier index.py
import subprocess

def readConfig(f):
    with open (f,'r') as fic:
        return fic.read() .decode('utf-8',errors='ignore')

def writeConfig(f,c):
    with open (f,'wb') as fic:
        fic.write(c.encode('utf-8'))
    return "ok"

def modifPortURL(URL,Port):
    ind=URL.find(':',6)
    if (ind != -1) : URL = URL[: ind]
    URL=URL.replace('https://','http://')
    if (URL.endswith('/') == False) : 
      URL+=':' + str(Port) + '/'
    else:
      URL=URL[0:-1] + ':' + str(Port) + '/'
    return URL
   
def launch_process(param):
    process = subprocess.Popen(param, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.wait()
    return {'output' : unicode(process.stdout.read(),"utf-8"), 'error' : unicode(process.stderr.read(),"utf-8")}
  
    
