#!/usr/bin/python
# -*- coding: utf-8 -*-

import subprocess
from flask import current_app as app
#############################################################################
def ping_pc(ip, encodage="cp850"):
    """envoie un ping à l'ordinateur d'adresse ip, et retourne la réponse
       sous forme d'une liste de lignes unicode
    """    
    commande = ["ping", "-q","-W","1","-w","1",ip]
    try:
        out, _ = subprocess.Popen(commande, 
                                  stdout=subprocess.PIPE, 
                                  stderr=subprocess.STDOUT).communicate()
    except (ValueError, OSError) as err:
        return ("Erreur: %s" % (err.args[0],)).decode(encodage)
    reponse = out.decode(encodage)
    return reponse.splitlines()
 
#############################################################################
def connectok(ip):
    """dit si un PC dont l'adresse ip est donnée, est connecté ou non
    """
    # envoi d'un ping à l'ip donné et saisie de la réponse
    lignes = ping_pc(ip)
    print lignes
    if u"bad address" in lignes[0]:
        return "ON" #ip + u" => nom de domaine introuvable"
    else:
        # recherche de la 1ère ligne vide au delà de la 1ère (=> indice k)
        for i, ligne in enumerate(lignes[1:]):
            if u"round-trip" in ligne: 
                return "ON" #ip + u" => connected"
                break
        return "OFF" #ip + u" => non connected"

def returnState(LstInfos):
    LstInfosRet = []
    # app.logger.debug("LstInfos: %s" %LstInfos)
    for key,info in LstInfos.items():
        for name,ip in info.items():
            # app.logger.debug("name: %s , info: %s" %(name,ip))
            ret = connectok(ip)
            LstInfosRet.append({'name':name,'value':ret})
    # app.logger.debug("LstInfosRet: %s" %LstInfosRet)
    return LstInfosRet
    
if __name__ == '__main__':
    ip1 = "192.168.1.13" # PC Bureau
    ip2 = "192.168.1.31" # Portable J
    ip3 = "192.168.1.32" # Portable C
    ip4 = "www.google.fr" # accès Web
    ips = [ip1, ip2, ip3, ip4]
     
    for ip in ips:
        print ip
        print connectok(ip)
