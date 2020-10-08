from datetime import date

import pymongo
from bson import json_util
from flask import Flask, jsonify, request, json, render_template, url_for
from flask.json import dumps, loads
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.utils import redirect

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost/blog'
mongo = PyMongo(app)
artigos = mongo.db.artigos
autores = mongo.db.autores




@app.route('/artigos', methods=['GET'])
def get_all_artigos():
    output = []
    for q in artigos.find():
        output.append({ 'id':str(q['_id']) ,'Titulo' : q['titulo'], 'data' : q['data'],'texto' : q['texto'], 'autor' : q['autor']['nome']  })

    tam = len(output)
    print(tam)
    return render_template('lista2.html', titulo='Blog', lista=output,tamanho=tam)

@app.route('/artigos/<texto>', methods=['GET'])
def get_search_artigo(texto):

    output = []
    for q in artigos.find(
            {"$or": [{"titulo": {'$regex': texto}}, {"texto": {'$regex': texto}}, {"autor.nome": {'$regex': texto}}]}):

             output.append({'id':str(q['_id']) ,'Titulo': q['titulo'], 'texto': q['texto'], 'autor': q['autor']['nome']})

    tam = len(output)
    print(tam)
    return render_template('lista2.html', titulo='Blog', lista=output,tamanho = tam )

@app.route('/remover/<id>')
def get_remover_artigos(id):
    artigos.delete_one({'_id': ObjectId(id)})
    return redirect('/artigos')


@app.route('/artigosmany/', methods=['POST'])
def get_search_artigos():
    texto = request.form['texto']
    return get_search_artigo(texto)

@app.route('/novo')
def novo():
        return render_template('novo.html', titulo='Novo artigo')


@app.route('/atualizar/<id>')
def get_atualizar_artigos(id):
    for dado in artigos.find({'_id': ObjectId(id)}):
        pass
    return render_template('atualizacao.html', titulo='Atualizar artigo',dado =dado )


@app.route('/atualizar', methods=['POST',])
def atualizar():
    dados=[]
    texto = request.form
    for key, value in texto.items():
        dados.append(value)
    artigos.update_one({"_id": ObjectId(dados[0])},  {'$set': {"texto": dados[2],"titulo":dados[1]  }  })
    return get_all_artigos()

@app.route('/remover/', methods=['POST'])
def remove_framework():
    id = request.json['_id']
    artigos.delete_one({'_id': ObjectId(id)})
    autores.delete_one({'_id': ObjectId(id)})
    return redirect('/artigos')

@app.route('/inserir', methods=['POST',])
def inserir():
    output={}
    titulo = request.form['titulo']
    texto = request.form['texto']
    autor = request.form['autor']


    for q in autores.find({"nome": {'$regex': autor}}):
        id = "ObjectId(" + str(q['_id']) + ")"
        autor =q['nome']
        if id != "":
            output = {
            "titulo": titulo,
            "data": str(date.today()),
            "texto": texto,
            "url": "http://20.30.40.70",
            "status": 1,
            "autor": {
                "_id": id,
                "nome": autor
            }
            }
            artigos.insert((output))
    return redirect('/artigos')

@app.route('/novoautor')
def novoautor():
        return render_template('autor.html')

@app.route('/inserirautor', methods=['POST',])
def inserirautor():
    output={}
    nome = request.form['nome']
    bio = request.form['bio']
    output = {
            "nome": nome,
            "bio": bio,
            }
    autores.insert(output)
    return redirect('/artigos')

@app.route('/', methods=['GET'])
def inicio():
      return redirect('/artigos')

if __name__ == '__main__':
    app.run(debug=True)