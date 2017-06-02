#! /bin/sh
# Creation d'un nom de fichier de verouillage :
LOCKFILE="/home/osmc/tmp/launchserver.PIDLck" ;
TMPFILE="/home/osmc/tmp/launchserver.log"
# Si un fichier de lock existe ...
[ -e ${LOCKFILE} ] && {
       echo "Fichier de lock anterieur trouve..." > ${TMPFILE} 2>&1
#       Verifions si le processus est en cours :
       [ -d /proc/$(cat ${LOCKFILE}) ] && {
#               Si oui, fin de script :
              echo "Processus encore actif. Fin." > ${TMPFILE} 2>&1
              exit 0 ;
       } || {
#               Si non le fichier a ete oublie. Il est supprime :
               echo "Processus termine. Nettoyage." > ${TMPFILE} 2>&1
               rm ${LOCKFILE} ;
       }
}
# Creation du fichier de lock :
echo ${$} > ${LOCKFILE} ;
python "/home/osmc/webosmc/index.py" > ${TMPFILE} 2>&1 &
