# coding: utf-8
import codecs
from flask import  render_template, redirect, request, url_for
import os
from . import app

@app.route('/gestionFichier/<path:pathFiles>',methods=['GET'])
def lancement_gestionFichier(pathFiles):
    # from modules.gestionFichier import make_tree
    path = os.path.expanduser(app.config["DDL_PATH"])
    pathFiles = '/' + pathFiles
    treeFiles = make_tree(pathFiles.encode('utf-8'), True, app.config["LST_EXCL_FILES"])
    treePath = make_tree(path.encode('utf-8'), False, app.config["LST_EXCL_PATH"])
    return render_template('gestionFichier.html',file_list=treeFiles,path_list=treePath,pathFiles=pathFiles)
@app.route('/gestionFichier/<path:pathFiles>',methods=['POST'])
def traitement_gestionFichier(pathFiles):
    # from modules.gestionFichier import Action
    pathFiles = Action(request, pathFiles)
    return redirect(url_for('lancement_gestionFichier',pathFiles=pathFiles))

def insertAccents(f):
    lstcarac = [[u'\xc3\xa2' , u'â'] , [u'\xc3\xa4' , u'ä'] , [ u'\xc3\xa0' , u'à'] , [ u'\xc3\xa9' , u'é'] , [ u'\xc3\xa8', u'è'] , [ u'\xc3\xab', u'ë'] , [ u'\xc3\xaa', u'ê']]
    for old, new in lstcarac:
        #if old==u'\xc3\xa9':
		#     raise
        f = f.replace(old, new)
    #for carac in lstcarac:
    #    f = f.replace(carac[0],carac[1])
    return f

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
		#url=request.path
		#url += request.form['repPrinc']
		#return render_template(url) 
	elif request.form['submitButton']=='Lancer':
		TypeAction=request.form['ChxAction']
		import urllib
		Rep=insertAccents(urllib.unquote(request.form['PathSelected'])).encode('utf-8')
		Files=insertAccents(urllib.unquote(request.form['FilesSelected'])).encode('utf-8').split(";")
		import os
		import shutil
		if TypeAction=='NvDossier':
			os.mkdir(os.path.join(Rep,'New'))
		elif TypeAction=='SupprimerDossier':
		    shutil.rmtree(Rep)
		elif TypeAction=='SupprimerFichiers':
			for File in Files:
				if File!='':os.remove(File)
		elif TypeAction=='Deplacer':
			for File in Files:
				if File!='':shutil.move(File,Rep)
		elif TypeAction=='Copier':
			for File in Files:
				if File!='':shutil.copy2(File,Rep)
		return pathFiles
