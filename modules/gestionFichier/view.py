# coding: utf-8
import codecs, os
from flask import Flask,render_template, redirect, request, url_for, Blueprint
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