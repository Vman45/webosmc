#! /usr/bin/python 
# -*- coding:utf-8 -*- 
                                                                                                                                                                                                              
from flask import Flask, flash, render_template, redirect, request, url_for, jsonify
import flask, os
app = Flask(__name__)
app.config.from_object('config')

#OK Terminé
@app.route('/')
def index():
    import modules.status
    
    return render_template('index.html')
@app.route('/SSH/')
def ClientSSH():
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
    from modules.gestionFichier import make_tree
    path = os.path.expanduser(app.config["DDL_PATH"])
    pathFiles = '/' + pathFiles
    treeFiles = make_tree(pathFiles.encode('utf-8'), True, app.config["LST_EXCL_FILES"])
    treePath = make_tree(path.encode('utf-8'), False, app.config["LST_EXCL_PATH"])
    return render_template('gestionFichier.html',file_list=treeFiles,path_list=treePath,pathFiles=pathFiles)
@app.route('/gestionFichier/<path:pathFiles>',methods=['POST'])
def traitement_gestionFichier(pathFiles):
    from modules.gestionFichier import Action
    pathFiles = Action(request, pathFiles)
    return redirect(url_for('lancement_gestionFichier',pathFiles=pathFiles))
@app.route('/config/',methods=['GET'])
def GETconfigWeb():
    from modules.webConfig import readConfig
    content = readConfig('../config.py')
    return render_template('config.html',content=content)  
@app.route('/config/',methods=['POST'])
def GETconfigWeb():
    from modules.webConfig import writeConfig
    ret = writeConfig('../config.py',request.form['contenu'])
    return render_template('config.html',content=request.form['contenu'])  

  #                                         En cours développement
@app.route('/log/')
def FichiersLog():
    return render_template('log.html')
@app.route('/MPD/')
def Musique():
    return render_template('MPD.html')

@app.route('/test/')
def lancement_test():
    return render_template('test.html')


if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
