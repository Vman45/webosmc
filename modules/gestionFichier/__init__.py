# coding: utf-8
import codecs
from flask import  render_template, redirect, request, url_for, Blueprint
app = Blueprint('gestionFichier',__name__)

@app.route('/<path:pathFiles>',methods=['GET'])
def lancement_gestionFichier(pathFiles):
    # from modules.gestionFichier import make_tree
    from code import make_tree
    path = os.path.expanduser(app.config["DDL_PATH"])
    pathFiles = '/' + pathFiles
    treeFiles = make_tree(pathFiles.encode('utf-8'), True, app.config["LST_EXCL_FILES"])
    treePath = make_tree(path.encode('utf-8'), False, app.config["LST_EXCL_PATH"])
    return render_template('gestionFichier.html',file_list=treeFiles,path_list=treePath,pathFiles=pathFiles)
@app.route('/<path:pathFiles>',methods=['POST'])
def traitement_gestionFichier(pathFiles):
    # from modules.gestionFichier import Action
    from code import Action
    pathFiles = Action(request, pathFiles)
    return redirect(url_for('lancement_gestionFichier',pathFiles=pathFiles))