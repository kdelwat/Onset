from flask import render_template, jsonify, request
from app import app
from app import evolver


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


def format_transcriptions(transcriptions):
    '''Split the raw string of transcriptions into
    the correct tuple rules.'''
    return [(pair.split(':')[0], pair.split(':')[1]) for pair in transcriptions.split('\n')]


@app.route('/evolve', methods=['POST'])
def evolve():
    words = request.form['words'].split()

    try:
        transcriptions = format_transcriptions(request.form['transcriptions'])
    except IndexError:
        return jsonify({'error': 'Error: Transcription seperator must be a colon'})

    try:
        generations = int(request.form['generations'])
    except ValueError:
        return jsonify({'error': 'Error: Generations must be an integer'})

    words, rules = evolver.evolve(words, generations, transcriptions)

    return jsonify({'rules': rules, 'words': words, 'error': 0})
