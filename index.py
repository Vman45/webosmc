#! /usr/bin/python 
# -*- coding:utf-8 -*- 
                                                                                                                                                                                                              
from flask import Flask, flash, render_template, redirect, request, url_for
app = Flask(__name__)  
app.debug = True
app.secret_key = 'kugan49'
#OK Terminé
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/dev/')
def dev():
    url_root=request.url_root.lstrip()
    ind=url_root.find(':',6)
    if (ind != -1) : url_root = url_root[: ind]
    url_root=url_root.replace('http://','https://')
    if (url_root.endswith('/') == False) : url_root+='/'
    return render_template('dev.html',path=url_root)
@app.route('/JD/')
def JD():
  return render_template('jDownloader.html',path='https://my.jdownloader.org/?deviceId=f85d6762b1f540de196fa733c649891b#webinterface:downloads')
@app.route('/majWeb/')
def majWeb():
    #import subprocess
    import os
    #os.system('git --git-dir /home/osmc/webosmc/.git pull --no-edit')
    os.system('sh /home/osmc/scripts/majWeb.sh')
    flash('OK<br>maj effectuée !!!!')
    return redirect(url_for('index'))

  
  
#                                         En cours développement
@app.route('/test/')
def test():
    return 'Test OK !!!' + request.url_root + '<br>' + request.base_url
@app.route('/orgaFic/<path:pathFiles>')
def orgaFic(pathFiles):
    #return render_template('/DDL/index.html',pathFiles=pathFiles,path='/')
    return render_template('orgaFic.html',pathFiles=pathFiles,path='/')

@app.route('/FolderBuilder/')
def FolderBuilder():
    return render_template('/jqueryfiletree/tests/manual/index.html')
    #return render_template('/FolderBuilder/index.html')
  
    
  
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
                                                                                                                                                                                                              
     
