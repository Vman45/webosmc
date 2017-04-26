#! /usr/bin/python 
# -*- coding:utf-8 -*- 
from flask import Flask, flash, render_template, redirect, request, url_for, jsonify
import flask, os
app = Flask(__name__)

# Gestion Log
import logging
from logging.handlers import RotatingFileHandler

# Gestion fichier config 
# app.config.from_object('config')
ini = ConfigParser.ConfigParser()
ini.read('config.ini')
app.config.update(SECRET_KEY=ini.get('RUN','SECRET_KEY'))
# Modules complémentaires
from modules.wymypy import wymypy
app.register_Blueprint(wymypy, url_prefix='/MPD')
from modules.gestionFichier import gestionFichier
app.register_Blueprint(gestionFichier, url_prefix='/gestionFichier')

#OK Terminé
@app.route('/')
def index():
    import subprocess
    ret = subprocess.check_output(ini.get('LINK', 'RECH_MAJ'))
    # ret = subprocess.check_output(app.config["RECH_MAJ"])
    if (ret == 1) :
        flash("Une nouvelle version du site est disponible\n Veuillez faire une mise à jour")
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
  # return render_template('jDownloader.html',path=app.config["JDOWNLOADER"])
  return render_template('jDownloader.html',path=ini.get('LINK', 'JDOWNLOADER'))
@app.route('/majWeb/')
def majWeb():
    # os.system(app.config["MAJ_SITE"])
    os.system(ini.get('LINK', "MAJ_SITE"))
    flash('OK\nmaj faite !!!!')
    return redirect(url_for('index'))
    
@app.route('/config/',methods=['GET'])
def GETconfigWeb():
    from modules.webConfig import readConfig
    # content = readConfig('../config.py')
    content = readConfig('../config.ini')
    return render_template('config.html',content=content)  
@app.route('/config/',methods=['POST'])
def POSTconfigWeb():
    from modules.webConfig import writeConfig
    # ret = writeConfig('../config.py',request.form['contenu'])
    ret = writeConfig('../config.ini',request.form['contenu'])
    return render_template('config.html',content=request.form['contenu'])  

  #                                         En cours développement
@app.route('/log/')
def FichiersLog():
    return render_template('log.html')
# **********************************Remplacé par Blueprint en haut 

    
# @app.route('/gestionFichier/<path:pathFiles>')
# def gestionFichier(pathFiles):
    # import modules.gestionFichier
# @app.route('/MPD/')
# def Musique():   
    # return render_template('MPD.html')
    
    
@app.route('/test/')
def lancement_test():
    from modules.status import get_status
    app.logger.warning('testing warning log %s %d','ok', 21)
    app.logger.info('testing info log')
    app.logger.error('testing error log')
    return render_template('test.html',data=get_status())

@app.route('/test/', method='post')
def get_data():
    from modules.status import get_status
    return {"status": "OK", "data": get_status()}

if __name__ == '__main__':
    # Debug = app.config["DEBUG"]
    Debug = ini.get('RUN','DEBUG')
    if Debug == 'True':
        # initialize the log handler
        logHandler = RotatingFileHandler('info.log', maxBytes=1000000, backupCount=3)
#        formatter = logging.Formatter("[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
        formatter = logging.Formatter( "%(asctime)s | %(pathname)s:%(lineno)d | %(funcName)s | %(levelname)s | %(message)s ")
        logHandler.setFormatter(formatter)
        # set the log handler level
        logHandler.setLevel(logging.DEBUG)
#        logHandler.setLevel(logging.INFO)
#        logHandler.setLevel(logging.ERROR)
        # set the app logger level
        app.logger.setLevel(logging.DEBUG)
#        app.logger.setLevel(logging.INFO)
        app.logger.addHandler(logHandler)    

    # app.run(debug=Debug, port=app.config["PORT"], host='0.0.0.0')
    app.run(debug=Debug, port=ini.get('RUN','PORT'), host='0.0.0.0')
