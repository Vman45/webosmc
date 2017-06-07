import ConfigParser
from functools import wraps
import json

from flask import Flask, render_template, request, abort, Response, Blueprint
app = Flask(__name__)
MPDClient = Blueprint('MPDClient',__name__, template_folder='templates')
from modules.MPD.libs.mpdsafe import MpdSafe

config = ConfigParser.SafeConfigParser()
mpd = MpdSafe()
plugins = []

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if config.has_option("auth", "enabled") and config.getboolean("auth", "enabled"):
            auth = request.authorization
            if not auth or not (auth.username == config.get("auth", "username") and auth.password == config.get("auth", "password")):
                return Response('Could not verify your access level for that URL.\nYou have to login with proper credentials', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
        return f(*args, **kwargs)
    return decorated


@MPDClient.route('/MPD')
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

def main():
    config_file=app.config["MPD_CONFIG"]
    wymypy.app.config.read(config_file)
    plugin_configs = {}
    for section in wymypy.app.config.sections():
        if not section.startswith("plugin-"): continue
        plugin_configs[section[7:]] = dict([(option, wymypy.app.config.get(section, option)) for option in wymypy.app.config.options(section)])

    # mpd->stream is special as it implies plugins-player->has_stream
    plugin_configs['player']['has_stream'] = bool(wymypy.app.config.get('mpd', 'stream'))

    # configure logging
    if wymypy.app.config.has_option("general", "logging"):
        logging.basicConfig(filename=wymypy.app.config.get("general", "logging"), format="%(asctime)s %(levelname)s %(message)s", level=logging.DEBUG)
    else:
        logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s", level=logging.DEBUG)

    # connect to MPD
    wymypy.app.mpd.connect(wymypy.app.config.get("mpd", "host"), wymypy.app.config.getint("mpd", "port"))

    # discover plugins
    wymypy.app.plugins = get_instances(wymypy.app.mpd, wymypy.app.config.get("plugins", "banned").split(","), plugin_configs)

    # start server
    wymypy.app.app.run(host=wymypy.app.config.get("server", "interface"),
                       port=wymypy.app.config.getint("server", "port"),
                       debug=wymypy.app.config.getboolean("general", "debug"),
                       request_handler=WyMyPyRequestHandler)
