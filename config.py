DEBUG = True  # Turns on debugging features in Flask
PORT = 5000
SECRET_KEY = "Kugan49"
GEN_MENU={}
GEN_MENU[0] = {"Accueil":"/"}
GEN_MENU[1] = {"Fichiers":"/gestionFichier/mnt/LOC/USB/DDL_OK/"}
GEN_MENU[2] = {"Musique":"/MPD/"}
GEN_MENU[3] = {"Kodi":"/kodi/"}
GEN_MENU[4] = {"JDownloader":"/JD/"}
GEN_MENU[5] = {"Scripts":"/gestionFichier/scripts/home/osmc/scripts/"}
GEN_MENU[6] = {"SSH":"/SSH/"}  
GEN_MENU[7] = {"Statuts":"/status/"}
GEN_MENU[8] = {"log":"/gestionFichier/log/home/osmc/tmp/"}
GEN_MENU[9] = {"Config":"/config/"}
LINK_AFF_MSG = False
LINK_MAJ_SITE = ["git", "pull"] #"sh /home/osmc/scripts/majWeb.sh"
LINK_VERIFMAJ = ["sh","/home/osmc/webosmc/verifVersion.sh"]#["git","-C /home/osmc/webosmc/ pull --dry-run 2>&1 | grep 'master' >/dev/null |echo $?"]
LINK_JDOWNLOADER = "https://my.jdownloader.org/?deviceId=4ad32ae65d600a9b070bba54a8f0429d#webinterface:downloads"
GESTIONFICHIER_DDL_PATH = "/mnt/LOC/USB"
GESTIONFICHIER_LST_EXCL_PATH = ['$RECYCLE.BIN','save', 'System Volume Information', 'test', 'musique', 'photos']
GESTIONFICHIER_LST_EXCL_FILES = ['.part','xyztetst']
SSH_PORT = 4200
KODI_PORT = 8080
STATUS_CPUMIN=2
STATUS_LSTPROC={}
STATUS_LSTPROC[0] = {"Kodi":"kodi.bin"}
STATUS_LSTPROC[1] = {"JDownloader":"java"}
STATUS_LSTPROC[2] = {"Site web":"python"}
STATUS_LSTPROC[3] = {"MPD":"mpd"}
STATUS_LSTPROC[4] = {"Synchronisation":"unison"}
MPD_CONFIG="/home/osmc/webosmc/modules/MPD/MPD.ini"
# A cabler
# LINK_LOG = ["tail","%s" % (PATH_LOG)] #--verbose --lines 20