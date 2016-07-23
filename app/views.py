from flask import render_template, jsonify
from app import app
from app import evolve

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/evolve', methods=['POST'])
def evolver():
    words = ['ppotato', 'paraddʰise']
    rules, words = evolve.evolve(words, 5)

    return jsonify({'rules':rules, 'words':words})
