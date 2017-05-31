# coding: utf-8
import codecs
# from flask import request
import os
import subprocess
from flask import Flask,jsonify
app = Flask(__name__)

def insertAccents(f):
    lstcarac = [[u'\xc3\xa2' , u'â'] , [u'\xc3\xa4' , u'ä'] , [ u'\xc3\xa0' , u'à'] , [ u'\xc3\xa9' , u'é'] , [ u'\xc3\xa8', u'è'] , [ u'\xc3\xab', u'ë'] , [ u'\xc3\xaa', u'ê']]
    for old, new in lstcarac:
        #if old==u'\xc3\xa9':
        #     raise
        f = f.replace(old, new)
    #for carac in lstcarac:
    #    f = f.replace(carac[0],carac[1])
    return f

def recup_files(path, lstExcl):
    try: 
        tree = dict(name=os.path.basename(path).decode('utf-8'), fullname=path.decode('utf-8'), children=[])
    except (UnicodeDecodeError,AttributeError) as err:
        tree = dict(name=os.path.basename(path), fullname=path, children=[])
    try: 
        lst = os.listdir(path)
    except UnicodeEncodeError:
        lst = os.listdir(path.encode('utf-8'))
    else:
        for name in lst:
            Excluded=False
            for word in lstExcl:
                if word in name.decode('utf-8'):
                    Excluded=True
            if Excluded==False:
                try:
                    fn = os.path.join(path, name)
                except UnicodeDecodeError:
                    fn = os.path.join(path.encode('utf-8'), name)
                try:
                    isDir = os.path.isdir(fn)
                except UnicodeEncodeError:
                    isDir = os.path.isdir(fn.encode('utf-8'))
                if isDir == False:
                    tree['children'].append(dict(name=name.decode('utf-8',errors='ignore'), fullname=fn.decode('utf-8',errors='ignore'))) 
    return tree
    
def make_tree(path, includeFiles, lstExcl):
    try: 
        tree = dict(name=os.path.basename(path).decode('utf-8'), fullname=path.decode('utf-8'), children=[])
    except (UnicodeDecodeError,AttributeError) as err:
        tree = dict(name=os.path.basename(path), fullname=path, children=[])
    try: 
        lst = os.listdir(path)
    except UnicodeEncodeError:
        lst = os.listdir(path.encode('utf-8'))
    #except OSError:
    #    pass #ignore errors
    else:
    #   raise
        for name in lst:
            Excluded=False
            for word in lstExcl:
                if word in name.decode('utf-8'):
                    Excluded=True
            if Excluded==False:
                try:
                    fn = os.path.join(path, name)
                except UnicodeDecodeError:
                    fn = os.path.join(path.encode('utf-8'), name)
                try:
                    isDir = os.path.isdir(fn)
                except UnicodeEncodeError:
                    isDir = os.path.isdir(fn.encode('utf-8'))
                if isDir == True:
                    tree['children'].append(make_tree(fn, includeFiles, lstExcl))
                else:
                    if includeFiles == True:
                        tree['children'].append(dict(name=name.decode('utf-8',errors='ignore'), fullname=fn.decode('utf-8',errors='ignore'))) 
    return tree

def Action(request,pathFiles):
    if request.form['submitButton']=='ModifPath':
        return request.form['repPrinc'][1:].encode('utf-8')
    elif request.form['submitButton']=='Lancer':
        TypeAction=request.form['ChxAction']
        import urllib
        Rep=insertAccents(urllib.unquote(request.form['PathSelected'])).encode('utf-8')
        Files=insertAccents(urllib.unquote(request.form['FilesSelected'])).encode('utf-8').split(";")
        import os
        import shutil
        if TypeAction=='NvDossier':
            os.mkdir(os.path.join(Rep,request.form['NomNvDossier'].encode('utf-8')))
        elif TypeAction=='SupprimerDossier':
            shutil.rmtree(Rep)
        elif TypeAction=='SupprimerFichiers':
            for File in Files:
                if File!='':
                    if os.path.isdir(File) == True :
                        shutil.rmtree(File)
                    else:
                        os.remove(File)
        elif TypeAction=='RenameFile':
            shutil.rename(File,os.path.join(Rep,request.form['NomNvFile'].encode('utf-8')))
        elif TypeAction=='Deplacer':
            for File in Files:
                if File!='':shutil.move(File,Rep)
        elif TypeAction=='Copier':
            for File in Files:
                if File!='':shutil.copy2(File,Rep)
        return pathFiles

def launch_script(pathFiles):
    process = subprocess.Popen(['sh', pathFiles], stdout=subprocess.PIPE)
    output, _error = process.communicate()
    return {'output' : output, 'error' : _error}
    # ret = subprocess.check_output(["sh",pathFiles])
    # return ret
    
def getLog(pathFiles):
    process = subprocess.Popen(["ls", pathFiles], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.wait()
    ret = ''
    if process.stderr.read() == '':
        retls = process.stdout.read()
        # app.logger.info('Resultat ls : \n' + retls)
        lstFic = retls.splitlines()
        # app.logger.info('LstFic=' + str(lstFic))
        for Fic in lstFic:
            param = ["tail", pathFiles + Fic]
            process = subprocess.Popen(param, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            process.wait()
            rettail = process.stdout.read()
            # app.logger.info(' retour ' + str(param) + ' : ' + rettail + 'erreurs :' + process.stderr.read())
            ret+= '===>  ' + Fic  + '  <===\n' + rettail + '\n\n'
    app.logger.info(' retour log ' + str(pathFiles) + ' : ' + str(ret))
    return jsonify({'log':ret})