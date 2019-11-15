PATH = "/home/osmc/webosmc/"
DEBUG = False  # Turns on debugging features in Flask
PORT = 5000
SECRET_KEY = "Kugan49"
LINK_AFF_MSG = False
LINK_MAJ_SITE = ["git", "--git-dir=" + PATH + ".git", "--work-tree=" + PATH, "pull"]
LINK_VERIFMAJ = ["sh",PATH + "verifVersion.sh"]
LINK_JDOWNLOADER = "https://my.jdownloader.org/?deviceId=4ad32ae65d600a9b070bba54a8f0429d#webinterface:downloads"
GESTIONFICHIER_DDL_PATH = "/mnt/LOC/USB"
GESTIONFICHIER_LST_EXCL_PATH = ['$RECYCLE.BIN','sauve', 'System Volume Information', 'test','install', 'musique', 'photos','lost+found']
GESTIONFICHIER_LST_EXCL_FILES = ['.partf','.chunk']
KODI_START = ["/usr/bin/sudo","-H systemctl start mediacenter"]
PYLOAD_START = ["/usr/bin/sudo","-H bash /home/osmc/scripts/wake_pyload.sh"]
STATUS_CPUMIN=2
STATUS_LSTPROC={}
STATUS_LSTPROC[0] = {"Kodi":"kodi.bin"}
STATUS_LSTPROC[1] = {"JDownloader":"java"}
STATUS_LSTPROC[2] = {"Synchronisation":"unison"}
STATUS_LSTPROC[3] = {"Jace":"python3"}
STATUS_LSTPROC[4] = {"pyload":"python"}
STATUS_LSTPROC[5] = {"Monit":"monit"}
STATUS_RECH_VERSION={}
STATUS_RECH_VERSION[0]={"Version OSMC locale" :["grep","VERSION_ID","/etc/os-release"]}
STATUS_RECH_VERSION[1]={"Version OSMC Disponible" : ["curl","-s","https://raw.githubusercontent.com/osmc/osmc/master/package/base-files-osmc/files/etc/os-release","|","grep","VERSION_ID"]}
STATUS_RECH_VERSION[2]={"Version Kodi" :["grep","Kodi","/home/osmc/.kodi/temp/kodi.log", "|","head", "-3"]}
LST_IP_TEST={}
LST_IP_TEST[0]={u"Portable J" : "192.168.1.31"}
LST_IP_TEST[1]={u"Portable C" : "192.168.1.32"}
THROWBOX_CONFIG=PATH + "modules/ThrowBox/throwbox.ini"
GEN_MENU={
    0: {
        'name': u'Accueil',
        'path':u'/',
        'title': u''
        },
   2: {
        'name': u'T\xe9l\xe9chargements',
        'path': u'SubMenuTitle',
        0: {
            'name':u'Fichiers',
            'path': u'/gestionFichier/mnt/LOC/USB/DDL_OK/',
            'title': u'Gestion des fichiers',
            'description': u'Permet de d\xe9placer, copier, supprimer des fichiers sur osmc',
            'icone': '/static/image/icons8-individual-server-80.png'
            },

        1: {
            'name': u'JDownloader',
            'path': u'/JD/',
            'title': u'JDownloader',
            'description': u'Gestion des t\xe9l\xe9chargements (application externe)',
            'icone': '/static/image/icons8-jdownloader-80.png'
            },
        2: {
            'name': u'Pyload',
            'path': u'/int_pyload/',
            'title': u'Py Load',
            'description': u'Gestion des t\xe9l\xe9chargements (application externe)',
            'icone': '/static/image/pyload.png'
            }
        },
    3: {
       'name':u'T\xe9l\xe9commande',
       'path': u'SubMenuTitle',
        0: {
            'name': u'Multim\xe9dia',
            'path': u'/kodi/',
            'title': u'Kodi Multim\xe9dia',
            'description': u'T\xe9l\xe9commande pour l\'interface multim\xe9dia d\'osmc',
            'icone': '/static/image/icons8-tv-80.png'
            }
        },
    4: {
        'name':u'Etat',
        'path': u'SubMenuTitle',
        0: {
            'name': u'Statuts',
            'path': u'/status/',
            'title': u'Statuts',
            'description': u'Visualiser l\'\xe9tat d\'osmc (processeur, m\xe9moire, disque, ...)',
            'icone': '/static/image/icons8-dashboard-80.png'
            },
        1: {
            'name': u'log',
            'path': u'/gestionFichier/log/home/osmc/tmp/',
            'title': u'Logs',
            'description': u'V\xe9rfier les logs de diff\xe9rents traitements d\'osmc',
            'icone': '/static/image/icons8-order-history-80.png'
            }
        },
    5: {
        'name':u'Avanc\xe9es',
        'path': u'SubMenuTitle',
        0: {
            'name': u'Scripts',
            'path': u'/gestionFichier/scripts/home/osmc/scripts/',
            'title': u'Ex\xe9cution',
            'description': u'Permet de lancer des scripts sur osmc',
            'icone': '/static/image/icons8-run-command-80.png'
            },
        1: {
            'name': u'SSH',
            'path': u'/SSH/',
            'title': u'Console SSH',
            'description': u'Acc\xe8s en mode console \xe0 osmc (EXPERTS)',
            'icone': '/static/image/icons8-console-80.png'
            },
        2: {
            'name': u'Config',
            'path': u'/config/home/osmc/webosmc/config.py',
            'title': u'R\xe9glagles',
            'description': u'Configuration des param\xe8tres du serveur web osmc',
            'icone': '/static/image/icons8-adjust-80.png'
            }

        },
    6: {
        'name': u'Cloud',
        'path': u'/ThrowBox/',
        'title': u'Cloud',
        'description': u'T\xe9l\xe9chargment de fichiers pr\xe9sents sur osmc',
        'icone': '/static/image/icons8-download-from-the-cloud-80.png'
        }
    }

#1: {
#        'name': u'homeassistant',
#        'path': u'/homeassistant/',
#        'title': u'Home Assistant',
#        'description': u'Interface de gestion de la Domotique pour la maison',
#        'icone': '/static/images/homeassistant.png'
#        },

#  1: {
#            'name': u'pyload',
#            'path': u'/pyload/',
#            'title': u'Py Load',
#            'description': u'Gestion des t\xe9l\xe9chargements (application interne)',
#            'icone': '/static/images/pyload.png'
#            },
