#! /usr/bin/python 
# -*- coding:utf-8 -*- 
from flask import Flask, flash, render_template, redirect, request, url_for, jsonify
import flask, subprocess
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

from modules.status.app import get_status
from modules.webConfig import modifPortURL
from modules.webConfig import readConfig
from modules.webConfig import writeConfig
from modules.webConfig import launch_process

#OK Terminé
@app.context_processor
def inject_dict_for_all_templates():
    return dict(MENU=app.config["GEN_MENU"],AFF_BANDEAU=app.config["GEN_AFF_BANDEAU"])
    
@app.route('/')
def index():
    ret = launch_process(app.config["LINK_VERIFMAJ"])
    app.logger.info('Verif MAJ :' + ' Resultat : ' + ret['output'] + '///' + ret['error'])
    if (ret['error']  != '') :
        flash(u"Un problème est surcenu dans la vérification de mise à jour n\nMessage : <br>" + ret['output'] + u"\n\nErreur :\n" + ret['error'])
    elif (ret['output'][:10] != "Up-to-date" or ret['error']  != '') :
        flash(u"Une nouvelle version du site est disponible.\nVeuillez faire une mise à jour\n\nMessage : \n" + ret['output'] )
    return render_template('index.html')
@app.route('/_majData/', methods=['GET'])
def get_majData():
    data = get_status(app.config["STATUS_LSTPROC"])
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
    app.logger.info('MAJ site :' + ' Resultat : ' + ret['output'] + '///' + ret['error'])
    if ret['error']  == '':
        message = u'OK maj faite !!!!\n\n' + ret['output']
    else:
        message = u'Problème de mise à jour !!!!\n\n' + ret['output'] + u'\n\nErreur:\n' + ret['error']
    flash(message)
    return redirect(url_for('index'))
    
@app.route('/config/',methods=['GET'])
def GETconfigWeb():
    content = readConfig('config.py')
    return render_template('config.html',content=content.strip())
@app.route('/config/',methods=['POST'])
def POSTconfigWeb():
    ret = writeConfig('config.py',request.form['contenu'].strip())
    return render_template('config.html',content=request.form['contenu'].strip())

  #                                         En cours développement

@app.route('/test/')
def lancement_test():
    return render_template('test.html')


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

