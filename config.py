PATH = "/home/osmc/webosmc/"
DEBUG = False  # Turns on debugging features in Flask
PORT = 5000
SECRET_KEY = "Kugan49"
LINK_AFF_MSG = False
LINK_MAJ_SITE = ["git", "--git-dir=" + PATH + ".git", "--work-tree=" + PATH, "pull"]
LINK_VERIFMAJ = ["sh",PATH + "verifVersion.sh"]
LINK_JDOWNLOADER = "https://my.jdownloader.org/?deviceId=4ad32ae65d600a9b070bba54a8f0429d#webinterface:downloads"
GESTIONFICHIER_DDL_PATH = "/mnt/LOC/USB"
GESTIONFICHIER_LST_EXCL_PATH = ['$RECYCLE.BIN','sauve', 'System Volume Information', 'test','install', 'musique', 'photos']
GESTIONFICHIER_LST_EXCL_FILES = ['.part','xyztetst']
KODI_START = ["/usr/bin/sudo","-H systemctl start mediacenter"]
STATUS_CPUMIN=2
STATUS_LSTPROC={}
STATUS_LSTPROC[0] = {"Kodi":"kodi.bin"}
STATUS_LSTPROC[1] = {"JDownloader":"java"}
STATUS_LSTPROC[2] = {"MPD":"mpd"}
STATUS_LSTPROC[3] = {"Synchronisation":"unison"}
STATUS_LSTPROC[4] = {"Jace":"python3"}
STATUS_LSTPROC[5] = {"pyload":"python"}
STATUS_LSTPROC[6] = {"Monit":"monit"}
STATUS_RECH_VERSION={}
STATUS_RECH_VERSION[0]={"Version OSMC locale" :["grep","VERSION_ID","/etc/os-release"]}
STATUS_RECH_VERSION[1]={"Version OSMC Disponible" : ["curl","-s","https://raw.githubusercontent.com/osmc/osmc/master/package/base-files-osmc/files/etc/os-release","|","grep","VERSION_ID"]}
STATUS_RECH_VERSION[2]={"Version Kodi" :["grep","Kodi","/home/osmc/.kodi/temp/kodi.log", "|","head", "-3"]}
MPD_CONFIG=PATH + "modules/MPD/MPD.ini"
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
            'icone': 'https://png.icons8.com/individual-server/androidL/96'
            },
      
        1: {
            'name': u'JDownloader',
            'path': u'/JD/',
            'title': u'JDownloader',
            'description': u'Gestion des t\xe9l\xe9chargements (application externe)',
            'icone': 'https://png.icons8.com/jdownloader/androidL/96'
            },
        2: {
            'name': u'Pyload',
            'path': u'/pyload/',
            'title': u'Py Load',
            'description': u'Gestion des t\xe9l\xe9chargements (application externe)',
            'icone': 'https://png.icons8.com/software-installer/androidL/96'
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
            'icone': 'https://png.icons8.com/tv/androidL/96'
            },
        1: {
            'name': u'Musique',
            'path': u'/MPD/',
            'title': u'Musique',
            'description': u'Piloter la musique d\'osmc et \xe9coute directe',
            'icone': 'https://png.icons8.com/musical-notes/androidL/96'
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
            'icone': 'https://png.icons8.com/dashboard/androidL/96'
            },
        1: {
            'name': u'log',
            'path': u'/gestionFichier/log/home/osmc/tmp/',
            'title': u'Logs',
            'description': u'V\xe9rfier les logs de diff\xe9rents traitements d\'osmc',
            'icone': 'https://png.icons8.com/order-history/androidL/96'
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
            'icone': 'https://png.icons8.com/run-command/androidL/96'
            },
        1: {
            'name': u'SSH',
            'path': u'/SSH/',
            'title': u'Console SSH',
            'description': u'Acc\xe8s en mode console \xe0 osmc (EXPERTS)',
            'icone': 'https://png.icons8.com/console/androidL/96'
            },
        2: {
            'name': u'Config',
            'path': u'/config/home/osmc/webosmc/config.py',
            'title': u'R\xe9glagles',
            'description': u'Configuration des param\xe8tres du serveur web osmc',
            'icone': 'https://png.icons8.com/adjust/androidL/96'
            }

        },
    6: {
        'name': u'Cloud',
        'path': u'/ThrowBox/',
        'title': u'Cloud',
        'description': u'T\xe9l\xe9chargment de fichiers pr\xe9sents sur osmc',
        'icone': 'https://png.icons8.com/download-from-the-cloud/androidL/96'
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
