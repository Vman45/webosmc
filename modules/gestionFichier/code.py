# coding: utf-8
import codecs
# from flask import request
import os
from flask import Flask,jsonify
app = Flask(__name__)

from modules.webConfig import launch_process

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
        tree = dict(name=os.path.basename(path).decode('utf-8'), fullname=path.decode('utf-8'), type = 'folder', children=[])
    except (UnicodeDecodeError,AttributeError) as err:
        tree = dict(name=os.path.basename(path), fullname=path, type = 'folder', children=[])
    try: 
        lst = os.listdir(path)
    except UnicodeEncodeError:
        lst = os.listdir(path.encode('utf-8'))
    else:
        if lst != []:
            lst.sort()
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
                    tree['children'].append(dict(name=name.decode('utf-8',errors='ignore'), fullname=fn.decode('utf-8',errors='ignore'), type = 'file')) 
    return tree
    
def make_tree(path, includeFiles, lstExcl):
    try: 
        tree = dict(name=os.path.basename(path).decode('utf-8'), fullname=path.decode('utf-8'), type = 'folder', children=[])
    except (UnicodeDecodeError,AttributeError) as err:
        tree = dict(name=os.path.basename(path), fullname=path, type = 'folder', children=[])
    try: 
        lst = os.listdir(path)
    except UnicodeEncodeError:
        lst = os.listdir(path.encode('utf-8'))
    #except OSError:
    #    pass #ignore errors
    else:
    #   raise
        app.logger.info('lst = %s' %lst)
        if lst != []:
            lst.sort()
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
                        tree['children'].append(dict(name=name.decode('utf-8',errors='ignore'), fullname=fn.decode('utf-8',errors='ignore'), type = 'file')) 
    return tree

def Action(request,pathFiles):
    app.logger.info('Traitement du formulaire : ')
    app.logger.info( request.form['submitButton'])
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
            shutil.move(Files[0],os.path.join(os.path.dirname(Files[0]),request.form['NomNvFile'].encode('utf-8')))
        elif TypeAction=='Deplacer':
            for File in Files:
                if File!='':
                    if os.path.exists(File)==True: shutil.move(File,Rep)
        elif TypeAction=='Copier':
            for File in Files:
                if File!='':
                    if os.path.exists(File)==True:shutil.copy2(File,Rep)
        return pathFiles
    elif request.form['submitButton']=='EnregFichier':
        content=request.form['Scriptcontenu'].strip()
        fichier=request.form['FileSelected'].strip()
        app.logger.info('Enregistrement du fichier : ' + fichier + '\n' + content)
        from modules.webConfig import writeConfig
        with open (fichier,"w") as fic:
            fic.write(content)
        return pathFiles
    
def getLog(pathFiles):
    ret= launch_process(["ls",pathFiles])
    if ret['error'] == '':
        retls = ret['output']
        # app.logger.info('Resultat ls : \n' + retls)
        lstFic = retls.splitlines()
        retour = u""
        # app.logger.info('LstFic=' + str(lstFic))
        for Fic in lstFic:
            rettail = launch_process(["tail", pathFiles + Fic])
            # app.logger.info(' retour ' + str(param) + ' : ' + rettail['output'] + 'erreurs :' + rettail['error'])
            retour+= u'===>  ' + Fic  + u'  <===\n' + rettail['output'] + u'\n\n'
    app.logger.info(' retour log ' + str(pathFiles) + ' : ' + retour)
    return jsonify({'log':retour})
