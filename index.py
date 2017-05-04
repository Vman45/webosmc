#! /usr/bin/python 
# -*- coding:utf-8 -*- 
from flask import Flask, flash, render_template, redirect, request, url_for, jsonify
import flask, os
app = Flask(__name__)

# Gestion Log
import logging
from logging.handlers import RotatingFileHandler

# Gestion fichier config 
app.config.from_object('config')
# Modules complémentaires
# from modules.wymypy import wymypy
# app.register_blueprint(wymypy, url_prefix='/MPD')
from modules.gestionFichier.view import gestionFichier
app.register_blueprint(gestionFichier, url_prefix='/gestionFichier')


# app.logger.warning('testing warning log %s %d','ok', 21)
# app.logger.info('testing info log')
# app.logger.error('testing error log')


#OK Terminé
@app.context_processor
def inject_dict_for_all_templates():
    return dict(MENU=app.config["GEN_MENU"],AFF_BANDEAU=app.config["GEN_AFF_BANDEAU"])
    
@app.route('/')
def index():
    import subprocess
    ret = subprocess.check_output(app.config["LINK_VERIFMAJ"])
    app.logger.info('Verif MAJ :' + ' Resultat : ' + ret + '///')
    if (ret[:10] <> "Up-to-date") :
        flash(u"Une nouvelle version du site est disponible\n Veuillez faire une mise à jour")
    return render_template('index.html')
@app.route('/SSH/')
def ClientSSH():
    from modules.webConfig import modifPortURL
    return render_template('SSH.html',path=modifPortURL(request.url_root.lstrip(),app.config['SSH_PORT']))
@app.route('/kodi/')
def ClientKodi():
    from modules.webConfig import modifPortURL
    return render_template('kodi.html',path=modifPortURL(request.url_root.lstrip(),app.config['KODI_PORT']))
@app.route('/JD/')
def JD():
  return render_template('jDownloader.html',path=app.config["LINK_JDOWNLOADER"])
@app.route('/majWeb/')
def majWeb():
    os.system(app.config["LINK_MAJ_SITE"])
    flash('OK\nmaj faite !!!!')
    return redirect(url_for('index'))
    
@app.route('/config/',methods=['GET'])
def GETconfigWeb():
    from modules.webConfig import readConfig
    content = readConfig('config.py')
    return render_template('config.html',content=content.strip())
@app.route('/config/',methods=['POST'])
def POSTconfigWeb():
    from modules.webConfig import writeConfig
    ret = writeConfig('config.py',request.form['contenu'].strip())
    return render_template('config.html',content=request.form['contenu'].strip())

  #                                         En cours développement
@app.route('/log/')
def FichiersLog():
    return render_template('log.html')

@app.route('/test/')
def lancement_test():
    from modules.status import get_status
    app.logger.info('testing info log')
    return render_template('test.html',data=get_status())

@app.route('/_majData/', methods=['GET'])
def get_majData():
    from modules.status import get_status
    # return jsonify("status"= "OK", "data"= get_status())
    data = get_status()
    app.logger.info('_Majdata=' + data)
    return jsonify(data = data)
if __name__ == '__main__':
    Debug = app.config["DEBUG"]
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

    app.run(debug=Debug, port=app.config["PORT"], host='0.0.0.0')