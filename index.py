#! /usr/bin/python 
# -*- coding:utf-8 -*- 
                                                                                                                                                                                                              
from flask import Flask, flash, render_template, redirect, request, url_for
app = Flask(__name__)  
app.debug = True
app.secret_key = 'kugan49'

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/test/')
def test():
    return 'Test OK !!!'
@app.route('/orgaFic/<path:pathFiles>')
def orgaFic(pathFiles):
    return render_template('orgaFic.html',pathFiles=pathFiles,path='/')
@app.route('/dev/')
def dev():
    return render_template('dev.html')
@app.route('/FolderBuilder/')
def FolderBuilder():
    return render_template('/FolderBuilder/index.html')
  
@app.route('/majWeb/')
def majWeb():
    #import subprocess
    import os
    #os.system('git --git-dir /home/osmc/webosmc/.git pull --no-edit')
    os.system('sh /home/osmc/scripts/majWeb.sh')
    flash('OK<br>maj effectuée relancer la page précédente et actualiser')
    return redirect(url_for('index'))
    
  
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
                                                                                                                                                                                                              
     
