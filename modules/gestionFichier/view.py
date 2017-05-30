# coding: utf-8
import codecs, os, subprocess
from flask import Flask,render_template, redirect, request, url_for, Blueprint, jsonify
app = Flask(__name__)
app.config.from_object('config')
gestionFichier = Blueprint('gestionFichier',__name__)

@gestionFichier.route('/<path:pathFiles>',methods=['GET'])
def lancement_gestionFichier(pathFiles):
    # from modules.gestionFichier import make_tree
    from modules.gestionFichier.code import make_tree
    path = os.path.expanduser(app.config["GESTIONFICHIER_DDL_PATH"])
    pathFiles = '/' + pathFiles
    treeFiles = make_tree(pathFiles.encode('utf-8'), True, app.config["GESTIONFICHIER_LST_EXCL_FILES"])
    treePath = make_tree(path.encode('utf-8'), False, app.config["GESTIONFICHIER_LST_EXCL_PATH"])
    return render_template('gestionFichier.html',file_list=treeFiles,path_list=treePath,pathFiles=pathFiles)
@gestionFichier.route('/<path:pathFiles>',methods=['POST'])
def traitement_gestionFichier(pathFiles):
    # from modules.gestionFichier import Action
    from modules.gestionFichier.code import Action
    pathFiles = Action(request, pathFiles)
    return redirect(url_for('gestionFichier.lancement_gestionFichier',pathFiles=pathFiles))

    
@gestionFichier.route('/scripts/<path:pathFiles>',methods=['GET'])
def FichiersScriptsGET(pathFiles):
    from modules.gestionFichier.code import recup_files
    pathFiles = '/' + pathFiles
    treeFiles = recup_files(pathFiles.encode('utf-8'), "")
    return render_template('scripts.html',file_list=treeFiles,pathFiles=pathFiles)
@gestionFichier.route('/scripts/<path:pathFiles>',methods=['POST'])
def FichiersScriptsPOST(pathFiles):
    from modules.gestionFichier.code import Action
    pathFiles = Action(request, pathFiles)
    return redirect(url_for('gestionFichier.FichiersScriptsGET',pathFiles=pathFiles))
@gestionFichier.route('/_retScripts/<path:pathFiles>', methods=['GET'])
def retScriptsGET(pathFiles):
    app.logger.info('lancement_script' + pathFiles)
    from modules.gestionFichier.code import launch_script
    ret = launch_script('/' + pathFiles)
    app.logger.info(' retour script' + str(ret))
    return jsonify(ret)
    
@gestionFichier.route('/log/<path:pathFiles>',methods=['GET','POST'])
def FichiersLogGET(pathFiles):
    return render_template('log.html',pathFiles=pathFiles)
@gestionFichier.route('/log/_majData/<path:pathFiles>',methods=['GET'])
def FichiersLogMAJ(pathFiles):
    from modules.gestionFichier.code import getLog
    return getLog(pathFiles)