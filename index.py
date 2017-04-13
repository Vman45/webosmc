#! /usr/bin/python 
# -*- coding:utf-8 -*- 
                                                                                                                                                                                                              
from flask import Flask, flash, render_template, redirect, request, url_for, jsonify
import flask, os
app = Flask(__name__)
app.config.from_object('config')

#OK Terminé
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/dev/')
def dev():
    url_root=request.url_root.lstrip()
    ind=url_root.find(':',6)
    if (ind != -1) : url_root = url_root[: ind]
    url_root=url_root.replace('https://','http://')
    if (url_root.endswith('/') == False) : 
      url_root+=':4200/'
    else:
      url_root=url_root[0:-1] + ':4200/'
    return render_template('dev.html',path=url_root)
@app.route('/JD/')
def JD():
  return render_template('jDownloader.html',path=app.config["JDOWNLOADER"])
@app.route('/majWeb/')
def majWeb():
    os.system(app.config["MAJ_SITE"])
    flash('OK\nmaj faite !!!!')
    return redirect(url_for('index'))
@app.route('/gestionFichier/<path:pathFiles>',methods=['GET'])
def lancement_gestionFichier(pathFiles):
    from gestionFichier import make_tree
    path = os.path.expanduser(app.config["DDL_PATH"])
    pathFiles = '/' + pathFiles
    treeFiles = make_tree(pathFiles.encode('utf-8'), True, app.config["LST_EXCL_FILES"])
    treePath = make_tree(path.encode('utf-8'), False, app.config["LST_EXCL_PATH"])
    return render_template('gestionFichier.html',file_list=treeFiles,path_list=treePath,pathFiles=pathFiles)
@app.route('/gestionFichier/<path:pathFiles>',methods=['POST'])
def traitement_gestionFichier(pathFiles):
    from gestionFichier import Action
    pathFiles = Action(request, pathFiles)
    return redirect(url_for('lancement_gestionFichier',pathFiles=pathFiles))
  
#                                         En cours développement
@app.route('/test/<path:pathFiles>',methods=['GET'])
def lancement_test(pathFiles):
    from gestionFichier import make_tree
    path = os.path.expanduser(app.config["DDL_PATH"])
    pathFiles = '/' + pathFiles
    treeFiles = make_tree(pathFiles, True, app.config["LST_EXCL_FILES"])
    treePath = make_tree(path, False, app.config["LST_EXCL_PATH"])
    return render_template('test.html',file_list=treeFiles,path_list=treePath,pathFiles=pathFiles)
@app.route('/test/<path:pathFiles>',methods=['POST'])
def traitement_test(pathFiles):
    from gestionFichier import Action
    pathFiles = Action(request, pathFiles)
    return redirect(url_for('lancement_test',pathFiles=pathFiles))

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
