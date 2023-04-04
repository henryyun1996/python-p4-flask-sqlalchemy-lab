#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate
from models import db, Zookeeper, Enclosure, Animal

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def home():
    return '<h1>Zoo app</h1>'

@app.route('/animal/<int:id>')
def animal_by_id(id):
    animal = Animal.query.filter(Animal.id == id).first()
    
    # if not animal:
    #     response_body = '<h1>404 owner not found</h1>'
    #     response = make_response(response_body, 404)
    #     return response
    
    response_body = f'''
    <h1>ID: {animal.id}</h1>
    <ul>Name: {animal.name}</ul>
    <ul>Species: {animal.species}</ul>
    <ul>Zookeeper: {animal.zookeeper.name}</ul>
    <ul>Enclosure: {animal.enclosure.environment}</ul>
    '''

    return make_response(response_body)

@app.route('/zookeeper/<int:id>')
def zookeeper_by_id(id):
    zookeeper = Zookeeper.query.filter(Zookeeper.id == id).first()

    response_body = f'''
    <h1>ID: {zookeeper.id}</h1>
    <ul>Name: {zookeeper.name}</ul>
    <ul>Birthday: {zookeeper.birthday}</ul>
    '''

    for animal in zookeeper.animals:
        response_body += f'<ul>Animal: {animal.name}</ul>'

    return make_response(response_body)

@app.route('/enclosure/<int:id>')
def enclosure_by_id(id):
    enclosure = Enclosure.query.filter(Enclosure.id == id).first()

    response_body = f'''
    <h1>ID: {enclosure.id}</h1>
    <ul>Environment: {enclosure.environment}</ul>
    <ul>Open to Visitors: {enclosure.open_to_visitors}</ul>
    '''

    for animal in enclosure.animals:
        response_body += f'<ul>Animal: {animal.name}</ul>'

    return make_response(response_body)


if __name__ == '__main__':
    app.run(port=5555, debug=True)
