from flask import render_template, jsonify, request
from app import app
from app import evolve

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/evolve', methods=['POST'])
def evolver():
    words = request.form['words'].split()

    try:
        generations = int(request.form['generations'])
    except ValueError:
        return jsonify({'error':'Error: Generations must be an integer'})

    rules, words = evolve.evolve(words, generations)

    return jsonify({'rules':rules, 'words':words, 'error':0})
