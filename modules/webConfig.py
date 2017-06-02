# coding: utf-8
# Permet de gérer des fonctions pour le fihcier index.py

def readConfig(f):
    with open (f,"r") as fic:
        return fic.read()

def writeConfig(f,c):
    with open (f,"w") as fic:
        fic.write(c)
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
   
def launch_process(command,param):
    process = subprocess.Popen([command, param], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.wait()
    return {'output' : process.stdout.read(), 'error' : process.stderr.read()}
  
    