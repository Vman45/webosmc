#! /usr/bin/python 
# -*- coding:utf-8 -*- 
from flask import Flask, flash, render_template, redirect, request, url_for, jsonify
import flask, subprocess, platform
app = Flask(__name__)

# Gestion Log
import logging
from logging.handlers import RotatingFileHandler

# Gestion fichier config 
app.config.from_object('config')
# Modules complémentaires
from modules.gestionFichier.view import gestionFichier
from modules.MPD.app import MPDClient
app.register_blueprint(MPDClient)
app.register_blueprint(gestionFichier, url_prefix='/gestionFichier')
from modules.ThrowBox.app import ThrowBox
app.register_blueprint(ThrowBox, url_prefix='/ThrowBox')
from modules.status.app import get_status
from modules.webConfig import modifPortURL
from modules.webConfig import readConfig
from modules.webConfig import writeConfig
from modules.webConfig import launch_process

@app.context_processor
def inject_dict_for_all_templates():
    if app.config["LINK_AFF_MSG"] == True and platform.system()[:3] != 'Win':
        ret = launch_process(app.config["LINK_VERIFMAJ"])
        output = ret['output'].replace('\n','')
        outputhtml =ret['output'].replace('\n','')
        app.logger.info('Verif MAJ :' + ' Resultat : ' + ret['output'] + '///' + ret['error'] + '///')
        if (output[len(output)-10:len(output)] != "Up-to-date"):
            if (ret['error']  != '') :
                flash(u"<h1>Un problème est survenu dans la vérification de mise à jour</h1> Message : " + outputhtml + u"<br><br>Erreur :" + ret['error'],'error')
            else:
                flash(u"<h1>Une nouvelle version du site est disponible.</h1><br>Veuillez faire une mise à jour<br><br>Message :<br>" + outputhtml + "<br><h2><a href='/majWeb/'>MaJ du serveur</a></h2>" , 'warning')
    import modules.status.status_functions as status_functions
    temperature=status_functions.getTemperature()
    return dict(MENU=app.config["GEN_MENU"],DEBUG=app.config["DEBUG"],temperature=temperature)

@app.route("/robots.txt")
def robots():
	return "User-agent: *\nDisallow: /"    

@app.route('/')
def index():
   return render_template('index.html')
@app.route('/status/')
def status():
    return render_template('status.html')
@app.route('/_majData/', methods=['GET'])
def get_majData():
    data = get_status(app.config["STATUS_LSTPROC"],app.config["STATUS_CPUMIN"])
    app.logger.info('majdata : ' + str(data) )
    return jsonify(data)
@app.route('/SSH/')
def ClientSSH():
    return render_template('SSH.html',path=modifPortURL(request.url_root.lstrip(),app.config['SSH_PORT']))
@app.route('/kodi/')
def ClientKodi():
    return render_template('kodi.html',path=modifPortURL(request.url_root.lstrip(),app.config['KODI_PORT']))
@app.route('/JD/')
def JD():
  return render_template('jDownloader.html',path=app.config["LINK_JDOWNLOADER"])
@app.route('/majWeb/')
def majWeb():
    ret = launch_process(app.config["LINK_MAJ_SITE"])
    app.logger.info('<h1>MAJ site :</h1>' + ' Resultat : ' + ret['output'] + '<br><br>Erreur :' + ret['error'])
    if ret['error']  == '':
        flash(u'<h1>OK maj faite !!!!</h1>' + ret['output'],'info')
    else:
        flash(u'<h1>Problème de mise à jour !!!!</h1>' + ret['output'] + u'<br><br>Erreur:' + ret['error'],'error')
    return redirect(url_for('index'))    
@app.route('/config/<path:pathFiles>',methods=['GET'])
def GETconfigWeb((pathFiles)):
    if pathFiles =='':
        pathFiles = 'config.py'
    else:
        pathFiles = '/' + pathFiles
    content = readConfig(pathFiles)
    return render_template('config.html',content=content.strip())
@app.route('/config/<path:pathFiles>',methods=['POST'])
def POSTconfigWeb((pathFiles)):
    if pathFiles =='':
        pathFiles = 'config.py'
    else:
        pathFiles = '/' + pathFiles
    app.logger.info('file content=%s',request.form['contenu'].split())
    ret = writeConfig(pathFiles,request.form['contenu'])
    return render_template('config.html',content=request.form['contenu'].strip())


if __name__ == '__main__':
    Debug = app.config["DEBUG"]
    if Debug == 'True':
        # initialize the log handler
        logHandler = RotatingFileHandler(filename='/home/osmc/tmp/webinfo.log', maxBytes=1000000, backupCount=3)
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
    app.run(debug=Debug, port=app.config["PORT"], host='0.0.0.0')
    
    # app.logger.warning('testing warning log %s %d','ok', 21)
    # app.logger.info('testing info log')
    # app.logger.error('testing error log')

