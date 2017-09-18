from flask import Flask, render_template, request, abort, Response, Blueprint
ThrowBox = Blueprint('ThrowBox',__name__, static_folder='static', static_url_path='/modules/ThrowBox/static', template_folder='/modules/ThrowBox/templates')
app = Flask(__name__)
app.config.from_object('config')


import ConfigParser
from functools import wraps
config = ConfigParser.SafeConfigParser()

InitDone = False

import os
import time
import functions

def init():
    config_file=app.config["THROWBOX_CONFIG"]
    config.read(config_file)
    plugin_configs = {}
    for section in config.sections():
        plugin_configs[section] = dict([(option, config.get(section, option)) for option in config.options(section)])
    InitDone = True
    
                       
def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if InitDone == False:
            init()
        if config.has_option("AUTH", "Enabled") and config.getboolean("AUTH", "Enabled"):
            auth = request.authorization
            if not auth or not (auth.username == config.get("AUTH", "userName") and auth.password == config.get("AUTH", "Password")):
                return Response('Could not verify your access level for that URL.\nYou have to login with proper credentials', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
        return f(*args, **kwargs)
    return decorated
    
@app.route("/")
@requires_auth
def index():
	return flask.render_template("index.html")

@app.route("/browse/")
@requires_auth
def root():
	BASE_PATH=""
	folders,files=functions.ReadPath("")
	#route=["/"]
	print(files)
	return flask.render_template("root.html",**locals())

@app.route("/browse/<path:path>")
@requires_auth
def browse(path):
	BASE_PATH=path

	# 404
	if functions.ReadPath(path)==None:
		functions.log("Error; 404; IP=%s" % flask.request.remote_addr)
		Error404=True
		ClientIP=flask.request.remote_addr
		return flask.render_template("browse.html",**locals())
	
	elif functions.IsFile(path):
		return flask.send_file(functions.RepoPath(path))
		
	else:
		folders,files=functions.ReadPath(path)

		# Remove the hidden files and folders (hidden=beggining with ".")
		folders=functions.RemoveHiddenObjects(folders)
		files=functions.RemoveHiddenObjects(files)

		# Sort the folders and files list.
		folders.sort()
		files.sort()

	route=path.split("/")

	return flask.render_template("browse.html",**locals())