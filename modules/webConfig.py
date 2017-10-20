# -*- coding: utf-8 -*-
# Permet de gérer des fonctions pour le fichier index.py

import httplib
from urlparse import urlparse
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
    inc=0
    cmd=[]
    for word in param:
        cmd[inc].append(word)
        if "|" in word:
            inc=inc+1
    if inc = 0:    
        process = subprocess.Popen(param, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process.wait()
    else:
        process.stdout = ""
        for c in cmd:
            process = subprocess.Popen(param, stdin=process.stdout,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            process.wait()
        # Connecting Segments of a Pipe

        # Multiple commands can be connected into a pipeline, similar to the way the Unix shell works, by creating separate Popen instances and chaining their inputs and outputs together. The stdout attribute of one Popen instance is used as the stdin argument for the next in the pipeline, instead of the constant PIPE. The output is read from the stdout handle for the final command in the pipeline.

        # subprocess_pipes.py
        # import subprocess

        # cat = subprocess.Popen(
            # ['cat', 'index.rst'],
            # stdout=subprocess.PIPE,
        # )

        # grep = subprocess.Popen(
            # ['grep', '.. literalinclude::'],
            # stdin=cat.stdout,
            # stdout=subprocess.PIPE,
        # )

        # cut = subprocess.Popen(
            # ['cut', '-f', '3', '-d:'],
            # stdin=grep.stdout,
            # stdout=subprocess.PIPE,
        # )

        # end_of_pipe = cut.stdout

        # print('Included files:')
        # for line in end_of_pipe:
            # print(line.decode('utf-8').strip())
        # The example reproduces the command line:

        # $ cat index.rst | grep ".. literalinclude" | cut -f 3 -d:
        # The pipeline reads the reStructuredText source file for this section and finds all of the lines that include other files, then prints the names of the files being included.
        
        
    return {'output' : unicode(process.stdout.read(),"utf-8"), 'error' : unicode(process.stderr.read(),"utf-8")}
  

def checkUrl(url):
    p = urlparse(url)
    conn = httplib.HTTPConnection(p.netloc)
    try:
        conn.request('HEAD', p.path)
        resp = conn.getresponse()
        return resp.status < 400
    except:
        return False