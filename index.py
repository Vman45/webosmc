#! /usr/bin/python 
# -*- coding:utf-8 -*- 
                                                                                                                                                                                                              
from flask import Flask, render_template, jsonify
app = Flask(__name__)                                                                                                                                                                                         
                                                                                                                                                                                                              
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/test')
def test():
    return 'Test OK !!!'
@app.route('/orgaFic')
def orgaFic():
    return render_template('orgaFic.html')
@app.route('/dev')
def dev():
    return render_template('dev.html')
                                                                                                                                                                                                              
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
                                                                                                                                                                                                              
                                                                                                                                                                                                              
@app.route('/background_process')
def background_process():
    try:
         lang = request.args.get('proglang', 0, type=str)
         if lang.lower() == 'python':
            return jsonify(result='You are wise')
         else:
            return jsonify(result='Try again.')
    except Exception as e:
         return str(e)