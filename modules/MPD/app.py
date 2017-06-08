
from flask import Flask, render_template, request, abort, Response, Blueprint
app = Flask(__name__)
app.config.from_object('config')
MPDClient = Blueprint('MPDClient',__name__, template_folder='templates')


import ConfigParser
from functools import wraps
import json
from modules.MPD.libs.mpdsafe import MpdSafe

config = ConfigParser.SafeConfigParser()
mpd = MpdSafe()
plugins = {}
InitDone = False

import inspect
import logging
import os
import os.path
import sys


def init():
    config_file=app.config["MPD_CONFIG"]
    config.read(config_file)
    plugin_configs = {}
    for section in config.sections():
        if not section.startswith("plugin-"): continue
        plugin_configs[section[7:]] = dict([(option, config.get(section, option)) for option in config.options(section)])

    # mpd->stream is special as it implies plugins-player->has_stream
    plugin_configs['player']['has_stream'] = bool(config.get('mpd', 'stream'))

    # connect to MPD
    mpd.connect(config.get("mpd", "host"), config.getint("mpd", "port"))

    # discover plugins
    plugins = get_instances(mpd, config.get("plugins", "banned").split(","), plugin_configs)
    InitDone = True
   
def get_instances(mpd, bannend_plugins=[], plugin_configs={}):
    """ instantiate classes which inherits of me, return the list """
    instances = {}
    base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "plugins")

    for plugin_file_name in os.listdir(base_dir):
        # filter out directories
        if not os.path.isfile(os.path.join(base_dir, plugin_file_name)): continue

        # filter out non py files
        if not plugin_file_name.endswith(".py"): continue

        # filter out special modules
        if plugin_file_name in ("__init__.py", ): continue

        # determine actual module name
        plugin_module_name = os.path.splitext(plugin_file_name)[0]

        # check for ban
        if plugin_module_name in bannend_plugins: continue

        # load it
        try:
            __import__("MPD.plugins.%s" % plugin_module_name)
        except Exception, m:
            app.logger.exception("Plugin import error for [%(name)s]: %(error)s" % {'name': plugin_module_name, 'error': m})
            continue

        # lookup module
        plugin_module = sys.modules["MPD.plugins.%s" % plugin_module_name]

        # lookup class
        if not hasattr(plugin_module, plugin_module_name.capitalize()): continue
        plugin_class = getattr(plugin_module, plugin_module_name.capitalize())

        # make sure its the right one
        if not inspect.isclass(plugin_class):
            continue

        app.logger.info(" - load plugin: %s" % plugin_module_name.capitalize())
        try:
            instances[plugin_module_name] = plugin_class(mpd, plugin_configs.get(plugin_module_name, {}))
            instances[plugin_module_name].name = plugin_module_name
        except Exception, m:
            app.logger.error("Plugin instantiation error for %s: %s" % (plugin_module_name, m))
    app.logger.debug("return plugins " + str(instances))
    return instances

                       
                       
                       
                       
def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if InitDone == False:
            init()
        if config.has_option("auth", "enabled") and config.getboolean("auth", "enabled"):
            auth = request.authorization
            if not auth or not (auth.username == config.get("auth", "username") and auth.password == config.get("auth", "password")):
                return Response('Could not verify your access level for that URL.\nYou have to login with proper credentials', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
        return f(*args, **kwargs)
    return decorated


@MPDClient.route('/MPD/')
@requires_auth
def root():
    return render_template('MPD_main.html',
                           player=plugins['player'].index(),
                           player_playlist=plugins['player'].playlist(),
                           player_stream=config.get("mpd", "stream") if config.has_option("mpd", "stream") else None,
                           plugins=sorted(plugins.values(), key=lambda plugin: plugin.button_index))


@MPDClient.route('/player')
@requires_auth
def player():
    return render_template('MPD_player.html')


@MPDClient.route('/plugin/<plugin>', methods=["GET", "POST"])
@MPDClient.route('/plugin/<plugin>/<method>', methods=["GET", "POST"])
@requires_auth
def plugin_methods(plugin, method=None):
    inst = plugins[plugin.lower()]
    args = request.form.to_dict()

    if method is None:
        method = "index"

    if hasattr(inst, method):
        return app.make_response(getattr(inst, method)(**args))

    abort(404)


@MPDClient.route('/__ajax/<method>', methods=["GET", "POST"])
@MPDClient.route('/__ajax/<plugin>/<method>', methods=["GET", "POST"])
@requires_auth
def ajax_methods(method, plugin=None):
    # right now the core has no ajax methods
    if plugin is None:
        abort(404)

    # process plugin ajax methods
    inst = plugins[plugin.lower()]
    args = request.form.to_dict()

    if hasattr(inst, "ajax_" + method):
        # set cach-control header for Safari on iOS 6
        response = app.make_response(json.dumps(getattr(inst, "ajax_" + method)(**args)))
        response.headers["Cache-Control"] = "no-cache"
        return response

    abort(404)
