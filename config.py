DEBUG = True  # Turns on debugging features in Flask
PORT = 5000
SECRET_KEY = "Kugan49"
MAJ_SITE = "sh /home/osmc/scripts/majWeb.sh"
RECH_MAJ = '["git", "fetch --dry-run -v 2>&1 | grep "master" | grep "up" >/dev/null | echo $?"]'  				 
JDOWNLOADER = "https://my.jdownloader.org/?deviceId=4ad32ae65d600a9b070bba54a8f0429d#webinterface:downloads"
DDL_PATH = "/mnt/LOC/USB"
LST_EXCL_PATH = ['$RECYCLE.BIN','save', 'System Volume Information', 'test', 'musique', 'photos']
LST_EXCL_FILES = ['.part','xyztetst']
WYMYPY = "/modules/wymypy/wymypy.ini"
