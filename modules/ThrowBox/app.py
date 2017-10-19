# coding: utf-8
from flask import Flask, render_template, request, abort, Response, Blueprint, send_file
ThrowBox = Blueprint('ThrowBox',__name__, static_folder='static', static_url_path='/modules/ThrowBox/static', template_folder='templates')
app = Flask(__name__)
app.config.from_object('config')


import ConfigParser
from functools import wraps
config = ConfigParser.SafeConfigParser()
import base64

InitDone = False
StockPath = ""
TempPass = False

import os
import time
import functions
import platform
import datetime
from werkzeug import secure_filename

def init():
    if platform.system()[:3] == 'Win':
        LOCAL_PATH=os.path.dirname(os.path.realpath(__file__))
        config_file=os.path.join(LOCAL_PATH, "throwbox.ini")
    else:
        config_file=app.config["THROWBOX_CONFIG"]
    config.read(config_file)
    global StockPath
    StockPath=config.get("REPO","path").decode('utf-8',errors='ignore')
    InitDone = True
    

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if InitDone == False:
            init()
        if config.has_option("AUTH", "enabled") and config.getboolean("AUTH", "enabled"):
            auth = request.authorization
            app.logger.info('Asking authorization auth %s' %auth)
            # Identifiant temporaire = temp
            # mot de passe temporaire = YYYYWW
            tempdate = datetime.date.today().isocalendar()
            temppassword = str(tempdate[0]) + str(tempdate[1])
            global TempPass
            if not auth:
                return Response(u"Autorisation acces refuse\nVous devez vous authentifier correctement", 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
            elif (auth.username == config.get("AUTH", "username") and auth.password ==  base64.b64decode(config.get("AUTH", "password"))):
                TempPass = False
                app.logger.info('authorized master')
            elif (auth.username == "temp" and auth.password == temppassword):
                TempPass = True
                app.logger.info('authorized temp')
            else:
                return Response(u"Autorisation acces refuse\nVous devez vous authentifier correctement", 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
        return f(*args, **kwargs)
    return decorated
    
@ThrowBox.route("/")
@requires_auth
def index():
    auth = ''
    return render_template("throwbox.html")

@ThrowBox.route("/browse/")
@requires_auth
def root():
    BASE_PATH=""
    # app.logger.info('StockPath : ' + StockPath)
    folders,files=functions.ReadPath(StockPath)
    print(files)
    return render_template("root.html",**locals())

@ThrowBox.route("/browse/<path:path>", methods = ['GET', 'POST'])
@requires_auth
def browse(path):
    BASE_PATH=path
    path=os.path.join(StockPath,path)
    
    if request.method == 'POST':
        f = request.files['file']
        filename = secure_filename(f.filename)
        f.save(os.path.join(path, filename))
        # return 'file uploaded successfully'
        Message = 'file uploaded successfully'
        return render_template("browse.html",**locals())
    else:
        if functions.IsFile(path) or functions.ReadPath(path)==None or TempPass == True:
            functions.log("Error; 404; IP=%s" % request.remote_addr)
            Error404=True
            ClientIP=request.remote_addr
            return render_template("browse.html",**locals())
        else:
            folders,files=functions.ReadPath(path)
            # app.logger.info("folders: %s  \n files : %s" %(folders,files))
            # Remove the hidden files and folders (hidden=beggining with ".")
            folders=functions.RemoveHiddenObjects(folders)
            files=functions.RemoveHiddenObjects(files)

            # Sort the folders and files list.
            folders.sort()
            files.sort()
        tmproute=path.split("/")
        route=[]
        u="/ThrowBox/browse"
        for r in tmproute:
            if r not in StockPath:
                u=u + '/' + r
                route.append(dict(name=r, url=u))        
            
        # app.logger.info("route: %s" %route)
        return render_template("browse.html",**locals())

@ThrowBox.route("/download/<path:path>", methods = ['GET'])
@requires_auth
def download(path):
    BASE_PATH=path
    path=os.path.join(StockPath,path)
   
    if functions.IsFile(path):
        return send_file(path)
    # 404
    elif functions.ReadPath(path)==None or TempPass == True:
        functions.log("Error; 404; IP=%s" % request.remote_addr)
        Error404=True
        ClientIP=request.remote_addr
    else:
        folders,files=functions.ReadPath(path)
        
        # Gestion du téléchargement 
        
        # app.logger.info("folders: %s  \n files : %s" %(folders,files))
        # Remove the hidden files and folders (hidden=beggining with ".")
        folders=functions.RemoveHiddenObjects(folders)
        files=functions.RemoveHiddenObjects(files)

        # Sort the folders and files list.
        folders.sort()
        files.sort()
    return render_template("browse.html",**locals())