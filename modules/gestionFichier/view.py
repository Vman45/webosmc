coding: utf-8
import codecs, os, subprocess
from flask import Flask,render_template, redirect, request, url_for, Blueprint, jsonify
app = Flask(__name__)
app.config.from_object('config')
gestionFichier = Blueprint('gestionFichier',__name__)
from modules.gestionFichier.code import Action
from modules.gestionFichier.code import make_tree
from modules.gestionFichier.code import recup_files
from modules.gestionFichier.code import getLog
from modules.webConfig import launch_process
from modules.webConfig import readConfig


@gestionFichier.route('/<path:pathFiles>',methods=['GET'])
def lancement_gestionFichier(pathFiles):
    path = os.path.expanduser(app.config["GESTIONFICHIER_DDL_PATH"])
    pathFiles = '/' + pathFiles
    treeFiles = make_tree(pathFiles.encode('utf-8'), True, app.config["GESTIONFICHIER_LST_EXCL_FILES"])
    treePath = make_tree(path.encode('utf-8'), False, app.config["GESTIONFICHIER_LST_EXCL_PATH"])
    return render_template('gestionFichier.html',file_list=treeFiles,path_list=treePath,pathFiles=pathFiles)
@gestionFichier.route('/<path:pathFiles>',methods=['POST'])
def traitement_gestionFichier(pathFiles):
    pathFiles = Action(request, pathFiles)
    return redirect(url_for('gestionFichier.lancement_gestionFichier',pathFiles=pathFiles))

    
@gestionFichier.route('/scripts/<path:pathFiles>',methods=['GET'])
def FichiersScriptsGET(pathFiles):
    pathFiles = '/' + pathFiles
    treeFiles = recup_files(pathFiles.encode('utf-8'), "")
    return render_template('scripts.html',file_list=treeFiles,pathFiles=pathFiles)
@gestionFichier.route('/scripts/<path:pathFiles>',methods=['POST'])
def FichiersScriptsPOST(pathFiles):
    # pathFiles = '/' + pathFiles
    app.logger.info('Enregistrement_script : ' + str(request.form))
    pathFiles = Action(request, pathFiles)
    app.logger.info('script enregistré')
    return redirect(url_for('gestionFichier.FichiersScriptsGET',pathFiles=pathFiles))
@gestionFichier.route('/_retScripts/<path:pathFiles>', methods=['GET'])
def retScriptsGET(pathFiles):
    pathFiles = './' + pathFiles
    app.logger.info('lancement_script : ' + pathFiles)
    # ret = launch_process(['sh', pathFiles])
    ret = launch_process([pathFiles,''])
    app.logger.info(' retour script : ' + str(ret))
    return jsonify(ret)
@gestionFichier.route('/_modScripts/<path:pathFiles>', methods=['GET'])
def modScriptsGET(pathFiles):
    pathFiles = '/' + pathFiles;
    app.logger.info('Modification_script : ' + pathFiles)
    content = readConfig(pathFiles).strip()
    # app.logger.info(' contenu script : ' + content)
    return jsonify({'name':pathFiles,'content':content})
    
@gestionFichier.route('/log/<path:pathFiles>',methods=['GET'])
def FichiersLogGET(pathFiles):
    return render_template('log.html',pathFiles=pathFiles)
@gestionFichier.route('/log/<path:pathFiles>',methods=['POST'])
def FichiersLogPOST(pathFiles):
    pathFiles = Action(request, pathFiles)
    return redirect(url_for('gestionFichier.FichiersLogGET',pathFiles=pathFiles))
@gestionFichier.route('/log/_majData/<path:pathFiles>',methods=['GET'])
def FichiersLogMAJ(pathFiles):
    return getLog('/' + pathFiles)