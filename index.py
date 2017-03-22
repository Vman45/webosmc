#! /usr/bin/python 
# -*- coding:utf-8 -*- 
                                                                                                                                                                                                              
from flask import Flask, render_template, jsonify
app = Flask(__name__)  
app.debug = True

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
    #subprocess.call('sh /home/osmc/scripts/majWeb.sh',shell=True)
    #status=subprocess.call('git --git-dir /home/osmc/webosmc/.git pull', shell=True) 
    import os
    os.system(''git --git-dir /home/osmc/webosmc/.git pull'')
    return '<br>OK<br>maj effectuée relancer la page précédente et actualiser'
  
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
                                                                                                                                                                                                              
                                                                                                                                                                                                              
@app.route('/background_process/')
def background_process():
    try:
         lang = request.args.get('proglang', 0, type=str)
         if lang.lower() == 'python':
            return jsonify(result='You are wise')
         else:
            return jsonify(result='Try again.')
    except Exception as e:
         return str(e)
