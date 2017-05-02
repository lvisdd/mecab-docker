#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os

from flask import Flask
from flask import abort, jsonify, Response, render_template, request
import MeCab

app = Flask(__name__)
# app.config['JSON_AS_ASCII'] = False

@app.route('/')
def hello():
    return 'Hello world!'

# @app.route('/')
# def home():
#   return render_template('index.html')

@app.route("/favicon.ico")
def favicon():
    return app.send_static_file("favicon.ico")

messages = ['Success', 'Faild']

@app.route('/parse', methods=['GET', 'POST'], strict_slashes=False)
def parse():
  try:
    if request.method == 'POST':
        text       = request.form['text']
        dictionary = request.form['dictionary']
    else:
        text       = request.args.get('text', default="", type=str)
        dictionary = request.args.get('dictionary', default="ipadic", type=str)
  except:
        abort(400)
  
  results = mecab_parse(text, dictionary)

  return mecab_response(200, messages[0], results, dictionary)

@app.route('/tokenize', methods=['GET', 'POST'], strict_slashes=False)
def tokenize():
  try:
    if request.method == 'POST':
        text       = request.form['text']
        dictionary = request.form['dictionary']
    else:
        text       = request.args.get('text', default="", type=str)
        dictionary = request.args.get('dictionary', default="ipadic", type=str)
  except:
        abort(400)
  
  results = mecab_tokenize(text, dictionary)

  # return results
  return mecab_response(200, messages[0], results, dictionary)

@app.errorhandler(400)
def error400(error):
    return macab_response(400, messages[1], None, None)

def mecab_response(status, message, results, dictionary):
    return jsonify({'status': status, 'message': message, 'results': results, 'dictionary': dictionary}), status

def mecab_parse(text, dictionary='ipadic'):
    dictionary_dir = "/usr/local/lib/mecab/dic/"
    if dictionary == 'neologd':
        dictionary_name = 'mecab-ipadic-neologd'
    else:
        dictionary_name = dictionary

    m = MeCab.Tagger('-d ' + dictionary_dir + dictionary_name)

    # 出力フォーマット（デフォルト）
    format = ['表層形', '品詞','品詞細分類1', '品詞細分類2', '品詞細分類3', '活用形', '活用型','原型','読み','発音']

    return [dict(zip(format, (lambda x: [x[0]]+x[1].split(','))(p.split('\t')))) for p in m.parse(text).split('\n')[:-2]]

def mecab_tokenize(text, dictionary='ipadic'):
    dictionary_dir = "/usr/local/lib/mecab/dic/"
    if dictionary == 'neologd':
        dictionary_name = 'mecab-ipadic-neologd'
    else:
        dictionary_name = dictionary
    
    # Execute wakati
    m = MeCab.Tagger("-Owakati " + '-d ' + dictionary_dir + dictionary_name)
    result = m.parse(text)
    
    return result

if __name__ == '__main__':
  app.run(host='0.0.0.0')
